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

    def parse_connection_state(self, output="", error_list=['error', 'Error']):
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
        # If target_os is not defined by the user we set it to generic
        if "target_os" not in module_args:
            module_args['target_os'] = "generic"
        module_args['action'] = "fact"
        # Connect to target device the default cmds as defined in device type defaults
        output = self._execute_module(module_name='device_connection', module_args=module_args, task_vars=task_vars, tmp=tmp)
        # Check if the device connection was successfully and failed
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
                    cmd_output['cmd_success'] = self.parse_connection_state(cmd_output['stdout'])
            # if the cmd did not return an error, and a parsing template is provided then parse the output
                if cmd_output['cmd_success'] and len(cmd_output['template']) > 0:
                    display.vvv('# Lets parse the output the output is')
                    display.vvv(cmd_output['stdout'])
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
