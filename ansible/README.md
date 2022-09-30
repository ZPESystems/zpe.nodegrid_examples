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
- ssh as ansible user to the nodegrid
```
ssh ansible@nodegrid
```
- extract collection
```
unzip ansible.zip
```
- navigate into the new folder
```
cd ./ansible/
```
- setup the user enviorment
```
ansible-playbook ./artefacts/installation/nodegrid_install_requirements.yml
```

- run your first playbook 
```
ansible-playbook get_facts.yml
```

- more examples can be found in the folder


#Usage
To run playbooks, 
- connect to the Nodegrid as ansible user
- move to the ansible folder
```
cd /home/ansible/ansible
```
- create you playbooks in this folder
- run your playbooks with
```
ansible-playbook <playbook>
```

- to limit the execution to a specific host run
```
ansible-playbook <playbook> -limit <host/group name>
```

- To read the detailed README files, more detailed README files are in the specific collection folders.


##Inventory
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









