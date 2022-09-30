# Install the collection
## Manually on a Nodegrid:
- Open a shell 
- Create the folder 'collections' with
`mkdir /var/local/file_manager/admin_group/collections`
- Copy the collection to into the folder

In fututure versions will we suport direct installtion via ansible-galaxy commands 

#Usage
The collection is designed to apply a full configuration and currently dose not support induvidial configuration changes.
Configurations Options which are not defined, will be reset to default values.

The collection supports ansible check_mode, and diff mode. 
In check_mode no changes are performed, but the playbook will indicate if a change would be required
In diff mode, the playbook with display the performed changes. Both modes can be combined.

## Examples
- Create a playbook and define a task to configure a network interface
### Update Date and Time Settings
```
- name: Update Date and Time
  zpe.system.date_and_time:
      date_and_time: "network_time_protocol"
      server: "pool.ntp.org"
      zone: "utc"
      enable_date_and_time_synchronization: "no"
```

### Update System Preferences
```
- name: Update System Preferences
  zpe.system.preferences:
      show_hostname_on_webui_header: "yes"
      idle_timeout: "3600"
      enable_banner: "yes"
      enable_alarm_sound_when_one_power_supply_is_powered_off: "no"
```

For more samples review test cases in teh collection Roles or review the documentation.

## Read documentation
```
ansible-doc -t module zpe.system.date_and_time
ansible-doc -t module zpe.system.preferences
```






