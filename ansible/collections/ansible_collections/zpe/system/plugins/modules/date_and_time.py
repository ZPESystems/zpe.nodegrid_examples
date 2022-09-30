#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Rene Neumann <rene.neumann@zpesystems.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''

'''

EXAMPLES = r'''

'''

RETURN = r'''

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zpe.system.plugins.module_utils.date_and_time_util import get_module_params
from ansible_collections.zpe.system.plugins.module_utils.date_and_time_util import get_nodegrid_dict
from ansible_collections.zpe.system.plugins.module_utils.nodegrid_util import get_nodegrid_os_details
from ansible.utils.display import Display

import pexpect
import os

# We have to remove the SID from the Environmental settings, to avoid an issue
# were we can not run pexpect.run multiple times
if "DLITF_SID" in os.environ:
    del os.environ["DLITF_SID"]
if "DLITF_SID_ENCRYPT" in os.environ:
    del os.environ["DLITF_SID_ENCRYPT"]
# import logging
display = Display()

def get_config():
    cmd = "cli -c export_settings /settings/date_and_time/ --plain-password"
    output = pexpect.run(cmd)
    output = output.decode('UTF-8').strip()
    output_dict = {}
    command_state = 'error'
    if "Error" in output or "error" in output:
        if "Error: Invalid argument:" in output:
            output_dict["error"] = "Error getting Settings"
        else:
            output_dict["error"] = output
    for line in output.splitlines():
        if "=" in line:
            keypath, value = line.split('=')
            path, key = keypath.split()
            output_dict[key] = value
    if 'error' not in output_dict.keys():
        output = output.replace('\r\r\n', '\r\n')
        command_state = "successful"
    return command_state, output_dict, output

def import_settings(change_import_settings_list, use_config_start=True):
    cmd_cli = pexpect.spawn('cli', encoding='UTF-8')
    cmd_cli.setwinsize(500, 250)
    cmd_cli.expect_exact('/]# ')
    cmd_cli.sendline('.sessionpageout undefined=no')
    cmd_cli.expect_exact('/]# ')
#    cmd_cli.before
    if use_config_start:
        cmd_cli.sendline('config_start')
        cmd_cli.expect_exact('/]# ')
#        cmd_cli.before
    cmd_cli.sendline("import_settings")
    cmd_cli.expect_exact('finish.')
    # output = cmd_cli.before
    for item in change_import_settings_list:
        cmd_cli.sendline(item)
    cmd_cli.sendcontrol('d')
    cmd_cli.expect_exact('/]# ')
    output = cmd_cli.before
    if use_config_start:
        cmd_cli.sendline('config_confirm')
        cmd_cli.expect_exact('/]# ')
#        cmd_cli.before
    output_dict = {}
    import_status_details = []
    import_status = "succeeded"
    for line in output.splitlines():
        if "Result:" in line:
            settings_status = line.strip().split()
            if len(settings_status) == 4:
                import_status_details.append(dict(
                    path=settings_status[1],
                    result=settings_status[3]
                ))
                if settings_status[3] != "succeeded":
                    import_status = "failed"
                    import_status_details.append(settings_status)
            else:
                import_status = "unknown, result parsing error"
    if "Error" in output or "error" in output:
        output_dict["state"] = 'error'
        # output_dict["output_raw"] = output
        output_dict["import_list"] = change_import_settings_list
        output_dict["import_status"] = import_status
        output_dict["import_status_details"] = import_status_details
    else:
        output_dict["state"] = 'success'
        # output_dict["output_raw"] = output
        output_dict["import_list"] = change_import_settings_list
        output_dict["import_status"] = import_status
        output_dict["import_status_details"] = import_status_details
    return output_dict

def compare_dict(current_config, defined_config, nodegrid_dict, skip_keys=['state']):
    change = {}
    no_change = {}
    error_change = {}
    skip_change = {}
    for key in defined_config:
        # lets skip keys which are not part of teh config
        if key not in skip_keys:
            # Check if current value is Null, this means it was defined, lets skip
            if defined_config[key] is None:
                skip_change[key] = 'No value was defined'
            else:
                # Check if the provided key is properly defined
                if key in nodegrid_dict:
                    # Lets first check if there is a dependency
                    if nodegrid_dict[key]['parent']:
                        # if there is then lets make sure that the dependency is met
                        parent_value = None
                        # Lets check if the required parent value is getting configured
                        if nodegrid_dict[key]['parent_ansible_name'] in change.keys():
                            parent_value = change[nodegrid_dict[key]['parent_ansible_name']]['value_new']
                        # Lets check if the required parent key was already set
                        elif nodegrid_dict[key]['parent_ansible_name'] in no_change.keys():
                            parent_value = no_change[nodegrid_dict[key]['parent_ansible_name']]
                        else:
                            # If the parent setting was not defined lets check if the defined value is a default value
                            # if it is then we will skip silently and n change will be performed, if teh value is
                            # different from the default, then we assume it was defined by the user
                            # and we must raise an error
                            if defined_config[key] in nodegrid_dict[key]['cli_default']:
                                skip_change[key] = defined_config[key]
                            else:
                                error_change[key] = "Error: parent setting : " + nodegrid_dict[key]['parent_ansible_name'] + \
                                                    " requires a supported value : " + str(nodegrid_dict[key]['parent_value'])
                        # Lets check if the required parent value was already set or if it is still on a default value
                        if parent_value is not None :
                            # if the parent_value is defined then lets check if it is on an expected value
                            if parent_value in nodegrid_dict[key]['parent_value']:
                                # lets compare the values if a value exist in the current settings
                                # if not lets add it as a change
                                if nodegrid_dict[key]['cli_name'] in current_config:
                                    if defined_config[key] == current_config[nodegrid_dict[key]['cli_name']]:
                                        no_change[key] = defined_config[key]
                                    else:
                                        change[nodegrid_dict[key]['ansible_name']] = dict(
                                            value_current=current_config[nodegrid_dict[key]['cli_name']],
                                            value_new=defined_config[key],
                                            template=nodegrid_dict[key]['import_template'].format(value=defined_config[key], cli_name=nodegrid_dict[key]['cli_name'])
                                        )
                                else:
                                    change[nodegrid_dict[key]['ansible_name']] = dict(
                                        value_current="",
                                        value_new=defined_config[key],
                                        template=nodegrid_dict[key]['import_template'].format(value=defined_config[key], cli_name=nodegrid_dict[key]['cli_name'])
                                    )
                            else:
                            # If the parent setting was not defined lets check if the defined value is a default value
                            # if it is then we will skip silently and n change will be performed, if teh value is
                            # different from the default, then we assume it was defined by the user
                            # and we must raise an error
                                if defined_config[key] in nodegrid_dict[key]['cli_default']:
                                    skip_change[key] = defined_config[key]
                                else:
                                    error_change[key] = "Error: parent setting : " + nodegrid_dict[key]['parent_ansible_name'] + \
                                                        " requires a supported value : " + str(nodegrid_dict[key]['parent_value'])
                    else:
                        # if not then lets compare the values if a value exist in the current settings
                        # if not lets add it as a change
                        if nodegrid_dict[key]['cli_name'] in current_config:
                            if defined_config[key] == current_config[nodegrid_dict[key]['cli_name']]:
                                no_change[key] = defined_config[key]
                            else:
                                change[key] = dict(
                                    value_current=current_config[nodegrid_dict[key]['cli_name']],
                                    value_new=defined_config[key],
                                    template=nodegrid_dict[key]['import_template'].format(value=defined_config[key], cli_name=nodegrid_dict[key]['cli_name'])
                                )
                        else:
                            change[key] = dict(
                                value_current="",
                                value_new=defined_config[key],
                                template=nodegrid_dict[key]['import_template'].format(value=defined_config[key], cli_name=nodegrid_dict[key]['cli_name'])
                            )
                else:
                    # The provided key was not properly implement
                    error_change[key] = "Error: setting : " + key + " is currently not implement"

    if len(change) > 0:
        return_value = dict(
            change_required=True,
            change=change,
            no_change=no_change,
            error_change=error_change,
#           skip_change=skip_change
            )
    else:
        return_value = dict(
            change_required=False,
            change=change,
            no_change=no_change,
            error_change=error_change,
#           skip_change=skip_change
            )
    return return_value

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = get_module_params()
    nodegrid_dict = get_nodegrid_dict()

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
        use_config_start_global = False
    elif nodegrid_os['software_minor'] < '6':
        result['warning'] = 'Not recommended and untested Nodegrid OS version, some features might not work. recommended 5.6.1 or higher. Current version: ' + nodegrid_os['software']
        use_config_start_global = False
    else:
        use_config_start_global = True
    # result['nodegrid_facts'] = nodegrid_os

    current_config = dict()
    state_dict = dict()
    state, current_config, config_settings = get_config()

    # Lets check if we were able to get the configuration , or if there was an issue
    # in case off an error we will raise an exception and fail the execution
    if state == "error":
        result['message'] = current_config
        result['failed'] = True
        module.fail_json(msg='Error while checking system preferences', **result)

    # Lets compare the current config with the specified configuration
    changes_dict = compare_dict(current_config, module.params, nodegrid_dict)

    # The module supports diff mode, which will display the configuration
    # changes which will be performed on the connection
    diff_dict=dict()
    prepared_output = str()
    change_import_settings_list = []
    if changes_dict['change_required']:
        for item in changes_dict['change']:
            change_import_settings_list.append(changes_dict['change'][item]['template'])
            prepared_output = prepared_output + changes_dict['change'][item]['template'] + "\r\n"
    diff_dict['prepared']=prepared_output
    result['diff'] = diff_dict

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        if changes_dict['change_required']:
            result['changed'] = True
        result['message'] = "No changes where performed, running in check_mode"
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    if changes_dict['change_required']:
        result['changed'] = True
        import_result = import_settings(change_import_settings_list, use_config_start=use_config_start_global)
        result['import_result'] = import_result
        if import_result['import_status'] == 'succeeded':
            result['message'] = 'Import was successful'
        else:
            module.fail_json(msg='Import failed', **result)
    else:
        result['changed'] = False
        result['message'] = 'No change required'

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
