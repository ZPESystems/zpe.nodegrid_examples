#!/usr/bin/python3
import pexpect
import time


def run_ansible_playbook(playbook, limit='', diff='', check=''):
    ssh_command = "ssh ansible@localhost -o StrictHostKeyChecking=no"
    ansible_cmd = "ansible-playbook /etc/ansible/playbooks/{playbook} --limit {limit} {diff} {check}".format(playbook=playbook, limit=limit, diff=diff, check=check)
    try:
        ansible_shell = pexpect.spawn(ssh_command, encoding='utf-8')
        ansible_shell.expect("$")
        ansible_shell.sendline(ansible_cmd)
        counter = 0
        out = ''
        while not out.endswith("$ ") and counter < 500:
            rsp = ''
            try:
                time.sleep(0.2)
                rsp = ansible_shell.read_nonblocking(size=1024, timeout=1)
            except Exception:
                counter = counter + 1
            out += rsp
        ansible_shell.sendline("exit")
        ansible_shell.close()
        for line in out.splitlines():
            if ansible_cmd in line:
                continue
            else:
                print(line)
    except Exception as e:
        print(str(e))


def get_info(dev):
    run_ansible_playbook("get_device_facts.yml", dev.device_name)


def save_config(dev):
    run_ansible_playbook("get_device_settings.yml", dev.device_name)


def check_config(dev):
    run_ansible_playbook("get_device_settings.yml", dev.device_name, diff='--diff', check='--check')
