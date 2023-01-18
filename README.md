# zpe.nodegrid_examples
This repository contains automation examples and libraries which can be used with Nodegrid OS. The repository aims to help customers to get started on the automation journey with Nodegrid OS. We invite customers to provide feedback and suggestions on examples that can be added in the future.

It is recommended to use the latest Nodegrid OS version (5.8.1 or higher) with the examples.

# 1. Getting Started - Using the build-in ansible features
## 1.1. Installation of examples
### 1.1.1. Nodegrid instance with Internet access
#### 1.1.1.1 Download the examples
- Connect to the WebUI or SSH as admin user to the Nodegrid appliance 
- WebUI only: Open a Console connection to Nodegrid
- go to the root shell
```
shell
```
- Navigate to `/var/local/file_manager/admin_group/` folder
```shell script
cd /var/local/file_manager/admin_group/
```
- Clone the example repository
```shell script
git clone https://github.com/ZPESystems/zpe.nodegrid_examples.git
```
#### 1.1.1.2 Install the examples
- install requirements in the existing admin shell session
```shell script
ansible-playbook /var/local/file_manager/admin_group/zpe.nodegrid_examples/ansible/artifacts/installation/nodegrid_install_requirements.yml
```
#### 1.1.1.3 [Optional] Allow a user to connect to the ansible user via ssh
- It is possible to authorize a user to access the ansible user via ssh by running `authorize_user.yml` playbook. For this, it is necessary to paste the ssh public key of the user in the playbook execution.
```shell script
ansible-playbook /var/local/file_manager/admin_group/ansible/playbooks/authorize_user.yml
```
### 1.1.2 Nodegrid instance without Internet access
#### 1.1.2.1 Download the examples
Download the Example from GitHub as zip file, by clicking on 'Code' and Select 'Download ZIP'
- Connect to the Nodegrid appliance the WebUI
- From the Access page open the 'File Manager' and navigate to the admin_group folder
- Upload the downloaded zip file
- Open a Console connection to Nodegrid or SSH to the unit
- go to the root shell
```
shell
```
- Navigate to `/var/local/file_manager/admin_group/` folder
```shell script
cd /var/local/file_manager/admin_group/
```
- Extract the zip file with
```shell script
unzip <file name>
```
#### 1.1.2.2 Install the examples
- install requirements in the existing admin shell session
```shell script
ansible-playbook /var/local/file_manager/admin_group/zpe.nodegrid_examples/ansible/artifacts/installation/nodegrid_install_requirements.yml
```
#### 1.1.2.3 [Optional] Allow a user to connect to the ansible user via ssh
- It is possible to authorize a user to access the ansible user via ssh by running `authorize_user.yml` playbook. For this, it is necessary to paste the ssh public key of the user in the playbook execution.
```shell script
ansible-playbook /var/local/file_manager/admin_group/ansible/playbooks/authorize_user.yml
```

## 1.2. Ready to run the first playbook
### 1.2.1 Activate Central Management
"Central Management" is a new feature that enables administrators to execute, schedule, and manage automation tasks for the local host or all appliances which are part of a Cluster.
Note: This feature is only available in version 5.8 or later
- In the WebUI navigate to Cluster -> Settings
- Activate the 'Enable Cluster' option. If the unit is already part of Cluster, then no further steps are required.
- Provide as a preshared key the value 'nodegrid' (or any other preshared key value) and click on save

#### 1.2.2 Run your first playbook
- Navigate to System > Central Management -> Inventory
- Select 'localhost' and click on run
- From the drop-down select the example playbook 'set_system_preferences.yml' and click on Run again
- The playbook will update the following settings under System -> Preferences:
    - show_hostname_on_webui_header: "yes"
    - idle_timeout: "3600"
    - enable_banner: "yes"
    - revision_tag: 'Ansible_Playbook-set_system_preferences.yml'
 -To review if the playbook was successful, inspect the automation logs under Logs

To explore the other examples and explanations of what they provide navigate to: https://github.com/ZPESystems/zpe.nodegrid_examples/tree/main/ansible

New playbooks can be uploaded under System -> General Management -> Playbooks


