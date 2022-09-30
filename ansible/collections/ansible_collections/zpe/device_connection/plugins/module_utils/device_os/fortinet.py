
class Fortinet:
    def __init__(self, module):
        self.connection_args = dict()
        self.connection_args['action'] = module['action']
        self.connection_args['target_found'] = True
        self.connection_args['target'] = module['target']
        self.connection_args['username'] = module['username']
        self.connection_args['password'] = module['password']
        self.connection_args['target_type'] = 'fortinet'
        self.connection_args['prompts'] = ['#']
        self.connection_args['password_prompts'] = ['assword:']
        self.connection_args['login_prompts'] = ['ogin:']
        self.connection_args['failed_login_prompts'] = ['Login incorrect']
        self.connection_args['send_new_line_on_login'] = True
        self.connection_args['new_line_on_login'] = '\n'
        self.connection_args['send_new_line_on_connection_timeout'] = False
        self.connection_args['new_line'] = '\n'
        self.connection_args['cmds_init'] = []
        self.connection_args['send_cmds_init'] = module['send_cmds_init']
        if self.connection_args['action'] == "fact":
            self.connection_args['cmds'] = [
                {"cmd": "get system status", "template": "fortinet_get_system_status"}
            ]
        elif self.connection_args['action'] == "setup_console":
            self.connection_args['cmds'] = [
                {"cmd": "config system console", "template": ""},
                {"cmd": "set output standard", "template": ""},
                {"cmd": "set baudrate 115200", "template": ""},
                {"cmd": "end", "template": "", "cmd_prompt" : ["(y/n)",'#']},
                {"cmd": "y", "template": "", "cmd_newline": ""}
            ]
        else:
            self.connection_args['cmds'] = module['cmds']
        self.connection_args['cmds_close'] = [
            {"cmd": "exit", "template": "", "read_output":"False"}
        ]
        self.connection_args['send_cmds_close'] = module['send_cmds_close']
        self.connection_args['cmd_prompt_match'] = module['cmd_prompt_match']
        self.connection_args['cmd_timeout'] = module['cmd_timeout']
        self.connection_args['read_output'] = module['read_output']
        self.connection_args['template_paths'] = module['template_paths']

    def get_connection_args(self):
        return self.connection_args
