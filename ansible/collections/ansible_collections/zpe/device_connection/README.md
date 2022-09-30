# zpe.device_connection
zpe.device_connection

# Install the collection
## Manually on a Nodegrid:
- Open a shell 
- Create the folder 'collections' with
`mkdir /var/local/file_manager/admin_group/ansible/collections`
- Copy the collection to into the folder

In fututure versions will we suport direct installtion via ansible-galaxy commands 

#Usage
The collection is designed to connect to target devices though an existing managed device conection.
The collection can be used, to send commands and to retrieve the output. 
The collection implements a basic get_facts implementation, with the aim to retrieve basic details:
like hostname, version and model information



## Examples
### Inventory
For each target device create host entry with the following information
```
ansible_host: <nodegrid_ip>
ansible_user: <nodegrid_username>
ssl_cert_verify: false
target: <device name or port on Nodegrid>
username: <device username>
password: <device password>
target_os: <target os supported values (generic, ios, junos,panos,fortios)>
``` 

- Create a playbook and define a task to configure a network interface
### Get basic device details
This will retrieve basic details from a target device. For the Generic target type, 
this will try to retrive the hostname from the device prompt

```
- hosts: all
  gather_facts: false
  collections:
    - zpe.device_connection

  tasks:
  - name: Get Hostname
    fact:
        target: "{{ target }}"
        username: "{{ username }}"
        password: "{{ password }}"
        target_os: "{{ target_os }}"

  - name: show Ansible_facts
    debug:
      var: ansible_facts
```

### Send Commands to a target device
```
- hosts: all
  gather_facts: false
  collections:
    - zpe.device_connection

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

The `cmds` section can take a wide range of additional parameters to support a wide range of different CLI implementations.
The following addition options are available

- template - define a template file which will be used to parse the output
- cmd_prompt - allows to define a expected prompt for the cmd
- cmd_prompt_match - prompts are matched against the end of line by default. By enabling this option the match will be performed inline
- cmd_timeout - overwrite a specific cmd timeout value in secounds
- cmd_newline - overwrite the default newline character

####cmd Examples
Template
```
        cmds:
          - cmd: 'show version'
            template: junos_show_version
```

Advanced - Fortinet interruption boot process and start a firmware update via TFP
```
              - cmd: execute reboot
                cmd_prompt: "(y/n)"
              - cmd: y                # no return key
                cmd_prompt: "configuration menu..."
                cmd_prompt_match: inline
                cmd_timeout: 60
                cmd_newline: ''
              - cmd: y              # no retrun key
                cmd_prompt: "H:"
                cmd_newline: ''
              - cmd: F              # no retrun key
                cmd_prompt: "[Y/N]?"
                cmd_newline: ''
              - cmd: y              # no retrun key
                cmd_timeout: 360
                cmd_prompt: "H:"
                cmd_newline: ''
              - cmd: G              # no retrun key
                cmd_prompt: "[192.168.1.168]:"
                cmd_newline: ''
              - cmd: "{{ tftp_address }}"
                cmd_prompt: "[192.168.1.188]:"
              - cmd: "{{ local_address }}"
                cmd_prompt: "[image.out]:"
              - cmd: "{{ image_name }}"
                cmd_prompt: "[D/B/R]?"
                cmd_timeout: 360
              - cmd: D            # no retrun key
                cmd_prompt: "login:"
                cmd_timeout: 360
                cmd_newline: '' 
```

For more samples review test cases in the collection Roles or review the documentation.







