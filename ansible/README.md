# Nodegrid Network Infrastructure Automation Examples
This collection of examples demonstrates the capabilities of Nodegrid OS and various automation tools and solutions

The current examples concentrate on ansible as an automation tool, intending to expand to other solutions. 

## Requirements
Nodegrid Version: Minimum version 5.6 or higher, recommended 5.6.5 or newer
python package: ttp

## Installation:

### Nodegrid installation
The user can install the collection in two modes on a Nodegrid appliance.
- for individual users, like the admin user, this will require some initial configuration for the user
- for the default 'ansible' user, this will enable the use of the Cluster feature to directly manage Nodegrid appliances, which are part of the cluster setup. [Recommended]

#### Download the examples
- Download the `ansible.zip` file for a full collection, including examples or `ansible_collections.zip` for the ansible collections on their own

### Install on Nodegrid 5.6.3 or earlier
#### Configure Ansible user
- Connect to the WebUI as an admin user
- Open the File Manager and navigate to admin_group
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
- setup the ansible user and install ssh_key for the ansible user; this will allow a user to connect to the ansible user via ssh

```
ansible-playbook /var/local/file_manager/admin_group/ansible/artefacts/installation/nodegrid_ansible_user.yml
```

#### Setup the Examples Environment
To become the "ansible" user, there are two ways:
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
### First Playbooks
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
To run commands against connected devices, must the local ansible user setup be compleated

### Local
The local inventory can be easily expanded by adding new hosts to the "hosts" file in the inventory folder.
The file is located in `/ansible/ansible/inventory`
### Cluster
A nodegrid, part of a Cluster, can automatically interact with units within the cluster. 
To see all available hosts run the command
```shell script
ansible-inventory --list
```

## Example Playbooks
Following is a range of example playbooks, which can be used. More examples can be found in the folder "playbooks".
The folder tfd26, contains examples which have been presented as part of Tech Field Day 26.


### Generic Examples
#### Run any CLI command on an example to get a Device Outlet status
```
- hosts: all
  gather_facts: false
  collections:
    - zpe.system
  var:
    device_name: DEVICE_NAME

  tasks:
    - name: Get outlet status for a device
      zpe.system.nodegrid_cmds:
        cmds:
          - cmd: 'cd /access/{{ device_name }}'
          - cmd: 'outlet_status'
      register: output

    - name: Display Outlet Status
      debug:
        var: output
```


#### Import any data into Nodegrid using import_settings commands
```
- hosts: all
  gather_facts: false
  collections:
    - zpe.system

  tasks:
  - name: Update zpecloud.com details on Nodegrid using import_settings
    zpe.system.nodegrid_import:
       cmds:
        - "/settings/zpe_cloud enable_zpe_cloud=yes"
        - "/settings/zpe_cloud enable_remote_access=yes"
        - "/settings/zpe_cloud enable_file_protection=no"
        - "/settings/zpe_cloud enable_file_encryption=no"
```


#### Import settings via a file
```
- name: Import Settings from import_settings file
  hosts: all
  var:
    import_settings_file: /etc/ansible/templates/settings.j2

  tasks:
    - name: Import settings file
      template:
        src: "{{ import_settings_file }}"
        dest: /tmp/import_settings.cli

    - name: import settings
      command: cli -c "import_settings --file /tmp/import_settings.cli"
      register: output

    - name: response
      debug:
        msg:
          - "stdout: {{ output.stdout }}"
          - "stderr: {{ output.stderr }}"
```


### Get Nodegrid facts 
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

### Configure Nodegrid
#### Create/Update Network Connections
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


#### Update System Settings
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

### Interact with managed devices
#### Run show version on a device, playbook will prompt for details
```
- hosts: all
  gather_facts: false
  collections:
    - zpe.device_connection
  vars_prompt:
      - name: target
        prompt: Enter target name, either ttyS or current device name
      - name: username
        prompt: Enter username
      - name: password
        prompt: Enter target password
      - name: target
        prompt: Enter target_os [generic, ios, junos,panos,fortios]
        default: generic

  tasks:
  - name: Run commands
    run_command:
        target: "{{ target }}"
        username: "{{ username }}"
        password: "{{ password }}"
        target_os: "{{ target_os }}"
        cmds:
          - 'show version'
    register: cmds_output

  - name: Print command results
    debug:
      var: cmds_output
``` 

#### Run a cmd (show system interface) on a device (Fortinet) and parse the output to ansible_facts
Nodegrid supports Template Text Parser (https://ttp.readthedocs.io/en/latest/) for parsing
```
- hosts: all
  gather_facts: false
  collections:
    - zpe.device_connection
  var:
    template_location: ./template

  tasks:
    - name: Run command on a device
      run_command:
        target: "{{ target }}"
        username: "{{ username }}"
        password: "{{ password }}"
        target_os: "{{ target_os }}"
        cmds:
            - cmd: 'show system interface internal'
              template: fortinet_show_system_interface
              template_paths:
                - '{{ template_location }}'
      register: cmds_output

    - name: Show
      debug:
        var: cmds_output
```

