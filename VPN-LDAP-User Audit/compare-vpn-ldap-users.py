import os
import pandas as pd
from tabulate import tabulate
from ldap3 import Server, Connection, ALL, SUBTREE

# === LDAP Configuration ===
LDAP_SERVER = os.getenv("LDAP_SERVER", "your.ldap.server")
LDAP_PORT = int(os.getenv("LDAP_PORT", 389))
LDAP_USER = os.getenv("LDAP_USER", "user@example.com")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD", "yourpassword")
BASE_DN = os.getenv("LDAP_BASE_DN", "ou=students,dc=example,dc=com")
SEARCH_FILTER = '(objectClass=user)'
ATTRIBUTES = ['sAMAccountName']

# === Step 1: Read unique usernames from the VPN CSV ===
def get_csv_usernames(csv_path):
    df = pd.read_csv(csv_path, skiprows=1, quotechar='"', sep=',')
    df.columns = df.columns.str.strip()  # Strip extra spaces in headers
    df['User'] = df['User'].str.strip()  # Strip spaces in usernames
    usernames = df['User'].dropna().unique()
    return set(usernames)

# === Step 2: Fetch usernames from LDAP ===
def get_ldap_usernames():
    server = Server(LDAP_SERVER, port=LDAP_PORT, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)
    
    conn.search(
        search_base=BASE_DN,
        search_filter=SEARCH_FILTER,
        search_scope=SUBTREE,
        attributes=ATTRIBUTES
    )
    
    ldap_users = set()
    for entry in conn.entries:
        if 'sAMAccountName' in entry:
            ldap_users.add(str(entry.sAMAccountName))
    
    conn.unbind()
    return ldap_users

# === Step 3: Compare and report ===
def compare_users(csv_users, ldap_users):
    only_in_csv = sorted(csv_users - ldap_users)
    only_in_ldap = sorted(ldap_users - csv_users)
    in_both = sorted(csv_users & ldap_users)

    print("\n✅ Users in BOTH LDAP and CSV:")
    print(tabulate([[u] for u in in_both], headers=["Username"], tablefmt="grid"))

    print("\n❌ Users ONLY in VPN CSV:")
    print(tabulate([[u] for u in only_in_csv], headers=["Username"], tablefmt="grid"))

    print("\n⚠️ Users ONLY in LDAP:")
    print(tabulate([[u] for u in only_in_ldap], headers=["Username"], tablefmt="grid"))

# === Step 4: Save comparison results to CSV ===
def save_comparison_to_csv(comparison_data, output_path='user_comparison_report.csv'):
    # Create DataFrames  
    df_ldap_only = pd.DataFrame({'Username': comparison_data['only_in_ldap']})

    # Combine all DataFrames
    combined_df = pd.concat([df_ldap_only])
    
    # Save to CSV
    combined_df.to_csv(output_path, index=False)
    print(f"\n📊 Comparison report saved to: {output_path}")


# === Main logic ===
if __name__ == '__main__':
    csv_path = 'vpn-connections-report.csv'
    csv_users = get_csv_usernames(csv_path)
    ldap_users = get_ldap_usernames()
    comparison_results = compare_users(csv_users, ldap_users)
    save_comparison_to_csv(comparison_results)
