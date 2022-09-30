# -*- coding: utf-8 -*-

from ansible.module_utils._text import to_native, to_text
from ansible.plugins.action import ActionBase
from ttp import ttp

class ActionModule(ActionBase):
    """action module"""


    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)
        self._result = {}
        self._task_vars = None

    def _run_command(self):
        command = self._task.args.get("command")
        ignore_error = self._task.args.get("ignore_error")
        result = dict()
        if command:
            cmds=list()
            cmds.append(dict(
                cmd=command,
                ignore_error=ignore_error
            ))
            cmd_args=dict(
                cmds=cmds
            )
            response = self._execute_module(module_name='nodegrid_cmds', module_args=cmd_args)
            if 'cmds_output' in response.keys():
                for item in response['cmds_output']:
                    try:
                        result["stdout"] = item['stdout']
                        result["stdout_lines"] = item['stdout_lines']
                    except Exception as exc:
                        result["failed"] = True
                        result["msg"] = [to_text(exc)]
            else:
                result = response
                result["failed"] = True
                result['result'] = response
                result['command'] = command
        return result


    def run(self, tmp=None, task_vars=None):

        self._task_vars = task_vars
        self._playhost = task_vars.get("inventory_hostname")

        result = self._run_command()
        if result.get("failed"):
            return result
        else:
            try:
                template_file = open(self._task.args.get("template"),'r')
                template = template_file.read()
            except:
                template = ""
            parsed_dict = dict()
            parser = ttp(data=result.get("stdout"), template=template)
            parser.parse()
            for item in parser.result()[0]:
                parsed_dict.update(item)
            result['template_data'] = result.get("stdout")
            result['template'] = template
            result['parsed'] = parsed_dict
            result["ansible_facts"] = parsed_dict
        return result
