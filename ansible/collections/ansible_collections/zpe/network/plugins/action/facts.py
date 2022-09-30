# -*- coding: utf-8 -*-

from ansible.plugins.action import ActionBase
from ttp import ttp

class ActionModule(ActionBase):
    """action module"""


    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)
        self._result = {}
        self._task_vars = None

    def _run_command(self, cmds):
        result = dict()
        if len(cmds) >0:
            response = self._execute_module(module_name='nodegrid_cmds', module_args=cmds)
            if 'cmds_output' in response.keys():
                result["failed"] = False
                result['result'] = response
            else:
                result["failed"] = True
                result['result'] = response
        return result

    def _get_cmds(self):
        cmds = list()
        cmds.append(
            dict(cmd='show /system/about/',
                 template='./collections/ansible_collections/zpe/network/templates/about',
                 set_fact='network_connections'),
        )
        cmds.append(
            dict(cmd='show /settings/network_connections',
                 template='./collections/ansible_collections/zpe/network/templates/network_connections',
                 set_fact='network_connections'),
        )
        cmds.append(
            dict(cmd='show /settings/network_settings',
                template='./collections/ansible_collections/zpe/network/templates/network_settings',
                set_fact='network_settings')
        )
        cmds.append(
            dict(cmd='show /settings/switch_interfaces/',
                template='./collections/ansible_collections/zpe/network/templates/switch_interfaces',
                set_fact='switch_interfaces')
        )
        cmds.append(
            dict(cmd='show system/routing_table/',
                template='./collections/ansible_collections/zpe/network/templates/routing_table',
                set_fact='routing_table')
        )
        cmds.append(
            dict(cmd='show system/network_statistics/',
                template='./collections/ansible_collections/zpe/network/templates/network_statistics',
                set_fact='network_statistics',
                ignore_error='True')
        )
        cmds.append(
            dict(cmd='show system/switch_statistics/',
                template='./collections/ansible_collections/zpe/network/templates/switch_statistics',
                set_fact='switch_statistics')
        )

        # Template must be update, as it contains header line
        cmds.append(
            dict(cmd='show /settings/switch_vlan/',
                template='./collections/ansible_collections/zpe/network/templates/switch_vlan',
                set_fact='switch_vlan')
        )
        return cmds

    def run(self, tmp=None, task_vars=None):
        self._task_vars = task_vars
        self._playhost = task_vars.get("inventory_hostname")

        cmds = self._get_cmds()
        cmd_args = dict(
            cmds=cmds
        )
        cmds_results = self._run_command(cmd_args)
        if cmds_results.get('error'):
            return cmds_results
        else:
            # cmd_parser_result = cmds_results
            parsed_dict = dict()
            for cmd_result in cmds_results.get('result').get('cmds_output'):
                if cmd_result.get('error'):
                    cmd_parser_result = dict()
                    cmd_parser_result = cmd_result
                else:
                    try:
                        template_file = open(cmd_result.get("template"),'r')
                        template = template_file.read()
                    except:
                        template = ""
                    parser = ttp(data=cmd_result['stdout'], template=template)
                    parser.parse()
                    for item in parser.result()[0]:
                        parsed_dict.update(item)
        result = dict()
        if len(parsed_dict) > 0:
            result["ansible_facts"] = parsed_dict
            result["failed"] = False
            result["changed"] = False
        else:
            result["failed"] = True
            result["changed"] = False
        return result

