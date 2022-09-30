
class Generic:
    def __init__(self, module):
        self.connection_args = dict()
        self.connection_args['action'] = module['action']
        self.connection_args['target_found'] = True
        self.connection_args['target'] = module['target']
        self.connection_args['username'] = module['username']
        self.connection_args['password'] = module['password']
        self.connection_args['target_type'] = 'generic'
        self.connection_args['prompts'] = module['prompts']
        self.connection_args['password_prompts'] = module['password_prompts']
        self.connection_args['login_prompts'] = module['login_prompts']
        self.connection_args['failed_login_prompts'] = module['failed_login_prompts']
        self.connection_args['send_new_line_on_login'] = module['send_new_line_on_login']
        self.connection_args['new_line_on_login'] = module['new_line_on_login']
        self.connection_args['send_new_line_on_connection_timeout'] = module['send_new_line_on_connection_timeout']
        self.connection_args['new_line'] = module['new_line']
        self.connection_args['cmds_init'] = module['cmds_init']
        self.connection_args['send_cmds_init'] = module['send_cmds_init']
        self.connection_args['cmds'] = module['cmds']
        self.connection_args['cmds_close'] = module['cmds_close']
        self.connection_args['send_cmds_close'] = module['send_cmds_close']
        self.connection_args['cmd_prompt_match'] = module['cmd_prompt_match']
        self.connection_args['cmd_timeout'] = module['cmd_timeout']
        self.connection_args['read_output'] = module['read_output']
        self.connection_args['template_paths'] = module['template_paths']

    def get_connection_args(self):
        return self.connection_args
