# 🔍 vpn-ldap-user-audit

This Python tool helps system administrators compare active VPN users listed in a CSV report with user accounts stored in an LDAP directory (such as Active Directory). It identifies users that exist in both systems, only in the VPN report, or only in LDAP.

---

## 🚀 Features

- Parses VPN usernames from a CSV report
- Authenticates and queries your LDAP server
- Compares usernames from both sources
- Displays results in a clean, tabulated format

---

## 📦 Requirements

- Python 3.7+
- Packages:
  - `pandas`
  - `ldap3`
  - `tabulate`

Install dependencies:

```bash
pip install pandas ldap3 tabulate
```
## 🔐 Configuration (Environment Variables)

Sensitive values like LDAP credentials and paths should be set using environment variables or loaded from a .env file (use python-dotenv for convenience if desired).

Required Environment Variables

```python
LDAP_SERVER=your.ldap.server
LDAP_PORT=389
LDAP_USER=administrator@example.com
LDAP_PASSWORD=yourpassword
LDAP_BASE_DN=ou=students,dc=example,dc=com
CSV_PATH=vpn-connections-report.csv
```

## 🛠️ Usage

Prepare your VPN CSV report with a User column.

Set your environment variables as above.

Run the script:

```bash
Copy
Edit
python compare_vpn_ldap_users.py
```

## 📄 CSV Format Example

```cs
Date,User,Duration
2024-01-01,jdoe,02:15
2024-01-01,asmith,00:45
```
## 📊 Example Output

```sql
✅ Users in BOTH LDAP and CSV:
+------------+
| Username   |
+------------+
| jdoe       |
| asmith     |
+------------+

❌ Users ONLY in VPN CSV:
+------------+
| Username   |
+------------+
| tempuser   |
+------------+

⚠️ Users ONLY in LDAP:
+---------------+
| Username      |
+---------------+
| newemployee   |
+---------------+
```

## 🧪 Testing

You can simulate testing with a mock CSV file and dummy LDAP entries (or mock the LDAP connection in the code for unit testing).