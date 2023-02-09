import salt.client
import sys
from pprint import pprint

SALT_API = salt.client.LocalClient()

# Only single target is supported
if len(sys.argv) > 1:
    TARGET = sys.argv[1]
else:
    print(f"Usage: sudo {sys.argv[0]} SALT_TARGET_NAME (Only single target is supported)")
    sys.exit(-1)

# Variables
TIMEOUT = 1500
PING_RETRIES = 30
UPGRADE_CHECK_RETRIES = 150

# File repository
FILE_REPO_PATH = "/srv/salt"
FILE_REPO = "salt:/"

# Files
NODEGRID_FIRMWARE = "Nodegrid_Platform_v5.6.9_20230111.iso"

# File paths
ISO_FILE = f"{FILE_REPO}/{NODEGRID_FIRMWARE}"

# Settings
NODEGRID_VERSION = "5.6.9"
DOCKER_LICENSE = "<ADD_YOUR_LICENSE_HERE>"
SYSTEM_TEMPLATE_CONTENTS = """
# Update system_preferences
/settings/system_preferences idle_timeout=3600
/settings/system_preferences show_hostname_on_webui_header=yes
/settings/system_preferences enable_banner=yes

# Configure date_time
/settings/date_and_time date_and_time=network_time_protocol
/settings/date_and_time server=pool.ntp.org
/settings/date_and_time zone=utc

# Add local user group
/settings/authorization/group_name/profile shell_access=yes
/settings/authorization/group_name/profile sudo_permission=yes
/settings/authorization/group_name/profile startup_application=cli

# Add local user
/settings/local_accounts/user_name username=user_name
/settings/local_accounts/user_name account_type=regular_account
/settings/local_accounts/user_name password=user_name
/settings/local_accounts/user_name hash_format_password=no
/settings/local_accounts/user_name password_change_at_login=no
/settings/local_accounts/user_name user_group=admin,group_name

# Add auth servers
/settings/authentication/servers/1 method=ldap_or_ad
/settings/authentication/servers/1 status=enabled
/settings/authentication/servers/1 fallback_if_denied_access=yes
/settings/authentication/servers/1 remote_server=192.168.2.88
/settings/authentication/servers/1 authorize_ssh_pkey_users=yes
/settings/authentication/servers/1 ldap_ad_base=dc=zpe,dc=net
/settings/authentication/servers/1 ldap_ad_secure=off
/settings/authentication/servers/1 ldap_port=default
/settings/authentication/servers/1 ldap_ad_database_username=cn=admin,dc=zpe,dc=net
/settings/authentication/servers/1 ldap_ad_database_password=administrator
/settings/authentication/servers/1 ldap_ad_group_attribute=memberUid
/settings/authentication/servers/1 search_nested_groups=no
/settings/authentication/servers/1 enable_ad_referrals=yes
/settings/authentication/servers/2 2-factor_authentication=none
/settings/authentication/servers/2 status=enabled
/settings/authentication/servers/2 apply_2-factor_auth_for_admin_and_root_users=no

# Add network connections
/settings/network_connections/BACKPLANE0 name=BACKPLANE0
/settings/network_connections/BACKPLANE0 type=ethernet
/settings/network_connections/BACKPLANE0 ethernet_interface=eth0
/settings/network_connections/BACKPLANE0 connect_automatically=no
/settings/network_connections/BACKPLANE0 set_as_primary_connection=no
/settings/network_connections/BACKPLANE0 enable_lldp=no
/settings/network_connections/BACKPLANE0 block_unsolicited_incoming_packets=no
/settings/network_connections/BACKPLANE0 ethernet_link_mode=auto
/settings/network_connections/BACKPLANE0 enable_ip_passthrough=no
/settings/network_connections/BACKPLANE0 ipv4_mode=no_ipv4_address
/settings/network_connections/BACKPLANE0 ipv4_default_route_metric=100
/settings/network_connections/BACKPLANE0 ipv4_ignore_obtained_default_gateway=no
/settings/network_connections/BACKPLANE0 ipv4_ignore_obtained_dns_server=no
/settings/network_connections/BACKPLANE0 ipv6_mode=no_ipv6_address
/settings/network_connections/BACKPLANE0 ipv6_default_route_metric=100
/settings/network_connections/BACKPLANE0 ipv6_ignore_obtained_default_gateway=no
/settings/network_connections/BACKPLANE0 ipv6_ignore_obtained_dns_server=no

# Add firewall rules
/settings/ipv4_firewall/chains/INPUT/1 description="Client Rules - SSH"
/settings/ipv4_firewall/chains/INPUT/1 protocol=tcp
/settings/ipv4_firewall/chains/INPUT/1 destination_port=22
/settings/ipv4_firewall/chains/INPUT/2 description="Client Rules - ICMP"
/settings/ipv4_firewall/chains/INPUT/2 protocol_number=1
/settings/ipv4_firewall/chains/OUTPUT/1 description="Feature Rules - LDAP"
/settings/ipv4_firewall/chains/OUTPUT/1 protocol=tcp
/settings/ipv4_firewall/chains/OUTPUT/1 source_port=389
/settings/ipv4_firewall/chains/OUTPUT/2 description="Feature Rules - LDAPS"
/settings/ipv4_firewall/chains/OUTPUT/2 protocol=tcp
/settings/ipv4_firewall/chains/OUTPUT/2 source_port=636

# Add wireguard Interface
/settings/wireguard/Test/interfaces interface_name=Test
/settings/wireguard/Test/interfaces interface_type=server
/settings/wireguard/Test/interfaces status=enabled
/settings/wireguard/Test/interfaces internal_address=10.10.10.1
/settings/wireguard/Test/interfaces listening_port=51820
/settings/wireguard/Test/interfaces keypair=input_manually
/settings/wireguard/Test/interfaces private_key=********
/settings/wireguard/Test/interfaces public_key=hM7nBUDtdzmFhWf0jU2KsoPLGjiER4EIUim+AMWaRyo=
/settings/wireguard/Test/interfaces routing_rules=create_routing_rules_on_default_routing_tables

# Add wireguard Peers
/settings/wireguard/Test/peers/Peer1 peer_name=Peer1
/settings/wireguard/Test/peers/Peer1 allowed_ips=10.10.10.1
/settings/wireguard/Test/peers/Peer1 public_key=khwSfe7TT9W6axkFdSeO3Uym4bZ/Um44NOzkfIFr91Y=
"""

def pprint_output(context, output):
    print(context)
    pprint(output)


def ping_icmp():
    print(f"\nINFO: Now checking Proxy {TARGET} pinging it's address, will retry {PING_RETRIES} times...")
    icmp_opts = {
        "retries": PING_RETRIES,
        "wait_secs": 2
    }
    output = SALT_API.cmd(TARGET, 'nodegrid.ping_icmp', kwarg=icmp_opts)
    pprint_output(f"nodegrid.ping_icmp", output)
    if "False" in str(output):
        print("ERROR: Could not reach target!")
        sys.exit(1)


def change_default_password():
    print("\nINFO: Now changing default password...")
    output = SALT_API.cmd(TARGET, 'nodegrid.change_default_password')
    pprint_output(f"nodegrid.change_default_password", output)
    if "False" in str(output) or "Timeout" in str(output):
        print("ERROR: Could not change target default password!")
        sys.exit(2)


def is_desired_version():
    print("\nINFO: Now checking target version against desired version...")
    status = False
    cur_version = "Unknown"

    output = SALT_API.cmd(TARGET, 'nodegrid.check_version', [NODEGRID_VERSION])
    pprint_output(f"nodegrid.check_version {NODEGRID_VERSION}", output)
    check = output[TARGET]
    if check and len(check) > 1:
        status = check[0]
        cur_version = check[1]

    if status:
        print(f"\nINFO: Nodegrid is on desired version: {NODEGRID_VERSION}")
    else:
        print(f"\nINFO: Nodegrid is NOT on desired version {NODEGRID_VERSION}, current is {cur_version} will execute software upgrade...")
        status = False

    return status


def cp_file():
    # Transfers ISO to minion, then to target (timeout for large file transfer).
    print(f"\nINFO: Now transferring firmware {NODEGRID_FIRMWARE} to {TARGET}...")
    output = SALT_API.cmd(TARGET, 'nodegrid.cp_file', [ISO_FILE, '/var/sw/'], timeout=TIMEOUT)
    pprint_output(f"nodegrid.cp_file [{ISO_FILE}, '/var/sw/']", output)
    if "False" in str(output):
        print("ERROR: Could not send firmware to target!")
        sys.exit(3)


def upgrade_sofware():
    print(f"\nINFO: Now sending upgrade software request to {TARGET} and retrying [{UPGRADE_CHECK_RETRIES}] times in between 5 seconds...")
    upgrade_opts = {
        "image_location": "local_system",
        "filename": NODEGRID_FIRMWARE,
        "retries": UPGRADE_CHECK_RETRIES,
        "wait_secs": 5
    }
    output = SALT_API.cmd(TARGET, 'nodegrid.software_upgrade', kwarg=upgrade_opts, timeout=TIMEOUT)
    pprint_output(f"nodegrid.software_upgrade [{ISO_FILE}, '/var/sw/']", output)
    if "False" in str(output):
        print("ERROR: Could not complete firmware upgrade to target!")
        sys.exit(4)
    if "Minion did not return" in str(output):
        print("ERROR: Could not verify firmware upgrade to target!")
        sys.exit(5)


def main():
    print(f"START: Now configuring factory default target {TARGET}...")

    ping_icmp()

    change_default_password()

    # Cross check version for desired version
    if not is_desired_version():

        cp_file()
        upgrade_sofware()

        if not is_desired_version():
            print("ERROR: Software upgrade to desired version failed!")
            sys.exit(6)

    print("\nINFO: Now importing template settings...")
    output = SALT_API.cmd(TARGET, 'nodegrid.import_settings', [SYSTEM_TEMPLATE_CONTENTS], timeout=TIMEOUT)
    pprint_output(f"nodegrid.import_settings", output)
    if "Error" in str(output) or "False" in str(output):
        print("ERROR: Import settings has errors, please check.")

    print("\nINFO: Adding license: docker license")
    output = SALT_API.cmd(TARGET, 'nodegrid.add_license', [DOCKER_LICENSE])
    pprint_output(f"nodegrid.add_license [{DOCKER_LICENSE}]", output)
    if "Error" in str(output):
        print("ERROR: Add Licences has errors, please check.")

    print("\nINFO: Enabling docker service")
    output = SALT_API.cmd(TARGET, 'nodegrid.cli', ['cd /settings/services/; set enable_docker=yes; commit'])
    pprint_output(f"nodegrid.cli ['cd /settings/services/; set enable_docker=yes; commit']", output)
    if "Error" in str(output):
        print("ERROR: Add Licences has errors, please check.")

    print("\nINFO: Run docker hello-world")
    output = SALT_API.cmd(TARGET, 'nodegrid.cli_root_shell', ['docker run hello-world'])
    pprint_output(f"nodegrid.cli_root_shell ['docker run hello-world']", output)
    if "Error" in str(output):
        print("ERROR: Add Licences has errors, please check.")

    print("END: Finished configuration.")

main()
sys.exit(0)
