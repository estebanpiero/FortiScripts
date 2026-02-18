# EMS Endpoints vs VPN Users Check

Compares user identities between a **FortiGate VPN connections report** and a
**FortiClient EMS endpoints export**, then produces three CSV reports showing
which users are unique to each source and which appear in both.

---

## Files

| File | Description |
|---|---|
| `vpn-connections-report.csv` | VPN log exported from FortiGate |
| `endpoints.csv` | Endpoint list exported from FortiClient EMS |
| `compare_users.py` | The comparison script |
| `vpn_only.csv` | Output — users found only in the VPN log |
| `ems_only.csv` | Output — users found only in EMS |
| `both.csv` | Output — users found in both sources |

---

## Requirements

- Python 3.9 or later (no third-party packages needed — uses the standard library only)

---

## How to Run

```bash
python3 compare_users.py
```

Run the script from any directory; it always looks for the input files in its
own folder and writes output files to that same folder.

---

## How It Works

### 1. Reading the VPN report (`vpn-connections-report.csv`)

FortiGate CSV exports include a title comment on the very first line:

```
"###VPN Connections - UserDefined###"
"ID","User","login","logout","Duration","transferred_bytes"
 1 ,"mateamargo","2025-04-14 17:23:32", ...
```

The script detects and skips that comment line automatically, then reads the
`User` column. Because the same user can appear multiple times (one row per
VPN session), duplicates are removed **in memory** — the original file is
never modified.

### 2. Reading the EMS endpoints export (`endpoints.csv`)

EMS wraps the logged-in username in the `fct_users` column with square
brackets:

```
[jdoe]
["jdoe"]
```

The script strips the brackets (and any surrounding quotes) so only the bare
username remains for comparison.

### 3. Normalization

Both sources go through the same cleaning steps before any comparison:

1. Trim leading/trailing whitespace.
2. Remove outer `[` `]` and any inner quote characters.
3. Convert to lowercase (controlled by the `CASE_INSENSITIVE` flag — see
   [Configuration](#configuration) below).

### 4. Set comparison

After normalization, standard Python set operations produce the three groups:

| Operation | Meaning |
|---|---|
| `vpn_users - ems_users` | Users only in VPN log |
| `ems_users - vpn_users` | Users only in EMS |
| `vpn_users & ems_users` | Users in both |

### 5. Output

Each group is written to its own single-column CSV, sorted alphabetically.

---

## Configuration

Open `compare_users.py` and edit the constants near the top of the file:

```python
# Path to the VPN connections report
VPN_CSV = BASE_DIR / "vpn-connections-report.csv"

# Path to the EMS endpoints export
EMS_CSV = BASE_DIR / "endpoints.csv"

# True  → usernames are compared case-insensitively (default)
# False → comparison is exact / case-sensitive
CASE_INSENSITIVE = True
```

If your input files have different names or live in a different folder, update
`VPN_CSV` and `EMS_CSV` accordingly.

---

## Notes

- IP addresses or IPv6 addresses that appear in the VPN `User` column are
  treated as usernames and will show up in the reports as-is. This is normal
  for some FortiGate tunnel configurations where a device IP is logged instead
  of a username.
- The script uses `utf-8-sig` encoding when reading, so files exported from
  Windows (with a BOM) are handled correctly.
