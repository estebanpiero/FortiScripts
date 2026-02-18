"""
compare_users.py
Compares user identities between a FortiGate VPN connections report and
a FortiClient EMS endpoints export, then writes three report CSVs.

Reports produced (in the same directory as the input files):
  vpn_only.csv  – users that appear only in the VPN log
  ems_only.csv  – users that appear only in the EMS endpoints export
  both.csv      – users that appear in both sources
"""

import csv
import pathlib
import re

# ---------------------------------------------------------------------------
# Paths – edit these if the files live elsewhere
# ---------------------------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).parent
VPN_CSV = BASE_DIR / "vpn-connections-report.csv"
EMS_CSV = BASE_DIR / "endpoints.csv"

# Set to True for case-insensitive comparison
CASE_INSENSITIVE = True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize(value: str) -> str:
    """Strip whitespace, square brackets, and optional surrounding quotes."""
    cleaned = value.strip()
    # Remove outer [ ... ] including any internal quotes: [jdoe] / ["jdoe"]
    cleaned = re.sub(r'^\[["\'"]?(.*?)["\'"]?\]$', r'\1', cleaned)
    cleaned = cleaned.strip().strip('"').strip("'")
    if CASE_INSENSITIVE:
        cleaned = cleaned.lower()
    return cleaned


def read_vpn_users(path: pathlib.Path) -> set[str]:
    """
    Read unique, normalised usernames from the VPN report.
    The first line is a report-title comment; real headers start on line 2.
    """
    users: set[str] = set()
    with path.open(newline="", encoding="utf-8-sig") as fh:
        # Skip the comment/title line
        first_line = fh.readline()
        if not first_line.strip().strip('"').startswith("#"):
            # No comment line – rewind and read from the top
            fh.seek(0)

        reader = csv.DictReader(fh)
        for row in reader:
            raw = row.get("User", "").strip()
            if raw:
                users.add(normalize(raw))
    return users


def read_ems_users(path: pathlib.Path) -> set[str]:
    """
    Read unique, normalised usernames from the EMS endpoints export.
    The fct_users column may contain values like [jdoe] or ["jdoe"].
    """
    users: set[str] = set()
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            raw = row.get("fct_users", "").strip()
            if raw:
                users.add(normalize(raw))
    return users


def write_report(path: pathlib.Path, header: str, users: set[str]) -> None:
    """Write a sorted set of usernames to a single-column CSV."""
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([header])
        for user in sorted(users):
            writer.writerow([user])
    print(f"  {len(users):>4} record(s)  →  {path.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"Reading VPN report  : {VPN_CSV.name}")
    vpn_users = read_vpn_users(VPN_CSV)
    print(f"  Unique VPN users   : {len(vpn_users)}")

    print(f"Reading EMS endpoints: {EMS_CSV.name}")
    ems_users = read_ems_users(EMS_CSV)
    print(f"  Unique EMS users   : {len(ems_users)}")

    vpn_only = vpn_users - ems_users
    ems_only = ems_users - vpn_users
    both     = vpn_users & ems_users

    print("\nWriting reports:")
    write_report(BASE_DIR / "vpn_only.csv", "user",  vpn_only)
    write_report(BASE_DIR / "ems_only.csv", "user",  ems_only)
    write_report(BASE_DIR / "both.csv",     "user",  both)

    print("\nDone.")


if __name__ == "__main__":
    main()
