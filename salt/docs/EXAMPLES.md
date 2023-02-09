# ZPE Salt Examples

## Configure ZPE Out of Box - Factory Default

> Only a single "salt target" is supported on this example script

### Routines

- Change default password;
- Check current version against desired version
- Upgrade software in case not in desired version
- Apply import_settings
- Add license
- Launch docker container via shell

### Requirements

#1 Factory default Nodegrid unit, configured in pillar file; (check [Nodegrid Proxy Module Configuration](#nodegrid-proxy-module-configuration))

#2 Transfer Nodegrid firmware images to the MASTER salt repository. (default: `/srv/salt/`)

#3 Set script variables:
```python
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
<ADD_TEMPLATE_HERE>
"""
```

### Execution

```bash
sudo python3 examples/scripts/configure_factory_nodegrid.py nodegrid_host
```

### Verification

After proper script setup and execution, the factory default Nodegrid unit should be on the desired firmware version, the configuration template is set up, and a docker container is running or executed.


## Get System Facts
```bash
salt nodegrid_host nodegrid.get_system_about
salt nodegrid_host nodegrid.cli "show /settings/system_preferences"
salt nodegrid_host nodegrid.cli "show /settings/network_connections"
```

## Get and Add Licenses
```bash
salt nodegrid_host nodegrid.cli "show /settings/license"
salt nodegrid_host nodegrid.add_license <ADD_YOUR_LICENSE_HERE>
```

## Send reboot Command
```bash
salt nodegrid_host nodegrid.cli "reboot --force"
```

## Update System Settings using the CLI function
```bash
salt nodegrid_host nodegrid.cli "cd /settings/system_preferences/
set idle_timeout=3600
set enable_banner=yes
commit"
salt nodegrid_host nodegrid.cli "cd /settings/license
add
set license_key=<ADD_YOUR_LICENSE_HERE>
commit"
```

## CLI function using File

The File should contain CLI Commands to be executed on the device.
It should be located at salt-master's file_roots, default: /srv/salt/
For example: /srv/salt/cli/file.cli

File Example:
```bash
cd /settings/system_preferences/
set idle_timeout=3600
set enable_banner=yes
commit
```

CLI Example:
```bash
salt nodegrid_host nodegrid.cli salt://cli/file.cli
```

## Export Settings
```bash
salt nodegrid_host nodegrid.export_settings "/settings/system_preferences"
```

## Import Settings
```bash
salt nodegrid_host nodegrid.import_settings "/settings/system_preferences idle_timeout=3600"
salt nodegrid_host nodegrid.import_settings "/settings/system_preferences idle_timeout=3600
/settings/system_preferences enable_banner=yes
/settings/system_preferences show_hostname_on_webui_header=yes"
```

## Import Settings using File
File with CLI import_settings formatted commands to be imported on the device.
Located at salt-master file_roots, default: /srv/salt/
Example: /srv/salt/cli/file.cli

File Example:
```bash
/settings/system_preferences idle_timeout=3600
/settings/system_preferences enable_banner=yes
/settings/system_preferences show_hostname_on_webui_header=yes
```

CLI Example:
```bash
salt nodegrid_host nodegrid.import_settings_file salt://cli/import.cli
```

## System Backup - Save Settings

Save the backup file locally, the file will be located on the proxied device at `/backup/<FILENAME>`
```bash
salt nodegrid_host nodegrid.save_settings destination=local_system filename=backup.cfg
```

Save backup on Remote Server, FTP server:
```bash
salt nodegrid_host nodegrid.save_settings destination=remote_server url=ftp://10.10.10.1/filepath username=ftpuser password=ftpuser absolute_name=True
```

## System Backup - Apply Settings

Apply Local file backup, the file must be located on the proxied device at  `/backup`
```bash
salt nodegrid_host nodegrid.apply_settings destination=local_system filename=backup.cfg
```

Apply Remote Server backup from the FTP server:
```bash
salt nodegrid_host nodegrid.apply_settings destination=remote_server url=ftp://10.10.10.1/backup.cfg username=ftpuser password=ftpuser
```

## Create/Update Network Connections

Configure Ethernet Connection - BACKPLANE0
```bash
salt nodegrid_host nodegrid.cli "
cd /settings/network_connections
add
set name="BACKPLANE0"
set connect_automatically=no
set set_as_primary_connection=no
set enable_lldp=yes
set block_unsolicited_incoming_packets=no
set ethernet_link_mode=auto
set enable_ip_passthrough=no
set ipv4_mode=no_ipv4_address
set ipv4_default_route_metric=100
set ipv4_ignore_obtained_default_gateway=no
set ipv4_ignore_obtained_dns_server=no
set ipv6_mode=no_ipv6_address
set ipv6_default_route_metric=100
set ipv6_ignore_obtained_default_gateway=no
set ipv6_ignore_obtained_dns_server=no
commit
"
```

Configure Cellular connection:
```bash
salt nodegrid_host nodegrid.cli "cd /settings/network_connections
add
set name="CELLULAR1"
set type=mobile_broadband_gsm
set connect_automatically=yes
set ipv4_mode=dhcp
set ipv6_mode=no_ipv6_address
set enable_ip_passthrough=no
set enable_data_usage_monitoring=yes
set sim-1_apn_configuration=automatic
set sim-1_mtu=auto
set enable_second_sim_card=no
commit
"
```

## Software Upgrade

Transfer firmware from file repo (/srv/salt/) to target.
Then, send a local upgrade request to the target.

```bash
salt '*' nodegrid.cp_file salt://Nodegrid_Platform_v5.6.9_20230111.iso /var/sw/ --timeout 900
salt '*' nodegrid.software_upgrade image_location=local_system filename=Nodegrid_Platform_v5.6.9_20230111.iso --timeout 60
```

## Add Firewall Rules

```bash
salt nodegrid_host nodegrid.import_settings "
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
"
```

## Add Wireguard Interface

```bash
salt nodegrid_host nodegrid.import_settings "
/settings/wireguard/Test/interfaces interface_name=Test
/settings/wireguard/Test/interfaces interface_type=server
/settings/wireguard/Test/interfaces status=enabled
/settings/wireguard/Test/interfaces internal_address=10.10.10.1
/settings/wireguard/Test/interfaces listening_port=51820
/settings/wireguard/Test/interfaces keypair=input_manually
/settings/wireguard/Test/interfaces private_key=********
/settings/wireguard/Test/interfaces public_key=hM7nBUDtdzmFhWf0jU2KsoPLGjiER4EIUim+AMWaRyo=
/settings/wireguard/Test/interfaces routing_rules=create_routing_rules_on_default_routing_tables
"
```

## Add Wireguard Peers

```bash
salt nodegrid_host nodegrid.import_settings "
/settings/wireguard/Test/peers/Peer1 peer_name=Peer1
/settings/wireguard/Test/peers/Peer1 allowed_ips=10.10.10.1
/settings/wireguard/Test/peers/Peer1 public_key=khwSfe7TT9W6axkFdSeO3Uym4bZ/Um44NOzkfIFr91Y=
```
