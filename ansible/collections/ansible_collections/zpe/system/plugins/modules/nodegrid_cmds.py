#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Rene Neumann <rene.neumann@zpesystems.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: connection_facts
author: Rene Neumann (@zpe-rneumann)
'''

EXAMPLES = r'''
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zpe.system.plugins.module_utils.nodegrid_util import get_nodegrid_os_details
from ansible.utils.display import Display

import pexpect
import os
import re

# We have to remove the SID from the Environmental settings, to avoid an issue
# were we can not run pexpect.run multiple times
if "DLITF_SID" in os.environ:
    del os.environ["DLITF_SID"]
if "DLITF_SID_ENCRYPT" in os.environ:
    del os.environ["DLITF_SID_ENCRYPT"]
# import logging
display = Display()


def execute_cmd(cmd):
        if 'cmd' in cmd.keys():
            cmd_cli = pexpect.spawn('cli', encoding='UTF-8')
            cmd_cli.setwinsize(500, 250)
            cmd_cli.expect_exact('/]# ')
            cmd_cli.sendline('.sessionpageout undefined=no')
            cmd_cli.expect_exact('/]# ')
            cmd_cli.sendline(cmd['cmd'])
            cmd_cli.expect_exact('/]# ')
            cmd_cli.sendline('exit')
            output = cmd_cli.before
            output = output.replace('\r\r\n', '\r\n')
            output_dict = dict()
            if 'ignore_error' in cmd.keys():
                output_dict['error'] = False
                output_dict['stdout'] = output
                output_lines = output.splitlines()
                output_dict['stdout_lines'] = output_lines
            else:
                if "Error" in output or "error" in output:
                    output_dict['error'] = True
                    output_dict['stdout'] = output
                else:
                    output_dict['error'] = False
                    output_dict['stdout'] = output
                    output_lines = output.splitlines()
                    output_dict['stdout_lines'] = output_lines
        return output_dict


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        cmds=dict(type='list', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    #
    # Nodegrid OS section starts here
    #
    # Lets get the current interface status and check if it must be changed

    nodegrid_os = get_nodegrid_os_details()
    if nodegrid_os['software_major'] < '5':
        module.fail_json(msg='Unsupported Nodegrid OS version. recommended 5.6.1 or higher. Current version: ' + nodegrid_os['software'], **result)
    elif nodegrid_os['software_minor'] < '6':
        result['warning'] = 'Not recommended and untested Nodegrid OS version, some features might not work. recommended 5.6.1 or higher. Current version: ' + nodegrid_os['software']

    # run commands and gather output
    cmd_results = list()
    cmd_result = dict()
    try:
        for cmd in module.params['cmds']:
            cmd_result = execute_cmd(cmd)
            if 'template' in cmd.keys():
                cmd_result['template'] = cmd['template']
            if 'set_fact' in cmd.keys():
                cmd_result['set_fact'] = cmd['set_fact']
            if 'ignore_error' in cmd.keys():
                cmd_result['ignore_error'] = cmd['ignore_error']
            cmd_result['command'] = cmd.get('cmd')
            cmd_results.append(cmd_result)
        result['error'] = False
        result['cmds_output'] = cmd_results
    except Exception as exc:
        result['error'] = True
        result['message'] = exc

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
