# Nodegrid Salt Proxy Module

- [Nodegrid Salt Proxy Module](#nodegrid-salt-proxy-module)
- [Pillar](#pillar)
- [Nodegrid Proxy Module Available Functions](#nodegrid-proxy-module-available-functions)
- [Nodegrid Proxy Module Installation](#nodegrid-proxy-module-installation)
  - [ZPE Salt Installation Guide](#zpe-salt-installation-guide)
  - [Dependencies](#dependencies)
    - [python-pexpect](#python-pexpect)
  - [Module Install on a Salt Installation](#module-install-on-a-salt-installation)
  - [Nodegrid Proxy Module Configuration](#nodegrid-proxy-module-configuration)
    - [Step 1: On MASTER: Configure and Run master](#step-1-on-master-configure-and-run-master)
    - [On SALT-PROXY: Configure and Run](#on-salt-proxy-configure-and-run)
    - [On SALT-MASTER: Accept Minion key](#on-salt-master-accept-minion-key)
    - [On SALT-PROXY: Run](#on-salt-proxy-run)
    - [On SALT-MASTER: Accept keys](#on-salt-master-accept-keys)
- [Salt CLI syntax](#salt-cli-syntax)
  - [Output example](#output-example)
- [ZPE Salt Examples](#zpe-salt-examples)
  - [Configure ZPE Out of Box - Factory Default](#configure-zpe-out-of-box---factory-default)
    - [Routines](#routines)
    - [Requirements](#requirements)
    - [Execution](#execution)
    - [Verification](#verification)
  - [Get System Facts](#get-system-facts)
  - [Get and Add Licenses](#get-and-add-licenses)
  - [Send reboot Command](#send-reboot-command)
  - [Update System Settings using the CLI function](#update-system-settings-using-the-cli-function)
  - [CLI function using File](#cli-function-using-file)
  - [Export Settings](#export-settings)
  - [Import Settings](#import-settings)
  - [Import Settings using File](#import-settings-using-file)
  - [System Backup - Save Settings](#system-backup---save-settings)
  - [System Backup - Apply Settings](#system-backup---apply-settings)
  - [Create/Update Network Connections](#createupdate-network-connections)
  - [Software Upgrade](#software-upgrade)
  - [Add Firewall Rules](#add-firewall-rules)
  - [Add Wireguard Interface](#add-wireguard-interface)
  - [Add Wireguard Peers](#add-wireguard-peers)
- [Salt installation on Nodegrid OS using IPKs](#salt-installation-on-nodegrid-os-using-ipks)
- [Salt installation on Ubuntu](#salt-installation-on-ubuntu)


This repository Proxy Minion interface module for managing ZPE's Nodegrid OS hosts.

This proxy minion enables Nodegrid OS hosts to be treated individually like a Salt Minion.

Salt's "Proxy Minion" functionality enables you to designate another machine to host a minion process that "proxies" communication from the Salt Master. The master does not know nor care that the target is not a "real" Salt Minion.

More in-depth conceptual reading on [Proxy Minions](https://docs.saltproject.io/en/latest/topics/proxyminion/index.html#proxy-minion) can be found in the Proxy Minion section of Salt's documentation.

> This module depends on a pre-installed Salt environment - [Salt Installation documentation](https://docs.saltproject.io/en/latest/topics/installation/index.html)

# Pillar

Proxy minions get their configuration from Salt's Pillar. Every proxy must have an instance in the Pillar file and a reference in the Pillar top file that matches the proxy ID.

At a minimum for communication with the Nodegrid host, the pillar should look like this:
```
proxy:
  proxytype: nodegrid
  host: <ip or hostname of nodegrid host>
  username: <nodegrid administrator username>
  password: <password>
```

# Nodegrid Proxy Module Available Functions

Please check the following documentation for functions specifications:
- [salt.proxy.nodegrid](docs/FUNCTIONS.md)


# Nodegrid Proxy Module Installation

To continue on this section, a Salt installation is necessary.
More information can be found in the official [Installation](https://docs.saltproject.io/en/latest/topics/installation/index.html) section of Salt's documentation.

## ZPE Salt Installation Guide

If you don't have an environment yet, please check this guide prepared for Ubuntu and Nodegrid OS below:
- [Salt installation on Ubuntu](#salt-installation-on-ubuntu)
- [Salt installation on Nodegrid OS using Docker](#salt-installation-on-nodegrid-os-using-docker)
- [Salt installation on Nodegrid OS using IPKs](#salt-installation-on-nodegrid-os-using-ipks)

## Dependencies

- python-pexpect

### python-pexpect
python-pexpect can be installed via pip:

`$ pip install python-pexpect`


## Module Install on a Salt Installation

On the SALT MASTER, connect to SSH and go to shell.

Create folder to modules installation, default is `/srv/salt/`:
```
sudo mkdir -p /srv/salt/_proxy
sudo mkdir -p /srv/salt/_modules
```

Clone the example repository and install:
```
git clone https://github.com/ZPESystems/zpe.nodegrid_examples.git
cd zpe.nodegrid_examples/salt
sudo cp salt/proxy/nodegrid.py /srv/salt/_proxy/
sudo cp salt/modules/nodegrid.py /srv/salt/_modules/
```

## Nodegrid Proxy Module Configuration

INTRO - use case
DIAGRAM

### Step 1: On MASTER: Configure and Run master
For each **file** add the following **contents**.

Edit the '/etc/salt/master' file to include the path to the file repository and pillar:
```
file_roots:
  base:
    - /srv/salt/
pillar_roots:
  base:
    - /srv/pillar
```

Create a pillar directory for the pillar files configuration:
```
sudo mkdir -p /srv/pillar
```

In '/srv/pillar/top.sls' map the devices details with the proxy name:
```
base:
  'nodegrid_host':
    - nodegrid_host
  'nodegrid_host2':
    - nodegrid_host2
```

In '/srv/pillar/nodegrid_host.sls' and '/srv/pillar/nodegrid_host2.sls' map the device details with the proxy name:
```
proxy:
  proxytype: nodegrid
  host: <ip or fqdn name of nodegrid host>
  username: <nodegrid administrator username>
  password: <password>
```

Run the SALT MASTER via the following command:
```
sudo salt-master -d --log-file /var/log/salt-master.log --log-file-level=debug -d
```

After storing the device information in the pillar on MASTER, now, configure the PROXY.

### On SALT-PROXY: Configure and Run
For each **file** add the following **contents**.

Create or edit the file '/etc/salt/proxy' to configure MASTER address:
```
master: <ip or hostname of salt-master>
multiprocessing: False # IMPORTANT
```

Configure minion '/etc/salt/minion', this is needed for proxy usage:
```
id: salt-minion
master: <ip or hostname of salt-master>
multiprocessing: False # IMPORTANT
```

Run the salt minion first, via the following command:
```shell script
sudo salt-minion --log-file /var/log/salt-minion.log -d
```

### On SALT-MASTER: Accept Minion key

Accept plain minion key:
```shell script
sudo salt-key -a salt-minion -y
```

Test minion communication using test ping:
```shell script
sudo salt salt-minion test.ping
salt-minion:
    True
```

Install dependencies on the minion environment:
```shell script
sudo salt salt-minion pip.install pexpect
```

Sync the newly installed module using the commands below:
```shell script
sudo salt salt-minion saltutil.sync_modules
sudo salt salt-minion saltutil.sync_proxymodules
```

### On SALT-PROXY: Run

Run the salt proxy via the following command
```
sudo salt-proxy --proxyid=nodegrid_host --log-file /var/log/proxy-nodegrid_host.log --log-file-level=debug -d

sudo salt-proxy --proxyid=nodegrid_host2 --log-file /var/log/proxy-nodegrid_host2.log --log-file-level=debug -d
```

### On SALT-MASTER: Accept keys
Yes, now on MASTER again. This is due to security reasons.

For each proxy process, accept the minion key.

Example: accept the key of all the proxies that start with the name nodegrid_host:
```
sudo salt-key -L
Accepted Keys:
Denied Keys:
Unaccepted Keys:
nodegrid_host
nodegrid_host2
Rejected Keys:
sudo salt-key -a nodegrid_host* -y
The following keys are going to be accepted:
Unaccepted Keys:
nodegrid_host
nodegrid_host2
Key for minion nodegrid_host accepted.
Key for minion nodegrid_host2 accepted.
```

To test your salt configuration, use the ping function to show the proxy connectivity status:
```
sudo salt nodegrid_host* nodegrid.ping
nodegrid_host:
    True
nodegrid_host2:
    True
```

# Salt CLI syntax
**Target**: Select the devices to run the command. (Note: [Targeting can be complex](https://docs.saltstack.com/en/latest/topics/targeting/))

**Module**: nodegrid or [others](https://docs.saltproject.io/en/latest/ref/proxy/all/index.html)

**Function**: ping, cli, get_system_about and [more...](docs/FUNCTIONS.md)

**Arguments**: for instance, a CLI command for the cli function
```
# salt <target> <module>.<function> [<arguments>]
sudo salt '*' nodegrid.cli "show /settings/license"
```

## Output example
```
sudo salt nodegrid_host* nodegrid.get_system_about
nodegrid_host:
    system: Nodegrid Manager
    licenses: 1000
    software: v5.6.3 (Aug 24 2022 - 11:59:15)
    cpu: Intel(R) Xeon(R) CPU E5-2698 v4 @ 2.20GHz
    cpu_cores: 1
    bogomips_per_core: 4394.90
    serial_number: 2F0E9B837ECF
    uptime: 1 days,  23 hours,  25 minutes
    boot mode: Legacy
    secure boot: Disabled
    model: VMware Virtual Platform
    revision tag: r1
nodegrid_host2:
    system: Nodegrid Manager
    licenses: 1000
    software: v5.8.2 (Dec 6 2022 - 08:59:05)
    cpu: Intel(R) Xeon(R) CPU E5-2698 v4 @ 2.20GHz
    cpu_cores: 1
    bogomips_per_core: 4394.90
    serial_number: ac5a3642f2873a4d2ef72916cee847bf
    uptime: 10 days,  0 hours,  31 minutes
    boot mode: Legacy
    secure boot: Disabled
    model: VMware Virtual Platform
    revision tag: r1
```

# ZPE Salt Examples

## Configure ZPE Out of Box - Factory Default

> Only a single "salt target" is supported on the examples scripts below.

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
```bash
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
DOCKER_LICENSE="<ADD_YOUR_LICENSE_HERE>"
# System Template for import_settings
```

### Execution

Bash script without error handling:
```bash
sudo chmod +x examples/configure_factory_nodegrid.sh
sudo bash examples/configure_factory_nodegrid.sh nodegrid_host
```

Python script with error handling:
```bash
sudo python3 examples/configure_factory_nodegrid.py nodegrid_host
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


# Salt installation on Nodegrid OS using IPKs
To use this Nodegrid module you need two Nodegrid hosts to setup salt-master and 
salt-proxy accordingly.

1. Download the IPK files for your Nodegrid OS version [here](https://zpesystems.atlassian.net/wiki/spaces/ENG/pages/1414135885/Using+Saltstack+on+Nodegrid) (permission required).

2. (For both hosts) Connect to the WebUI as an admin user to the Nodegrid appliance
- Connect to the WebUI as an admin user
- Open the file Manager and navigate to admin_group
- Upload the IPKs tar file zpe.nodegrid_salt_ipks.zip file into the folder
- Close the File Manager window
1. Open a Console connection to Nodegrid
- Access the shell as an admin user using the shell command
- Navigate to /var/local/file_manager/admin_group/
```shell script
shell
cd /var/local/file_manager/admin_group/
```
- Extract the zip file with
```shell script
unzip zpe.nodegrid_salt_ipks.zip
```
- Install on IPKs on Nodegrid
```shell script
sudo mount -o remount,rw /;
```
```shell script
sudo opkg install /var/local/file_manager/admin_group/zpe.nodegrid_salt_ipks/*.ipk
```

Done, now follow the instructions in this section:   - [Module Installation for Existing Salt Installation](#module-installation-for-existing-salt-installation)

# Salt installation on Ubuntu
To use this Nodegrid module you need two Ubuntu hosts to set up salt-master and salt-proxy accordingly.

1. For the ubuntu MASTER instance, connect to SSH and execute:
```shell script
sudo apt-get install salt-master
sudo systemctl stop salt-master
```

2. For the ubuntu PROXY instance, connect to SSH and execute:
```shell script
sudo apt-get install salt-minion
sudo systemctl stop salt-minion
```

Done, now follow the instructions in this section:   - [Module Installation for Existing Salt Installation](#module-installation-for-existing-salt-installation)