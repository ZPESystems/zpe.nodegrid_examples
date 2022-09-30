from ansible.utils.display import Display
import time
import pexpect
import socket


display = Display()


class NodegridDeviceConnection:
    def __init__(self, module):
        self.module = module

    def _check_prompt(self, text, prompttype="prompt", cmd_prompt=None, cmd_prompt_match=None):

        if cmd_prompt_match is None:
            cmd_prompt_match = "end"
        prompts_sendspace = ['More: <space>,  Quit: q or CTRL+Z, One line: <return>']
        prompt_exist = False
        if prompttype == "prompt":
            if cmd_prompt is not None:
                if isinstance(cmd_prompt, list):
                    prompts = cmd_prompt
                else:
                    prompts = [cmd_prompt]
            else:
                prompts = self.module['prompts']
        elif prompttype == "login":
            prompts = self.module['login_prompts']
        elif prompttype == "failed_login":
            prompts = self.module['failed_login_prompts']
        elif prompttype == "password":
            prompts = self.module['password_prompts']
        elif prompttype == "sendspace":
            prompts = prompts_sendspace
        else:
            prompts = self.module['prompts']

        display.vvv("_check_prompt: Command Prompt: " + str(prompts))
        for prompt in prompts:
            if cmd_prompt_match == "end":
                display.vvv("_check_prompt: end line check prompt: " + self.filter_nonprintable(text.strip()))
                if self.filter_nonprintable(text.strip()).endswith(prompt):
                    prompt_exist = True
            elif cmd_prompt_match == "inline":
                display.vvv("_check_prompt: inline check prompt: " + self.filter_nonprintable(text.strip()))
                if prompt in self.filter_nonprintable(text.strip()):
                    prompt_exist = True
        display.vvvv("prompt_exist:" + str(prompt_exist))
        return prompt_exist

    def local_get_connection(self):
        # Error Codes:
        # 0 - Promt
        # 1 - Login
        # 2 - password
        # 10 - connected by another user
        # 11 - read-only
        # 12 - device connection error
        # 13 - Login failed - Wrong Username
        # 14 - Login failed - Wrong Password
        # 100 - other error
        debug_output = dict()
        debug_action_list = list()
        debug_action_list.append("Create a Target connection")
        display.vvv("Create a Target connection")
        start_time = time.time()
        cmd = 'cli'
        connection_return_code = 100  # 0 - Promt, 1 - Login, 2 - password, 10 - connected by another user, 11 - read-only, 12 - device connection error 100 - other error
        channel_spawn = pexpect.spawn(cmd, timeout=30)
        try:
            recv_buffer = ""
            teststring = ""
            channel_spawn.expect("/]# ")
            display.vvv("Connected to CLI")
            channel_spawn.sendline("cd /access/")
            channel_spawn.expect("access]# ")
            display.vvv("In Access Menu")
            channel_spawn.sendline("connect " + self.module['target'])
            channel_shared = False
            channel_connected = False
            channel_notready_counter = 0
            username_counter = 0
            read_timeout = 60
            while True:
                try:
                    rsp = channel_spawn.read_nonblocking(1024, timeout=read_timeout)
                    recv_buffer += rsp.decode()
                except pexpect.exceptions.TIMEOUT as e:
                    display.vvv("timeout")
                    debug_action_list.append("timeout :" + str(e))
                read_timeout = 1
                teststring += rsp.decode().strip()
                debug_action_list.append("teststring :" + str(teststring.strip()))
                if channel_spawn.eof():
                    display.vvv("Read Error")
                    connection_return_code = 12
                    break
                elif teststring.strip().endswith("to cli ]") and not channel_connected:
                    display.vvv("Connection to Nodegrid is Open")
                    debug_action_list.append("Connection to Nodegrid is Open")
                    channel_notready_counter = 0
                    channel_connected = True
                    time.sleep(1)
                    # Clear teststring
                    teststring = ""
                    if self.module['send_new_line_on_login']:
                        display.vvv("Send new Line")
                        debug_action_list.append("Send new Line")
                        channel_spawn.send(self.module['new_line_on_login'])
                    continue
                elif teststring.strip().endswith("Device is in use by another user ]"):
                    display.vvv("Connection to Device is used by another user")
                    debug_action_list.append("Connection to Device is used by another user")
                    connection_return_code = 10
                    break
                elif teststring.strip().endswith("to see who is on this device.]") and not channel_shared:
                    display.vvv("Session is Shared")
                    debug_action_list.append("Session is Shared")
                    channel_shared = True
                    time.sleep(1)
                    channel_spawn.send(self.module['new_line'])
                    continue
                elif teststring.strip().endswith("logged in to share session in this device.]"):
                    debug_action_list.append("Session is Shareable")
                    connection_return_code = 10
                    break
                elif teststring.strip().endswith("attached]") and not channel_connected:
                    debug_action_list.append("Session attached")
                    channel_connected = True
                    if self.module['send_new_line_on_login'] == "True":
                        channel_spawn.send(self.module['new_line'])
                    continue
                elif teststring.strip().endswith("read-only -- use ^E c ? for help]"):
                    display.vvv("Session is Read Only")
                    debug_action_list.append("Session is Read Only")
                    connection_return_code = 11
                    break
                elif self._check_prompt(teststring):
                    debug_action_list.append("Device Prompt Detected")
                    connection_return_code = 0
                    break
                elif self._check_prompt(teststring, "login"):
                    if username_counter == 2:
                        display.vvv("Login incorrect")
                        debug_action_list.append("Login incorrect")
                        connection_return_code = 13
                        break
                    else:
                        display.vvv("Device Login Prompt Detected")
                        debug_action_list.append("Device Login Prompt Detected")
                        channel_spawn.send(self.module['username'] + self.module['new_line'])
                        display.vvv("Username Counter: " + str(username_counter))
                        debug_action_list.append("Username Counter: " + str(username_counter))
                        connection_return_code = 1
                        username_counter += 1
                        time.sleep(1)
                        continue
                elif self._check_prompt(teststring, "failed_login", cmd_prompt_match="inline"):
                    display.vvv("Login incorrect")
                    debug_action_list.append("Login incorrect")
                    connection_return_code = 14
                    break
                elif self._check_prompt(teststring, "password"):
                    display.vvv("Password Prompt Detected")
                    debug_action_list.append("Password Prompt Detected")
                    channel_spawn.send(self.module['password'] + self.module['new_line'])
                    connection_return_code = 2
                    time.sleep(5)
                    continue
                else:
                    channel_notready_counter += 1
                    display.vvv("Not Ready Yet " + str(channel_notready_counter))
                    debug_action_list.append("Not Ready Yet " + str(channel_notready_counter))
                    if channel_notready_counter == 5:
                        display.vvv("Checking : " + str(self.module['send_new_line_on_connection_timeout']))
                        debug_action_list.append("Checking : " + str(self.module['send_new_line_on_connection_timeout']))
                        if self.module['send_new_line_on_connection_timeout'] == "True":
                            display.vvv("Sending newline")
                            channel_spawn.send(self.module['new_line'])
                    elif channel_notready_counter == 10:
                        connection_return_code = 100
                        debug_output['error'] = "Connection not ready counter reached"
                        break
                    continue
        except pexpect.exceptions.EOF as e:
            display.vvv("Unexpected EOF")
            debug_output['error'] = str("Unexpected EOF : " + str(e))
            connection_return_code = 100
        except Exception as e:
            display.vvv(str(e))
            debug_output['error'] = str(e)
            connection_return_code = 100

        end_time = time.time()
        display.vvv("Connected to Target")
        display.vvv("Connection to device took : " + str(end_time - start_time) + " sec")
        debug_output['action'] = debug_action_list
        return channel_spawn, connection_return_code, debug_output

    def local_send_cmd(self, channel_spawn, cmd_args):
        # lets set values to defaults if they are not defined
        if 'cmd_new_line' not in cmd_args.keys():
            cmd_args['cmd_new_line'] = self.module['new_line']
        if 'read_output' not in cmd_args.keys():
            cmd_args['read_output'] = self.module['read_output']
        if 'cmd_prompt' not in cmd_args.keys():
            cmd_args['cmd_prompt'] = self.module['prompts']
        if 'cmd_prompt_match' not in cmd_args.keys():
            cmd_args['cmd_prompt_match'] = self.module['cmd_prompt_match']
        if 'cmd_timeout' not in cmd_args.keys():
            cmd_args['cmd_timeout'] = self.module['cmd_timeout']
        if 'template_paths' not in cmd_args.keys():
            cmd_args['template_paths'] = self.module['template_paths']

        debug_action_list = list()

        try:
            debug_action_list.append("Command send: " + cmd_args['cmd'] + cmd_args['cmd_new_line'])
            channel_spawn.send(cmd_args['cmd'] + cmd_args['cmd_new_line'])
            recv_buffer = ""
            teststring = ""
            debug_action_list.append("read_output : " + str(cmd_args['read_output']))
            if cmd_args['read_output']:
                timeout_counter = 0
                while not self._check_prompt(teststring, cmd_prompt=cmd_args['cmd_prompt'], cmd_prompt_match=cmd_args['cmd_prompt_match']) and timeout_counter < cmd_args['cmd_timeout']:
                    try:
                        time.sleep(0.2)
                        rsp = channel_spawn.read_nonblocking(1024, timeout=cmd_args['cmd_timeout'])
                        recv_buffer += self.filter_nonprintable(rsp.decode())
                    except socket.timeout as e:
                        debug_action_list.append("read timeout : " + str(e))
                        timeout_counter = timeout_counter + 1
                    teststring = recv_buffer.strip()
                    debug_action_list.append("teststring: " + teststring)
            else:
                recv_buffer = ""
            cmd_output = dict()
            cmd_output['failed'] = False
            cmd_output['cmd'] = cmd_args['cmd']
            cmd_output['read_output'] = cmd_args['read_output']
            if 'template' in cmd_args.keys():
                cmd_output['template'] = cmd_args['template']
                cmd_output['template_paths'] = cmd_args['template_paths']
            else:
                cmd_output['template'] = ''
            cmd_output['stdout'] = recv_buffer
            lines = recv_buffer.splitlines()
            lines.pop(0)
            if len(lines) > 1:
                lines.pop()
            cmd_output['stdout_lines'] = lines
            # cmd_output['debug'] = debug_action_list
            return 0, cmd_output
        except Exception as e:
            cmd_output = dict()
            cmd_output['failed'] = True
            cmd_output['error'] = "Error: executing command"
            cmd_output['error_details'] = str(e)
            cmd_output['debug'] = debug_action_list
            display.vvv("Error: executing command")
            return 1, cmd_output

    @staticmethod
    def filter_nonprintable(text):
        import string
        # Get the difference of all ASCII characters from the set of printable characters
        nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
        # Use translate to remove all non-printable characters
        return text.translate({ord(character): None for character in nonprintable})
