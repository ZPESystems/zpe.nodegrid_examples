#!/usr/bin/python3

import pexpect
import json


def get_devices():
    raw = pexpect.run('llconf ini -si /etc/spm_server.ini json')
    return raw.strip()


def parse(raw):
    inventory = {
        "managed_devices": {
            "hosts": [],
            "children": ["device_disabled", "device_enabled", "device_ondemand"],
            "vars": {
                "ansible_python_interpreter": "/usr/bin/python3",
                "ansible_ssh_user": "ansible",
                "ansible_ssh_private_key_file": "/home/ansible/.ssh/id_ed25519",
                "ansible_host": "localhost"
                }
        },
        "device_disabled": {
            "hosts": []
        },
        "device_enabled": {
            "hosts": []
        },
        "device_ondemand": {
            "hosts": []
        },
        "_meta": {
            "hostvars": {
                 }
            }
        }
    parsed = json.loads(raw)
    if len(parsed) == 1:
        parsed = parsed['(root)']
        for device in parsed:
            inventory['managed_devices']['hosts'].append(device)
            if parsed[device]['status'] == 'disabled':
                inventory['device_disabled']['hosts'].append(device)
            elif parsed[device]['status'] == 'enabled':
                inventory['device_enabled']['hosts'].append(device)
            elif parsed[device]['status'] == 'ondemand':
                inventory['device_ondemand']['hosts'].append(device)
            if parsed[device]['type'] not in inventory.keys():
                inventory.update({parsed[device]['type']: {
                    "hosts": []
                }})
                inventory['managed_devices']['children'].append(parsed[device]['type'])
                inventory[parsed[device]['type']]['hosts'].append(device)
            else:
                inventory[parsed[device]['type']]['hosts'].append(device)
            inventory['_meta']['hostvars'][device] = parsed[device]
    return inventory


if __name__ == '__main__':
    devices = get_devices()
    out = parse(devices)
    print(json.dumps(out))
