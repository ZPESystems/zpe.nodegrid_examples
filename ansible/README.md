# Nodegrid Network Infrastructure Automation Examples
This collection of examples, demonstrates the capabilties on Nodegrid OS and variours automation tools and solutions

The current examples concentrate on ansible as automation tool, with an aim to expand to other solutions 

## Requirements
Nodegrid Version: Minimum version 5.6 or higher, recommended 5.6.5 or newer
python package: ttp

## Installation:

### Nodegrid installation
The collection can be installed in to modes on a Nodegrid appliance.
- for individual users, like the admin user, this will require some initial configuration for the user
- for default 'ansible' user, this will enable the use of the Cluster feature to directly manage Nodegrid appliances which are part of teh cluster setup.
This is the recommended setup.

#### Download the examples
- Download the `ansible.zip` file for a full collection including examples or `ansible_collections.zip` for the ansible collections on there own
### Install on Nodegrid 5.6.3 or earlier
#### Configure Ansible user
- Connect to the WebUI as a admin user
- Open the file Manager and navigate to admin_group
- Upload the file `ansible.zip` file into the folder
- Close the File Manager window
- Open a Console connection to Nodegrid
- drop down to the admin user shell with `shell`
- navigate to `/var/local/file_manager/admin_group/` with 
```shell script
cd /var/local/file_manager/admin_group/
```
- extract the zip file with
```shell script
unzip ansible.zip
```
- setup the ansible user and install ssh_key for the ansible user, this will allow a user to connect to teh ansible user via ssh

```
ansible-playbook /var/local/file_manager/admin_group/ansible/artefacts/installation/nodegrid_ansible_user.yml
```

#### Setup the Examples Enviorment
Become ansible user, there are 2 ways:
- locally as admin user run
```
sudo su - ansible
```
- or ssh as ansible user to the nodegrid
```
ssh ansible@nodegrid
```
- install the requirements
```
ansible-playbook /var/local/file_manager/admin_group/ansible/artefacts/installation/nodegrid_install_requirements.yml
```
- run your first playbook - get system facts
```
ansible-playbook /var/local/file_manager/admin_group/ansible/playbooks/get_facts.yml
```
- run your first playbook - set system preferences
```
ansible-playbook /var/local/file_manager/admin_group/ansible/playbooks/set_system_preferences.yml
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



