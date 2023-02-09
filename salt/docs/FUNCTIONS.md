# Nodegrid Proxy Module Available Functions

## salt.proxy.nodegrid.ping()

Test SSH connection to target.

Returns boolean.

retries=5
- How many times to retry

wait_secs=2
- How many seconds to wait until next retry

CLI Example:
```bash
salt '*' nodegrid.ping
salt '*' nodegrid.ping retries=10 wait_secs=1 --timeout 20
salt '*' nodegrid.ping retries=10 wait_secs=2 --timeout 40
salt '*' nodegrid.ping retries=10 wait_secs=5 --timeout 50
```

## salt.proxy.nodegrid.ping_icmp()
When Nodegrid is factory default, we cannot use common ping.

So request ICMP ping on the target before trying to send commands.

Returns boolean.

retries=5
- How many times to retry

wait_secs=2
- How many seconds to wait until next retry

CLI Example:
```bash
salt '*' nodegrid.ping_icmp
salt '*' nodegrid.ping_icmp retries=10 wait_secs=1 --timeout 20
salt '*' nodegrid.ping_icmp retries=10 wait_secs=2 --timeout 40
salt '*' nodegrid.ping_icmp retries=10 wait_secs=5 --timeout 50
```


## salt.proxy.nodegrid.change_default_password()

Returns a list containing boolean and a status message.
Launch SSH and Change password to the pillar file password.
Validates if changed to pillar password.

When Nodegrid is factory default password change is enforced.

CLI Example:
```bash
salt '*' nodegrid.change_default_password
```

## salt.proxy.nodegrid.check_version(desired_version)
Check device version against given desired version.

Returns boolean, False is returned along with current device version.

CLI Example:
```bash
salt '*' nodegrid.check_version 5.6.9
```

## salt.proxy.nodegrid.get_system_about()

Returns raw CLI output of the command: `show /system/about`

CLI Example:
```bash
salt '*' nodegrid.get_system_about
```

## salt.proxy.nodegrid.add_license(lic_key)

Returns boolean of CLI procedure of License Setup commands of license key passed as argument.

In case of error, returns CLI error message.

CLI Example:
```bash
salt '*' nodegrid.add_license LICENSE_KEY
```

## salt.proxy.nodegrid.cli(command)

Returns raw CLI output of the command passed as argument.

In case of error, returns CLI error message.

command:

- Command to be executed on the device.

CLI Example:
```bash
salt '*' nodegrid.cli "show /system/about"
salt '*' nodegrid.cli "show /settings/license"
salt '*' nodegrid.cli "show /settings/devices"
salt '*' nodegrid.cli "reboot --force"
salt '*' nodegrid.cli "cd /settings/system_preferences/
set idle_timeout=3600
set enable_banner=yes
commit"
salt '*' nodegrid.cli "cd /settings/license
add
set license_key=LICENSE
commit"
```

## salt.proxy.nodegrid.cli_file(file)

Returns a raw CLI output of the commands on the file passed as argument.

In case of error, returns CLI error message.

file:
- File with CLI Commands to be executed on the device.
- Located at salt-master file_roots, default: /srv/salt/
- Example: /srv/salt/cli/file.cli

File Example:
```bash
$ cat /path/to/file.cli
cd /settings/system_preferences/
set idle_timeout=3600
set enable_banner=yes
commit
```

CLI Example:
```bash
salt '*' nodegrid.cli salt://cli/file.cli
```

## salt.proxy.nodegrid.cli_shell(command)
"""
Execute given command in user shell.

Returns raw CLI output of the command passed as argument.

CLI Example:
```bash
salt '*' nodegrid.cli_shell "ls /var/sw"
``` 

## salt.proxy.nodegrid.cli_root_shell(command)
Execute given command in root shell.

Returns raw CLI output of the command passed as argument.

CLI Example:
```bash
salt '*' nodegrid.cli_root_shell "ls /var/sw"
```

## salt.proxy.nodegrid.import_settings(command)

Returns boolean of CLI import_settings procedure of the given CLI exported data.

command:
- CLI import_settings formatted commands to be imported on the device.

CLI Example:
```bash
salt '*' nodegrid.import_settings "/settings/system_preferences idle_timeout=3600"
salt '*' nodegrid.import_settings "/settings/system_preferences idle_timeout=3600
/settings/system_preferences enable_banner=yes"
```

## salt.proxy.nodegrid.import_settings_file(file)

Returns boolean of CLI import_settings procedure of the given file with CLI exported data.

file:
- File with CLI import_settings formatted commands to be imported on the device.
- Located at salt-master file_roots, default: /srv/salt/
- Example: /srv/salt/cli/file.cli

File Example:
```bash
$ cat /path/to/import.cli
/settings/system_preferences idle_timeout=3600
/settings/system_preferences show_hostname_on_webui_header=yes
```

CLI Example:
```bash
salt '*' nodegrid.import_settings_file salt://cli/import.cli
salt '*' nodegrid.import_settings_file salt://cli/import_template.cli --timeout 100
```

## salt.proxy.nodegrid.export_settings(path)

Returns raw CLI output of export_settings procedure on the given CLI path.

path:
- CLI path to export and get the data from.

CLI Example:
```bash
salt '*' nodegrid.export_settings "/settings/system_preferences"
```

## salt.proxy.nodegrid.save_settings(**kwargs)
Returns boolean of CLI procedure of save_settings with the given options.

In case of error, returns CLI error message.

destination:
- Where to save the backup file (local_system or remote_server)

filename:
- (local_system) name or the absolute_path of the backup file (/backup/filename)

url:
- (remote_server) Remote server url to get backup file

username:
- (remote_server) Name or the absolute_path of the backup file

password:
- (remote_server) Name or the absolute_path of the backup file

absolute_name:
- (remote_server) Boolean. The path in url to be used as absolute path name

CLI Example:
```bash
salt '*' nodegrid.save_settings destination=local_system filename=backup.cfg
salt '*' nodegrid.save_settings destination=remote_server url=ftp://SERVER_IP/filepath username=ftpuser password=ftpuser absolute_name=True
```

## salt.proxy.nodegrid.apply_settings(**kwargs)
Returns boolean of CLI procedure of apply_settings with the given options.

In case of error, returns CLI error message.

from_destination:
- Where to get the backup file (local_system or remote_server)

filename:
- (local_system) name or the absolute_path of the backup file (/backup/filename)

url:
- (remote_server) Remote server url to get backup file

username:
- (remote_server) Name or the absolute_path of the backup file

password:
- (remote_server) Name or the absolute_path of the backup file

absolute_name:
- (remote_server) Boolean. The path in url to be used as absolute path name

CLI Example:
```bash
salt '*' nodegrid.apply_settings destination=local_system filename=backup.cfg
salt '*' nodegrid.apply_settings destination=remote_server url=ftp://SERVER_IP/filepath username=ftpuser password=ftpuser
```


## salt.proxy.nodegrid.cp_file(**kwargs)
Returns boolean of transfer of the file.
In case of error, returns error message.

Get file from master using salt.cp.get_file
Transfer file from minion to target using SCP

file
- File with CLI Commands to be executed on the device.
- Located at salt-master file_roots, default: /srv/salt/
- Example: /srv/salt/file.txt
destination
- Path on target device to transfer file

CLI Example:
```bash
salt '*' nodegrid.cp_file salt://file.txt /tmp/
salt '*' nodegrid.cp_file salt://Nodegrid_Platform_v5.4.3_20211221.iso /var/sw/ --timeout 900
```


## salt.proxy.nodegrid.software_upgrade(**kwargs)
Execute CLI procedure of apply_settings with the given options.
In case of CLI error, returns CLI error message.

Upgrade takes an average of 10 minutes to complete and to the system be available again.

Returns boolean
- Condition 1: Upgrade routine requested successfully;
- Condition 2: Wait to device be available again successfully.

wait=True
- Wait after upgrade software request is sent
retries=150
- How many times to retry
wait_secs=5
- How many seconds to wait until next retry

image_location:
- Where to get the firmware file (local_system or remote_server)

filename:
- (local_system) name or the absolute_path of the backup file (/backup/filename)

url:
- (remote_server) Remote server url to get backup file

username:
- (remote_server) Name or the absolute_path of the backup file

password:
- (remote_server) Name or the absolute_path of the backup file

absolute_name:
- (remote_server) Boolean. The path in url to be used as absolute path name

format_partitions_before_upgrade:
- (optional, boolean)

force_boot_mode:
- (optional, boolean)

if_downgrading:
- (optional, boolean)
- - apply_factory_default_configuration
- - restore_configuration_saved_on_version_upgrade

CLI Example:
```bash
salt '*' nodegrid.software_upgrade image_location=local_system filename=Nodegrid_Platform_v5.6.9_20230111.iso --timeout 1500
salt '*' nodegrid.software_upgrade image_location=local_system filename=Nodegrid_Platform_v5.6.9_20230111.iso retries=75 wait_secs=10 --timeout 1500
salt '*' nodegrid.software_upgrade image_location=local_system filename=Nodegrid_Platform_v5.6.9_20230111.iso wait=False --timeout 60
salt '*' nodegrid.software_upgrade destination=remote_server url=ftp://SERVER_IP/Nodegrid_Platform_v5.6.9_20230111.iso username=ftpuser password=ftpuser  wait=False --timeout 120
```
