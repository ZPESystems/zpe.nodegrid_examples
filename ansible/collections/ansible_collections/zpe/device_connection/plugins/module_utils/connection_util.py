from ansible.utils.display import Display
from ansible_collections.zpe.device_connection.plugins.module_utils.device_os.generic import Generic
from ansible_collections.zpe.device_connection.plugins.module_utils.device_os.nodegrid import Nodegrid
from ansible_collections.zpe.device_connection.plugins.module_utils.device_os.fortinet import Fortinet
from ansible_collections.zpe.device_connection.plugins.module_utils.device_os.panos import Panos
from ansible_collections.zpe.device_connection.plugins.module_utils.device_os.junos import Junos
from ansible_collections.zpe.device_connection.plugins.module_utils.device_os.ios import IOS
import pexpect

display = Display()

def get_module_params():
    module_args = dict(
        action=dict(type='str', required=False, default=''),
        target=dict(type='str', required=True),
        target_os=dict(type='str', choice=['generic'], required=False, default='generic'),
        username=dict(type='str', required=False, default='zpe'),
        password=dict(type='str', required=False, default='', no_log=True),
        prompts=dict(type='list', required=False, default=[':~$', ']#', '#', '>']),
        password_prompts=dict(type='list', required=False, default=['assword:'], no_log=False),
        login_prompts=dict(type='list', required=False, default=['ogin:', 'sername:', 'User Name:']),
        failed_login_prompts=dict(type='list', required=False, default=['Login incorrect', 'press ENTER key to retry authentication']),
        send_new_line_on_login=dict(type='bool', required=False, default=True),
        new_line_on_login=dict(type='str', required=False, default='\r\n'),
        send_new_line_on_connection_timeout=dict(type='bool', required=False, default=False),
        new_line=dict(type='str', required=False, default='\n'),
        cmds_init=dict(type='list', required=False, default=[]),
        send_cmds_init=dict(type='bool', required=False, default=True),
        cmds_close=dict(type='list', required=False, default=[{"cmd": "exit", "template": "", "read_output": False}]),
        send_cmds_close=dict(type='bool', required=False, default=True),
        cmds=dict(type='list', required=False, default=[{"cmd": "", "template": "cli_prompt_hostname"}]),
        cmd_prompt_match=dict(type='str', choice=['end', 'inline'], required=False, default='end'),
        cmd_timeout=dict(type='int', required=False, default=10),
        read_output=dict(type='bool', required=False, default=True),
        template_paths=dict(type='list', required=False, default=['./collections/ansible_collections/zpe/device_connection/parse_templates', './templates']),
    )
    return module_args

def get_nodegrid_dict():
    nodegrid_keys = dict(
    )
    return nodegrid_keys

def get_connection_args(target_type, module=None):
    try:
        target_check = check_target(module['target'])
        if target_check['found']:
            if target_type == 'generic':
                device_type = Generic(module)
                connection_args = device_type.get_connection_args()
            elif target_type == 'nodegrid':
                device_type = Nodegrid(module)
                connection_args = device_type.get_connection_args()
            elif target_type == 'fortios':
                device_type = Fortinet(module)
                connection_args = device_type.get_connection_args()
            elif target_type == 'junos':
                device_type = Junos(module)
                connection_args = device_type.get_connection_args()
            elif target_type == 'panos':
                device_type = Panos(module)
                connection_args = device_type.get_connection_args()
            elif target_type == 'ios':
                device_type = IOS(module)
                connection_args = device_type.get_connection_args()
            else:
                generic = Generic(module)
                connection_args = generic.get_connection_args()
        else:
            connection_args = dict()
            connection_args['target_found'] = target_check['found']
            connection_args['target_check'] = target_check
            connection_args['message'] = "target device : {} not found".format(module['target'])
            connection_args['error'] = ''
        return connection_args
    except Exception as e:
        connection_args = dict()
        connection_args['target_type'] = target_type
        connection_args['target_found'] = False
        connection_args['target_check'] = {}
        connection_args['message'] = "Error: error getting device details"
        connection_args['error'] = str(e)
        return connection_args

def check_target(target):
    cmd_cli = pexpect.spawn('cli', encoding='UTF-8')
    cmd_cli.setwinsize(500, 250)
    cmd_cli.expect_exact('/]# ')
    cmd_cli.sendline('.sessionpageout undefined=no')
    cmd_cli.expect_exact('/]# ')
    cmd_cli.sendline("cd /access")
    cmd_cli.expect_exact('s]# ')
    cmd_cli.sendline("search " + target)
    cmd_cli.expect_exact('h]# ')
    output = cmd_cli.before
    output_dict = {}
    device = list()
    device_found = False
    error = False
    for line in output.splitlines():
        if "results" in line:
            device = line.strip().split()
            try:
                if device[1] == "1":
                    device_found = True
                else:
                    device_found = False
            except Exception:
                device_found = False
                error = True
    if "Error" in output or "error" in output or error:
        output_dict["state"] = 'error'
        output_dict["found"] = device_found
        output_dict["device_found_details"] = device
    else:
        output_dict["state"] = 'success'
        output_dict["found"] = device_found
        output_dict["device_found_details"] = device
    return output_dict
