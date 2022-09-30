from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from os.path import exists
from ttp import ttp
display = Display()


class ActionModule(ActionBase):

    def parse_output(self, output="", template="",paths=['']):
        # Take a command output and parse the output using a TTP template
        # Function returns a parsed dict
        # Dict will be blank if parsing failed
        template_file = None
        for path in paths:
            template_exists = exists(path + "/" + template + ".ttp")
            if template_exists:
                template_file = open(path + "/" + template + ".ttp",'r')
        try:
            if template_file is not None:
                parsed_dict = dict()
                template = template_file.read()
                parser = ttp(data=output, template=template)
                parser.parse()
                for item in parser.result()[0]:
                    parsed_dict.update(item)
                return True, parsed_dict
            else:
                return False, f'Error: was not able to find template: {template}.ttp in template path: {paths}'
        except Exception as e:
            return False, f'Error: parsing text. Full error: {e}'

    def parse_state(self, output="", error_list=['error', 'Error']):
        found_error = False
        for error_check in error_list:
            if error_check in output:
                found_error = True
        if found_error:
            return False
        else:
            return True

    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        # Get the passed in module variables
        module_args = self._task.args.copy()
        # Create the framework for the return object
        result = dict(
            changed=False,
            message=''
        )
        # module_args['target_os'] = "generic"

        # Check if commands where passed in as a string list or as dict
        cmd_list = list()
        replace_cmd_list = False
        # Check if any commands where specified in the task,
        # if not we will use the defaults as defined by the module
        if 'cmds' in module_args.keys():
            for cmd in module_args['cmds']:
                if isinstance(cmd, str):
                    cmd_dict = dict(cmd=cmd)
                    cmd_list.append(cmd_dict)
                if isinstance(cmd, dict):
                    cmd_list.append(cmd)
            display.vvv(str(cmd_list))
            module_args['cmds'] = cmd_list

        output = self._execute_module(module_name='device_connection', module_args=module_args, task_vars=task_vars, tmp=tmp)
        # Check if the command execution failed
        if 'failed' in output.keys():
            result['failed'] = True
            if 'message' in output.keys():
                result['message'] = output['message']
            if 'msg' in output.keys():
                result['msg'] = output['msg']
        else:
        # lets check the output of the cmds and check for errors and parse if needed
            facts = dict()
            display.vvv('# lets check the output of the cmds and check for errors and parse if needed')
            for cmd_output in output['cmds_output']:
                if cmd_output['failed']:
                    cmd_output['cmd_success'] = False
                else:
                    cmd_output['cmd_success'] = self.parse_state(cmd_output['stdout'])
            if cmd_output['cmd_success'] and len(cmd_output['template']) > 0:
                parse_state, parse_output = self.parse_output(output=cmd_output['stdout'], template=cmd_output['template'], paths=cmd_output['template_paths'])
                if parse_state:
                    cmd_output['parse_output'] = parse_output
                    for key in parse_output:
                        facts[key] = parse_output[key]
                else:
                    cmd_output['parse_error'] = parse_output
            result['ansible_facts'] = facts
            result['output'] = output['cmds_output']
            result['changed'] = output['changed']
        return result
