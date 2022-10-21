# Nodegrid Network Infrastructure Automation Examples
This collection of examples, demonstrates the capabilities on Nodegrid OS and various automation tools and solutions

The current examples concentrate on ansible as automation tool, with an aim to expand to other solutions 

## Requirements
Nodegrid Version: Minimum version 5.6 or higher, recommended 5.6.5 or newer

## Installation:

### Nodegrid installation
The collection can be installed by the default 'admin' user, this will enable the use of the Cluster feature to directly manage Nodegrid appliances which are part of the cluster setup.

#### Download the examples
- Download the repository as a zip for a full collection or use the `git clone` command to clone the full repository

#### Repository downloaded as zip (zpe.nodegrid examples.zip)
- Connect to the WebUI as a admin user
- Open the file Manager and navigate to admin_group
- Upload the file `zpe.nodegrid_examples.zip` file into the folder
- Close the File Manager window
- Open a Console connection to Nodegrid
- Acesse o shell como usuário administrador usando o comando `shell`
- Navigate to `/var/local/file_manager/admin_group/` 
```shell script
cd /var/local/file_manager/admin_group/
```
- extract the zip file with
```shell script
unzip zpe.nodegrid_examples.zip
```
#### Using git clone command
- Connect to the WebUI as a admin user
- Open a Console connection to Nodegrid
- Navigate to `/var/local/file_manager/admin_group/` 
```shell script
cd /var/local/file_manager/admin_group/
```
- Clone de repository
```shell script
git clone https://github.com/ZPESystems/zpe.nodegrid_examples.git
```

### Install on Nodegrid 5.6.3 or latest to configure Ansible user and environment
- install the requirements
```shell script
ansible-playbook /var/local/file_manager/admin_group/zpe.nodegrid_examples/ansible/artifacts/installation/nodegrid_install_requirements.yml
```
- become ansible user
```shell script
sudo su - ansible
```
#### Allow a user to connect to the ansible user via ssh
- It is possible to authorize a user to access the ansible user via ssh by running `authorize_user.yml` playbook. For this, it is necessary to paste the ssh public key of the user in the playbook execution.
```shell script
ansible-playbook /var/local/file_manager/admin_group/ansible/playbooks/authorize_user.yml
```
### Ready to run the first playbook
- run your first playbook - get system facts
```
ansible-playbook /etc/ansible/playbooks/get_facts.yml
```
- run your first playbook - set system preferences
```
ansible-playbook /etc/ansible/playbooks/set_system_preferences.yml
```

- more examples can be found in the playbook folder
```
cd /etc/ansible/playbooks/
```

# Usage
To run playbooks, 
- connect to the Nodegrid as ansible user
- create new playbooks in `/etc/ansible/playbooks/`
- run your playbooks with
```
ansible-playbook /etc/ansible/playbooks/<playbook>
```

- to limit the execution to a specific host run
```
ansible-playbook /etc/ansible/playbooks/<playbook> -limit <host/group name>
```

- To read the detailed README files, more detailed README files are in the specific collection folders.


## Inventory
### Localhost
To run playbooks which configure the Nodegrid no further setup is required. In order to run commands against 
connected device must the local ansible user setup be compleated

### Local
The local inventory can be easly expanded by adding new hosts to the hosts file in inventory folder.
The file is located in `/ansible/ansible/inventory`
### Cluster
A nodegrid which is part of a Cluster can automatically interact with units within the cluster. 
To see all available hosts run the command
```shell script
ansible-inventory --list
```

## Example Playbooks

### Get Nodegrid Device facts 
```
- hosts: all
  gather_facts: false
  collections:
    - zpe.network

  tasks:

    - name: Get Network Facts from Nodegrid
      zpe.network.facts:

    - name: Get Network Facts from Nodegrid
      zpe.system.facts:

    - name: Display ansible_facts
      debug:
        var: ansible_facts
```

### Create/Update Network Connections
```
- hosts: all
  gather_facts: false
  collections:
    - zpe.network

  tasks:
    - name: Configure Ethernet Connection - BACKPLANE0
      zpe.network.connection:
          connection_name: "BACKPLANE0"
          connect_automatically: 'no'
          set_as_primary_connection: 'no'
          enable_lldp: 'yes'
          block_unsolicited_incoming_packets: 'no'
          ethernet_link_mode: 'auto'
          enable_ip_passthrough: 'no'
          ipv4_mode: 'no_ipv4_address'
          ipv4_default_route_metric: '100'
          ipv4_ignore_obtained_default_gateway: 'no'
          ipv4_ignore_obtained_dns_server: 'no'
          ipv6_mode: 'no_ipv6_address'
          ipv6_default_route_metric: '100'
          ipv6_ignore_obtained_default_gateway: 'no'
          ipv6_ignore_obtained_dns_server: 'no'

    - name: Configure Celluar connection
      zpe.network.connection:
        connection_name: "CELLUAR1"
        connection_type: 'mobile_broadband_gsm'
        connect_automatically: 'yes'
        ipv4_mode: 'dhcp'
        ipv6_mode: 'no_ipv6_address'
        enable_ip_passthrough: 'yes'
        ethernet_connection: 'backplane0'
        enable_data_usage_monitoring: 'yes'
        sim_1_apn_configuration: 'automatic'
        sim_1_mtu: 'auto'
        enable_second_sim_card: 'no'
```

### Update System Settings
```
- hosts: all
  gather_facts: false
  collections:
    - zpe.system

  tasks:
  - name: Update System Preferences
    zpe.system.preferences:
        show_hostname_on_webui_header: "yes"
        idle_timeout: "3600"
        enable_banner: "yes"
```
