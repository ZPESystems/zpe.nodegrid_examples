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
                 template='./collections/ansible_collections/zpe/system/templates/about',
                 set_fact='network_connections'),
        )
        cmds.append(
            dict(cmd='show /system/open_sessions/',
                 template='./collections/ansible_collections/zpe/system/templates/open_sessions',
                 set_fact='open_sessions'),
        )
        cmds.append(
            dict(cmd='show /system/device_sessions/',
                 template='./collections/ansible_collections/zpe/system/templates/device_sessions',
                 set_fact='device_sessions'),
        )
        # cmds.append(
        #     dict(cmd='show /system/event_list/',
        #          template='./collections/ansible_collections/zpe/system/templates/event_list',
        #          set_fact='event_list'),
        # )
        cmds.append(
            dict(cmd='show /system/system_usage/cpu_usage/',
                 template='./collections/ansible_collections/zpe/system/templates/cpu_usage',
                 set_fact='cpu_usage'),
        )
        cmds.append(
            dict(cmd='show /system/system_usage/disk_usage/',
                 template='./collections/ansible_collections/zpe/system/templates/disk_usage',
                 set_fact='disk_usage'),
        )
        cmds.append(
            dict(cmd='show /system/system_usage/memory_usage/',
                 template='./collections/ansible_collections/zpe/system/templates/memory_usage',
                 set_fact='memory_usage'),
        )
        cmds.append(
            dict(cmd='show /system/hw_monitor/io_ports/',
                 template='./collections/ansible_collections/zpe/system/templates/io_ports',
                 set_fact='io_ports'),
        )
        cmds.append(
            dict(cmd='show /system/hw_monitor/power/',
                 template='./collections/ansible_collections/zpe/system/templates/power',
                 set_fact='power'),
        )
        cmds.append(
            dict(cmd='show /system/hw_monitor/thermal/',
                 template='./collections/ansible_collections/zpe/system/templates/thermal',
                 set_fact='thermal'),
        )
        cmds.append(
            dict(cmd='show /system/hw_monitor/usb_sensors/',
                 template='./collections/ansible_collections/zpe/system/templates/usb_sensors',
                 set_fact='usb_sensors'),
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

