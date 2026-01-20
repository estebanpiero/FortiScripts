# python3 list_ec_tags_ssh.py --host 192.0.2.10 --user admin --password 'YOURPASS'

#!/usr/bin/env python3
import re
import argparse
import json
import csv
from dataclasses import dataclass, asdict
from typing import List, Optional

import paramiko


@dataclass
class Endpoint:
    record: Optional[int]
    ems_serial: str
    tenant_id: str
    uid: str
    ip: Optional[str] = None
    hostname: Optional[str] = None
    tags: List[str] = None


RE_RECORD = re.compile(r"^Record\s+#(\d+):\s*$", re.MULTILINE)
RE_IP = re.compile(r"^\s*IP Address\s*=\s*(.+?)\s*$", re.MULTILINE)
RE_HOSTNAME = re.compile(r"^\s*Host Name:\s*(.+?)\s*$", re.MULTILINE)
RE_EMS_SN = re.compile(r"^\s*EMS serial number:\s*([A-Za-z0-9]+)\s*$", re.MULTILINE)
RE_TENANT = re.compile(r"^\s*EMS tenant id:\s*([A-Fa-f0-9]{32})\s*$", re.MULTILINE)
RE_UID = re.compile(r"^\s*FortiClient UID:\s*([A-Fa-f0-9]{32})\s*$", re.MULTILINE)
RE_TAG_LINE = re.compile(r"^\s*([A-Za-z0-9_.:\- ]+)\s*$")


def ssh_run(host: str, port: int, user: str, password: Optional[str], keyfile: Optional[str], cmd: str) -> str:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if keyfile:
        pkey = paramiko.RSAKey.from_private_key_file(keyfile)
        client.connect(hostname=host, port=port, username=user, pkey=pkey, timeout=15)
    else:
        client.connect(hostname=host, port=port, username=user, password=password, timeout=15)

    try:
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        if err.strip():
            # FortiGate sometimes writes non-fatal notices to stderr; keep it but don’t always fail.
            pass
        return out
    finally:
        client.close()


def parse_endpoints_from_list(output: str) -> List[Endpoint]:
    matches = list(RE_RECORD.finditer(output))
    endpoints: List[Endpoint] = []
    for i, m in enumerate(matches):
        rec = int(m.group(1))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(output)
        block = output[start:end]

        ems_sn_m = RE_EMS_SN.search(block)
        tenant_m = RE_TENANT.search(block)
        uid_m = RE_UID.search(block)
        if not (ems_sn_m and tenant_m and uid_m):
            continue

        ip_m = RE_IP.search(block)
        hn_m = RE_HOSTNAME.search(block)

        endpoints.append(
            Endpoint(
                record=rec,
                ems_serial=ems_sn_m.group(1),
                tenant_id=tenant_m.group(1),
                uid=uid_m.group(1),
                ip=ip_m.group(1).strip() if ip_m else None,
                hostname=hn_m.group(1).strip() if hn_m else None,
                tags=[],
            )
        )
    return endpoints


def parse_tags_from_find_by_uid(output: str) -> List[str]:
    if "Tags:" not in output:
        return []
    lines = output.splitlines()

    tags: List[str] = []
    in_tags = False
    for line in lines:
        if line.strip() == "Tags:":
            in_tags = True
            continue
        if not in_tags:
            continue
        if line.strip() == "":
            break
        m = RE_TAG_LINE.match(line)
        if m:
            tag = m.group(1).strip()
            if tag:
                tags.append(tag)

    seen = set()
    uniq = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


def main():
    ap = argparse.ArgumentParser(description="List FortiClient endpoints and their security posture tags via SSH")
    ap.add_argument("--host", required=True)
    ap.add_argument("--port", type=int, default=22)
    ap.add_argument("--user", required=True)
    ap.add_argument("--password")
    ap.add_argument("--keyfile", help="SSH private key file (optional)")
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--csv", dest="csv_out")
    args = ap.parse_args()

    list_out = ssh_run(args.host, args.port, args.user, args.password, args.keyfile, "diagnose endpoint ec-shm list")
    endpoints = parse_endpoints_from_list(list_out)

    for ep in endpoints:
        cmd = f"diagnose endpoint ec-shm find-by-uid {ep.uid} {ep.ems_serial} {ep.tenant_id}"
        find_out = ssh_run(args.host, args.port, args.user, args.password, args.keyfile, cmd)
        ep.tags = parse_tags_from_find_by_uid(find_out)

    print(f"{'RECORD':<6} {'IP':<15} {'HOSTNAME':<25} {'UID':<32} {'TAGS'}")
    print("-" * 120)
    for ep in endpoints:
        print(f"{str(ep.record or ''):<6} {(ep.ip or ''):<15} {(ep.hostname or ''):<25} {ep.uid:<32} {', '.join(ep.tags or [])}")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump([asdict(e) for e in endpoints], f, indent=2)
        print(f"\nWrote JSON to: {args.json_out}")

    if args.csv_out:
        with open(args.csv_out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["record", "ip", "hostname", "ems_serial", "tenant_id", "uid", "tags"])
            for e in endpoints:
                w.writerow([e.record, e.ip, e.hostname, e.ems_serial, e.tenant_id, e.uid, "|".join(e.tags or [])])
        print(f"Wrote CSV to: {args.csv_out}")


if __name__ == "__main__":
    main()
