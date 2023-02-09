#!/bin/bash
# exec >> /tmp/salt_nodegrid.out 2>&1

#############################################################################
### NOTICE: this script should be executed with with sudo privilege only. ###
#############################################################################

if [ "$1" != "" ]; then
    TARGET="$1"
else
    echo "Usage: sudo $0 SALT_TARGET_NAME (Only single target is supported)"
    exit 1
fi

# Variables
TIMEOUT=1500
PING_RETRIES=30
UPGRADE_CHECK_RETRIES=150

# File repository
FILE_REPO_PATH="/srv/salt"
FILE_REPO="salt:/"

# Files
NODEGRID_FIRMWARE="Nodegrid_Platform_v5.6.9_20230111.iso"

# File paths
ISO_FILE="$FILE_REPO/$NODEGRID_FIRMWARE"
SYSTEM_TEMPLATE="$FILE_REPO_PATH/template.cli"
SYSTEM_TEMPLATE_PATH="$FILE_REPO/template.cli"

# Settings
NODEGRID_VERSION="5.6.9"
DOCKER_LICENSE=""

# System Template for import_settings_file salt function
setup_import_template(){
    echo "INFO: Now importing template settings..."

    sudo cat >> "$SYSTEM_TEMPLATE" << HEREDOC
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
HEREDOC

    return $?
}

salt_is_desired_version(){
    echo "INFO: Now checking target version against desired version..."
    OUT=$(sudo salt "$TARGET" nodegrid.check_version "$NODEGRID_VERSION")

    CHECK=$(echo "$OUT" | tr "\n" " " | cut -d "-" -f 2 | xargs)
    CUR_VERSION=$(echo "$OUT" | tr "\n" " " | cut -d "-" -f 3 | xargs)
    echo "$OUT"

    if [[ "$CHECK" == "True" ]]; then
        echo "INFO: Nodegrid is on desired version: $NODEGRID_VERSION"
        return 0
    else
        echo "INFO: Nodegrid is NOT on desired version [$NODEGRID_VERSION], current is [$CUR_VERSION] will execute software upgrade..."
        return 1
    fi
}

main(){
    echo "START: Now configuring factory default target [$TARGET]..."

    echo "INFO: Now checking Proxy [$TARGET] pinging it's address, will retry [$PING_RETRIES] times..."
    sudo salt "$TARGET" nodegrid.ping_icmp retries="$PING_RETRIES" wait_secs=2

    echo "INFO: Now changing default password..."
    sudo salt "$TARGET" nodegrid.change_default_password

    # Cross check version for expected version
    if ! salt_is_desired_version; then

        # Transfers ISO to minion, then to target (timeout for large file transfer).
        echo "INFO: Now transferring firmware [$NODEGRID_FIRMWARE] to [$TARGET]..."
        sudo salt "$TARGET" nodegrid.cp_file "$ISO_FILE" /var/sw --timeout "$TIMEOUT"

        echo "INFO: Now sending upgrade software request to [$TARGET] and retrying [$UPGRADE_CHECK_RETRIES] between 5 seconds..."
        sudo salt "$TARGET" nodegrid.software_upgrade image_location=local_system filename="$NODEGRID_FIRMWARE" retries=$UPGRADE_CHECK_RETRIES wait_secs=5 --timeout "$TIMEOUT"

        if ! salt_is_desired_version; then
            echo "ERROR: Software upgrade to desired version failed!" 
            exit 2
        fi

    fi

    # shellcheck disable=SC2181
    if setup_import_template; then
        sudo salt "$TARGET" nodegrid.import_settings_file "$SYSTEM_TEMPLATE_PATH" --timeout "$TIMEOUT"
    else
        echo "ERROR: Could not write template at [$SYSTEM_TEMPLATE]!" 
        exit 3
    fi

    echo "INFO: Adding license: docker license"
    sudo salt "$TARGET" nodegrid.add_license "$DOCKER_LICENSE"

    echo "INFO: Enabling docker service"
    sudo salt "$TARGET" nodegrid.cli "cd /settings/services/; set enable_docker=yes; commit"

    echo "INFO: Run docker hello-world"
    sudo salt "$TARGET" nodegrid.cli_root_shell "docker run hello-world"

    echo "END: Finished configuration."
}

main
exit 0