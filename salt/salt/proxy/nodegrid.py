#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Diego Russi <diego.russi@zpesystems.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import

# Import python libs
import logging
from io import BytesIO
from re import search, subn
from re import compile as re_compile
from os.path import exists
from os import remove, system
from time import sleep


# Global variables
DETAILS = {}
GRAINS_CACHE = {}

CLI_PROMPT = [
    ']# ',
    '# ',           # root
    '$ ',           # user
    '(yes, no)  :'  # reboot, delete...
]
CLI_PROMPT_REGEX = r"^\[.+@.+ ?.+\]# $"
CLI_TIMEOUT = 60
MINION_FILE_CACHE = "/tmp/"

PLOG = "/tmp/pexpect.log"
PSLOG = "/tmp/pexpect_send.log"
PRLOG = "/tmp/pexpect_read.log"

CONN_ERROR = "Could not connect or login to proxy target device."

# Set up logging
FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]: %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__file__)

# Module properties
__proxyenabled__ = ["nodegrid"]
__virtualname__ = "nodegrid"


try:
    import pexpect

    HAS_LIB = True
except ImportError:
    HAS_LIB = False

# Required Functions

def __virtual__():
    """
    Only load if the pexpect execution module is available.
    """
    if HAS_LIB:
        return __virtualname__

    return False, "The Nodegrid Proxy Minion module did not load due missing requirements: python-pexpect."


def init(opts):
    """
    Required.
    This function gets called when the proxy starts up.
    For nodegrid device, the appropriate pillar conf with SSH connection details must be cached.
    """
    try:
        log.debug("zpe_nodegrid opts: " + str(opts["proxy"]))

        # Cache configuration details globally
        DETAILS["host"] = opts["proxy"]["host"]
        DETAILS["username"] = opts["proxy"]["username"]
        DETAILS["password"] = opts["proxy"]["password"]
        # DETAILS["public_key_file"] = public_key_file

        return True

    except Exception as error: # pylint: disable=broad-except
        _do_log_exception(error, "init")
        return False


def shutdown(conn_obj):
    """
    Required.
    """
    # DETAILS["flog"].close()
    # DETAILS["fsend"].close()
    DETAILS["mread"].close()
    conn_obj.sendline("exit")
    conn_obj.close()
    return True


def ping(**kwargs):
    log.debug("PROXY zpe_nodegrid ping status")
    log.debug("PROXY zpe_nodegrid ping kwargs = " + str(kwargs))

    tries = 1
    fn_ret = False
    retries = kwargs.get("retries", 5)
    wait_secs = kwargs.get("wait_secs", 2)

    try:
        while (tries <= retries):
            log.debug(f"zpe_nodegrid ping tries={str(tries)}")

            conn_obj, ret = _connect()
            if conn_obj and ret == "OK":
                log.debug(f"zpe_nodegrid ping OK")
                fn_ret = True
                break

            tries = tries + 1
            sleep(wait_secs)
            continue

    except Exception as error: # pylint: disable=broad-except
        _do_log_exception(error, "ping")
        return False

    return fn_ret

# Connectivity Functions

def _connect():
    """
    Connect into given proxy target device
    """
    try:
        log.debug("zpe_nodegrid connect DETAILS: " + str(DETAILS))
        return _pexpect_connect(DETAILS["username"], DETAILS["password"], DETAILS["host"])

    except Exception as error: # pylint: disable=broad-except
        _do_log_exception(error, "_connect")
        return None, "Exception: Could not establish connection to proxy target."


def _pexpect_connect(username, password, host):
    # Connection setup
    options = " -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=QUIET"

    cmd = f"ssh {options} {username}@{host}"
    log.debug(f"zpe_nodegrid connect cmd: {cmd}")

    # Start connection
    try:
        # conn_obj = pexpect.spawn(cmd, encoding='UTF-8', timeout=CLI_TIMEOUT)
        conn_obj = pexpect.spawn(cmd, encoding=None, timeout=CLI_TIMEOUT)
        conn_obj.setwinsize(500, 250)

        # Debug purposes only
        # DETAILS["flog"] = open(PLOG, "wb")
        # DETAILS["fsend"] = open(PSLOG, "wb")
        # conn_obj.logfile = DETAILS["flog"]
        # conn_obj.logfile_send = DETAILS["fsend"]

        # Setup CLI Raw output in memory file
        DETAILS["mread"] = BytesIO(b"")
        conn_obj.logfile_read = DETAILS["mread"]

        conn_obj.expect_exact('Password:')
        conn_obj.sendline(password)

    except (pexpect.exceptions.EOF, pexpect.exceptions.TIMEOUT, Exception) as perror:
        _do_log_exception(perror, "_pexpect_connect")
        return None, CONN_ERROR

    if not conn_obj:
        return None, CONN_ERROR

    if _expect(conn_obj) == -1:
        return None, CONN_ERROR

    return conn_obj, "OK"

# Helper Functions

def _sendline(conn_obj, line):
    log.debug("sendline line: [" + line + "]")

    try:
        conn_obj.sendline(line)
    except (pexpect.exceptions.EOF, pexpect.exceptions.TIMEOUT, Exception) as perror:
        _do_log_exception(perror, "_sendline")
        return False

    if _expect(conn_obj) == -1:
        log.error("zpe_nodegrid sendline #2 failed")
        return False
    return True


def _expect(conn_obj):
    try:
        ret = conn_obj.expect_exact(CLI_PROMPT, timeout=CLI_TIMEOUT)
        log.debug("zpe_nodegrid expect ret="+str(ret))
        log.debug("zpe_nodegrid after "  + str(conn_obj.after))
        log.debug("zpe_nodegrid before " + str(conn_obj.before))
        log.debug("zpe_nodegrid mread " + str(DETAILS["mread"].getvalue()))
    except (pexpect.exceptions.EOF, pexpect.exceptions.TIMEOUT, Exception) as perror:
        _do_log_exception(perror, "_pexpect_connect")
        return -1
    return ret


def _receive(buffer, ret, command):
    received = ""
    errors = ""

    if ret == -1:
        errors = errors + "Command failed: " + command + "\n"
        return "", errors

    for line in buffer.splitlines():
        if line != "":
            line.strip().replace("\n", "").replace("\r", "")
            log.debug("zpe_nodegrid receive, line:" + repr(line))
            if "Error: " in line:
                errors = {
                    "command": command,
                    "error": {
                        errors + line + "\n"
                        }
                    }
            received = received + line + "\n"

    log.debug("zpe_nodegrid receive, received:" + str(received))
    log.debug("zpe_nodegrid receive, errors:" + str(errors))
    return received, errors


def _send(conn_obj, command):
    # PERFORMANCE: From shell, we could invoke `cli -f FILE`
    # but we have file transfer constraint on salt
    # so we send line by line
    error = False
    errors = ""
    sent = ""
    received = ""
    buffer = ""

    commands = command.splitlines()
    sent = commands

    if len(commands) > 2:
        for line in commands:
            ret = _sendline(conn_obj, line)
            buffer = str(conn_obj.before)
            rec_aux, err_aux = _receive(buffer, ret, line)
            log.debug("zpe_nodegrid send, rec_aux:" + repr(rec_aux))
            log.debug("zpe_nodegrid send, err_aux:" + repr(err_aux))
            received = received + rec_aux + conn_obj.after
            errors = errors + str(err_aux)
    else:
        ret = _sendline(conn_obj, command)
        buffer = str(conn_obj.before)
        received, errors = _receive(buffer, ret, command)

    log.debug("zpe_nodegrid send, sent:" + str(commands))
    log.debug("zpe_nodegrid send, received:" + str(received))
    log.debug("zpe_nodegrid send, error:" + str(error))

    if errors:
        error = True
    return sent, received, error, errors


def _format_ouput(sent, received, error):
    status = "true" if (error != "") else "false"
    return {
        "result": status,
        "command": sent,
        "out": received,
        "errors": error
    }

def _escapeAnsi(line):
    ansi_escape = re_compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub(' ', line)


def _get_cli_output():
    output = ""
    out = DETAILS["mread"].getvalue().decode('utf-8')
    log.debug("out='"+str(out)+"'")
    # log.debug("out="+repr(out))
    out = out.replace("\rPassword: \r\n", "")
    out = out.replace(" .sessionpageout undefined=no\r\n", "")
    out = out.replace("no\r\r\n", "")

    for line in _escapeAnsi(out).splitlines():
        # log.debug("repr line="+repr(line))
        # log.debug("str  line='"+str(line)+"'")
        if not line.strip():
            continue
        if line.endswith("#]"):
            log.debug("1 removing line='"+repr(line)+"'")
            continue
        if line.endswith("#] "):
            log.debug("2 removing line='"+repr(line)+"'")
            continue
        if repr(line).endswith("#] \x07"):
            log.debug("3 removing line='"+repr(line)+"'")
            continue
        if line.isspace():
            log.debug("4 removing line='"+repr(line)+"'")
            continue
        if not line.isprintable():
            log.debug("5 removing line='"+repr(line)+"'")
            continue
        line, check = subn(CLI_PROMPT_REGEX, " ", line)
        log.debug("_get_cli_output check="+str(check))
        if check > 0:
            continue
        output = output + line.strip() + "\n"
    log.debug("_get_cli_output output="+str(output))
    # log.debug("_get_cli_output repr output="+repr(output))
    return output


def _do_log_exception(error, function=""):
    import traceback
    log.error("Execption: zpe_nodegrid at function " + function + "\n" \
    "Error: " + str(error) + "\n" \
    "Traceback: " + traceback.format_exc())


def _send_cli_command(conn_obj, cli_cmd):
    ret = -1
    # multiple lines
    if len(cli_cmd.splitlines()) > 2:
        log.debug("DEBUG multiline")
        for cmd in cli_cmd.splitlines():
            ret = _sendline(conn_obj, cmd)
    else:
        # single line
        log.debug("DEBUG singleline")
        ret = _sendline(conn_obj, cli_cmd)

    # extra expect to get full buffer output
    _sendline(conn_obj, "\n")
    _expect(conn_obj)

    return ret


def _exec_import_settings(conn_obj, import_settings_list, use_config_start=True):
    """
    Function retrieved from
    zpe.system/collections/ansible_collections/zpe/system/plugins/modules/nodegrid_import.py
    """
    if use_config_start:
        conn_obj.sendline('config_start')
        conn_obj.expect_exact('/]# ')
    conn_obj.sendline("import_settings")
    conn_obj.expect_exact('finish.')
    for item in import_settings_list:
        conn_obj.sendline(item)
        # TODO: Treat possible user errors here
        # Example: send "commit" in between import_settings raises "Error: Invalid line: commit"
    conn_obj.sendcontrol('d')
    conn_obj.expect_exact('/]# ')
    output = conn_obj.before.decode("utf-8")
    if use_config_start:
        conn_obj.sendline('config_confirm')
        conn_obj.expect_exact('/]# ')
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
        output_dict["import_list"] = import_settings_list
        output_dict["import_status"] = import_status
        output_dict["import_status_details"] = import_status_details
    else:
        output_dict["state"] = 'success'
        output_dict["import_list"] = import_settings_list
        output_dict["import_status"] = import_status
        output_dict["import_status_details"] = import_status_details
    log.debug("import_settings output="+str(output))
    log.debug("import_settings output_dict="+str(output_dict))
    log.debug("import_settings import_status_details"+str(import_status_details))

    return output_dict


def _validate_args(kwargs, required_f):
    for field in required_f:
        if field in kwargs:
            continue
        else:
            return False, "Missing required option: " + str(field)
    return True, ""


def _set_optional_bool_field(kwargs, field):
    # Optional, default is no
    value = kwargs.get(field)
    if not value:
        kwargs.__setitem__("absolute_name", "no")
    else:
        kwargs.__setitem__("absolute_name", "yes")


def _file_transfer(file, read=True, cache=True):
    # Get master file here, on minion/proxy

    contents = ""
    minion_file = ""
    error = ""
    found = False

    try:
        # Search file on master repository
        repo_list = __salt__["cp.list_master"]() # pylint: disable=undefined-variable
        log.debug(f"_file_transfer repo_files: {repo_list}")
        for item in repo_list:
            log.debug(f"_file_transfer item: {item}")
            if item in file: # on purpose
                found = True
                break
        if not found:
            return minion_file, contents, "File not found on master's file repository."

        minion_file = __salt__["cp.get_file"](file, MINION_FILE_CACHE) # pylint: disable=undefined-variable
        if not exists(minion_file):
            return None, None, "File transfer failed: Could not find file on minion."

        if read:
            cfile = open(minion_file, "r")
            contents = cfile.read()
            cfile.close()

        if not cache:
            log.debug(f"_file_transfer remove cache file, cache={cache}")
            remove(minion_file)

    except FileNotFoundError:
        return None, None, "Error: File not found."
    except OSError as err:
        _do_log_exception(err, "_file_transfer")
        if "No space left on device" in str(error):
            return None, None, "No space left on device [minion]"
    except Exception as err:
        _do_log_exception(err, "_file_transfer")
        return None, None, "An exception occured during file transfer to [minion]"

    return minion_file, contents, error


def _file_transfer_target(file, target_dest, cache=True):

    minion_file, contents, error = _file_transfer(file, False, True) # pylint: disable=unused-variable
    if error:
        return error

    try:
        options = " -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
        cmd = f"scp {options} {minion_file} " + \
            DETAILS["username"] + "@" + DETAILS["host"] + ":" + target_dest
        log.debug("zpe_nodegrid scp cmd = " + str(cmd))

        conn_obj = pexpect.spawn(cmd, encoding="utf-8", timeout=CLI_TIMEOUT)

        ret = conn_obj.expect_exact(['Password:', pexpect.EOF])
        if ret == 0:
            conn_obj.sendline(DETAILS["password"])
            conn_obj.expect_exact(pexpect.EOF)
        elif ret == 1:
            log.error("zpe_nodegrid cp_file scp EOF")
            return False

        log.debug("zpe_nodegrid scp ret = " + str(ret))
        if ret == 1:
            log.error("zpe_nodegrid cp_file scp TIMED OUT")
            return False

        buffer = str(conn_obj.before) + str(conn_obj.after)
        log.debug("zpe_nodegrid scp buffer = " + buffer)
        for line in buffer.splitlines():
            ltest = line.lower()
            if "error" in ltest or \
                "failed" in ltest or \
                "denied" in ltest or \
                "no space left on device" in ltest:
                return "File transfer to target failed: " + line.strip()

        if not cache:
            remove(minion_file)

    except (pexpect.exceptions.EOF, pexpect.exceptions.TIMEOUT, Exception) as perror:
        _do_log_exception(perror, "cp_file")
        return False

    # Check file transfer to destination minion/proxy
    check = __proxy__["nodegrid.cli_shell"]("ls -l " + target_dest + file.split("/")[-1]) # pylint: disable=undefined-variable
    log.debug("zpe_nodegrid run scp ret = " + check)
    if "No such file or directory" in check:
        return "File transfer failed: Could not find file on target: " + DETAILS["host"]
    else:
        return True


# Module Functions

def ping_icmp(**kwargs):
    log.debug("PROXY zpe_nodegrid ping_icmp kwargs = " + str(kwargs))

    tries = 1
    response = 1
    fn_ret = False
    retries = kwargs.get("retries", 5)
    wait_secs = kwargs.get("wait_secs", 2)

    try:
        while (tries <= retries):
            response = system("ping -q -W 1 -c 1 " + DETAILS["host"])
            log.debug(f"zpe_nodegrid ping_icmp tries={str(tries)}, response={str(response)}")

            if response == 0:
                return True
            else:
                tries = tries + 1
                sleep(wait_secs)
                continue

    except Exception as error: # pylint: disable=broad-except
        _do_log_exception(error, "ping_icmp")
        return False

    return fn_ret


def check_version(desired_version):
    """
    Check device version against given desired version.

    Returns boolean, False is returned along with current device version.

    CLI Example:
    .. code-block:: bash
        salt '*' nodegrid.check_version 5.6.9
    """
    log.debug("PROXY zpe_nodegrid check_version")
    log.debug("desired_version: ["+ str(desired_version) +"]")

    ret = False
    current_version = ""
    version_reg = r"software: v(\d+\.\d+\.\d+)"

    output = __proxy__["nodegrid.get_system_about"]()
    if not output:
        return False

    log.debug("check_version output = " +repr(output))
    match = search(version_reg, output)

    if match:
        current_version = match.group(1)
        if current_version == desired_version:
            # version we want
            ret = True
        else:
            ret = False
    else:
        return False

    return (ret,
            current_version
    )


def cli(command, **kwargs): # pylint: disable=unused-argument
    """
    Returns raw CLI output of the command passed as argument.
    In case of error, returns CLI error message.

    command
        Command to be executed on the device.

    CLI Example:
    .. code-block:: bash
        salt '*' nodegrid.cli "show /system/about"
        salt '*' nodegrid.cli "show /settings/license"
        salt '*' nodegrid.cli "show /settings/devices"
        salt '*' nodegrid.cli "reboot --force"
        salt '*' nodegrid.cli "cd /settings/system_preferences/
        set idle_timeout=3600
        set enable_banner=yes
        commit"
        salt '*' nodegrid.cli "cd /settings/license
        add
        set license_key=LICENSE
        commit
        cancel"
        "
    """
    try:
        log.debug("PROXY zpe_nodegrid CLI")
        log.debug("command: ["+ str(command) +"]")
        log.debug("kwargs: ["+ str(kwargs) +"]")

        output = ""
        error = False

        conn_obj, ret = _connect()
        if not conn_obj:
            return ret

        ret = _send_cli_command(conn_obj, '.sessionpageout undefined=no')

        ret = _send_cli_command(conn_obj, command)

        if ret == -1:
            return False

        output = _get_cli_output()

        shutdown(conn_obj)
        return output

    except Exception as error: # pylint: disable=broad-except
        _do_log_exception(error, "cli")
        return False


def cli_file(file, **kwargs): # pylint: disable=unused-argument
    """
    Returns a raw CLI output of the commands on the file passed as argument.
    In case of error, returns CLI error message.

    file
        File with CLI Commands to be executed on the device.
        Located at salt-master file_roots, default: /srv/salt/
        Example: /srv/salt/cli/file.cli

    File Example:
    .. code-block:: bash
        $ cat /path/to/file.cli
        cd /settings/system_preferences/
        set idle_timeout=3600
        commit
        cancel
        cd /settings/license
        add
        set license_key="LICENSE"
        commit
        cancel

    CLI Example:
    .. code-block:: bash
        salt '*' nodegrid.cli salt://cli/file.cli
    """

    try:
        log.debug("PROXY zpe_nodegrid CLI_FILE")
        log.debug("file: ["+ str(file) +"]")
        log.debug("kwargs: ["+ str(kwargs) +"]")

        minion_file, cli_cmd, error = _file_transfer(file, read=True, cache=True)
        if cli_cmd:
            return __proxy__["nodegrid.cli"](cli_cmd)    # pylint: disable=undefined-variable
        elif error:
            return error

    except Exception as error: # pylint: disable=broad-except
        _do_log_exception(error, "cli_file")
        return False


def cli_shell(command):
    """
    Execute given command in user shell.

    Returns raw CLI output of the command passed as argument.

    CLI Example:
    .. code-block:: bash
        salt '*' nodegrid.cli_shell "ls /var/sw"
    """
    pre_command = "shell\n"
    cmd = pre_command + command
    return __proxy__["nodegrid.cli"](cmd)


def cli_root_shell(command):
    """
    Execute given command in root shell.

    Returns raw CLI output of the command passed as argument.

    CLI Example:
    .. code-block:: bash
        salt '*' nodegrid.cli_root_shell "ls /var/sw"
    """
    pre_command = "shell sudo su -\n"
    cmd = pre_command + command
    return __proxy__["nodegrid.cli"](cmd)


def import_settings(command, **kwargs):
    """
    Returns boolean of CLI import_settings procedure of the given CLI exported data.

    command
        CLI import_settings formatted commands to be imported on the device.

    CLI Example:
    .. code-block:: bash
    salt '*' nodegrid.import_settings "/settings/system_preferences idle_timeout=3600
/settings/system_preferences idle_timeout=1234"
    """
    log.debug("PROXY zpe_nodegrid import_settings")
    log.debug("command: ["+ str(command) +"]")
    log.debug("kwargs: ["+ str(kwargs) +"]")
    conn_obj, ret = _connect()
    if not conn_obj:
        return ret

    import_settings_list = []
    # parse command to be a list
    for item in command.splitlines():
        import_settings_list.append(item)

    output_dict = _exec_import_settings(conn_obj, import_settings_list, True)

    if output_dict["import_status"] == "succeeded":
        log.debug("PROXY zpe_nodegrid returning True")
        return True

    log.debug("PROXY zpe_nodegrid returning False")
    return False


def import_settings_file(file, **kwargs):
    """
    Returns boolean of CLI import_settings procedure of the given file with CLI exported data.

    file
        File with CLI import_settings formatted commands to be imported on the device.
        Located at salt-master file_roots, default: /srv/salt/
        Example: /srv/salt/cli/file.cli

    File Example:
    .. code-block:: bash
        $ cat /path/to/import.cli
        /settings/system_preferences idle_timeout=3600
        /settings/system_preferences show_hostname_on_webui_header=yes

    CLI Example:
    .. code-block:: bash
    salt '*' nodegrid.import_settings_file salt://cli/import.cli
    """
    log.debug("PROXY zpe_nodegrid import_settings_file")
    log.debug("file: ["+ str(file) +"]")
    log.debug("kwargs: ["+ str(kwargs) +"]")

    conn_obj, ret = _connect()
    if not conn_obj:
        return ret

    minion_file, contents, error = _file_transfer(file, read=True, cache=False) # pylint: disable=unused-variable
    if contents:
        return __proxy__["nodegrid.import_settings"](contents) # pylint: disable=undefined-variable
    elif error:
        return error


def export_settings(path, **kwargs):
    """
    Returns raw CLI output of export_settings procedure on the given CLI path.

    path
        CLI path to get exporte and get the data from.

    CLI Example:
    .. code-block:: bash
    salt '*' nodegrid.export_settings "/settings/system_preferences"
    """
    log.debug("PROXY zpe_nodegrid export_settings")
    log.debug("path: ["+ str(path) +"]")
    log.debug("kwargs: ["+ str(kwargs) +"]")
    conn_obj, ret = _connect()
    if not conn_obj:
        return ret

    output = ""

    conn_obj, ret = _connect()
    if not conn_obj:
        return ret

    ret = _send_cli_command(conn_obj, "export_settings " + path)
    # TODO: remove lines that contains only CLI_PROMPT
    # Example: last couple lines

    if ret == -1:
        return False

    output = _get_cli_output()

    shutdown(conn_obj)
    return output


def get_system_about():
    """
    Returns raw CLI output of the command: `show /system/about`
    CLI Example:
    .. code-block:: bash
        salt '*' nodegrid.get_system_about
    """
    return __proxy__["nodegrid.cli"](    # pylint: disable=undefined-variable
        "show /system/about"
    )


def add_license(lic_key):
    """
    Returns True if CLI procedure of adding given license is successfull.
    In case of error, returns CLI error message.
    CLI Example:
    .. code-block:: bash
        salt '*' nodegrid.add_license LICENSE_KEY
    """
    ret = __proxy__["nodegrid.cli"](    # pylint: disable=undefined-variable
        "cd /settings/license; add; set license_key="+lic_key+"; commit"
    )
    if not "Error" in ret:
        return True
    return ret


def save_settings(**kwargs):
    """
    Returns True if CLI procedure of save_settings with the given options is successfull.
    In case of error, returns CLI error message.

    :param destination: Where to save the backup file (local_system or remote_server)
    :param filename: (local_system) name or the absolute_path of the backup file (/backup/filename)
    :param url: (remote_server) Remote server url to get backup file
    :param username: (remote_server) Name or the absolute_path of the backup file
    :param password: (remote_server) Name or the absolute_path of the backup file
    :param absolute_name: (remote_server) Boolean. The path in url to be used as absolute path name
    :return: Boolean. Procedure status:

    CLI Example:
    .. code-block:: bash
    salt '*' nodegrid.save_settings destination=local_system filename=backup.cfg
    salt '*' nodegrid.save_settings destination=remote_server url=ftp://SERVER_IP/filepath username=ftpuser password=ftpuser absolute_name=True
    """

    log.debug("PROXY zpe_nodegrid save_settings")
    log.debug("kwargs: ["+ str(kwargs) +"]")

    cmd = ""
    local_system = ["filename"]
    remote_server = ["url", "username", "password"]

    # Mandatory check
    destination = kwargs.get("destination")
    if not destination:
        return "Missing required option: destination"

    if destination == "local_system":
        ret, msg = _validate_args(kwargs, local_system)
        if not ret:
            return msg
    elif destination == "remote_server":
        ret, msg = _validate_args(kwargs, remote_server)
        if not ret:
            return msg
    else:
        return "Required option [destination] should be either 'local_system' or 'remote_server', received '" + str(destination) + "'"

    if destination == "local_system":
        cmd = "save_settings\nset destination=local_system" + \
            "\nset filename="+kwargs["filename"]+"\ncommit"
    if destination == "remote_server":
        _set_optional_bool_field(kwargs, "absolute_name")
        cmd = "save_settings\nset destination=remote_server" + \
            "\nset url="+kwargs["url"]+"\nset username="+kwargs["username"] + \
            "\nset password="+kwargs["password"] + \
            "\nset the_path_in_url_to_be_used_as_absolute_path_name="+kwargs["absolute_name"] + \
            "\ncommit"

    log.debug("save_settings cmd="+str(cmd))
    log.debug("save_settings cmd="+str(cmd))
    if cmd:
        ret = __proxy__["nodegrid.cli"](cmd)    # pylint: disable=undefined-variable
        if not "Error" in ret:
            return True
        return ret

    return False


def apply_settings(**kwargs):
    """
    Returns True if CLI procedure of apply_settings with the given options is successfull.
    In case of error, returns CLI error message.

    :param from_destination: Where to get the backup file (local_system or remote_server)
    :param filename: (local_system) name or the absolute_path of the backup file (/backup/filename)
    :param url: (remote_server) Remote server url to get backup file
    :param username: (remote_server) Name or the absolute_path of the backup file
    :param password: (remote_server) Name or the absolute_path of the backup file
    :param absolute_name: (remote_server, optional, boolean) The path in url to be used as absolute path name
    :return: Boolean or Error of Procedure:

    CLI Example:
    .. code-block:: bash
    salt '*' nodegrid.apply_settings destination=local_system filename=backup.cfg
    salt '*' nodegrid.apply_settings destination=remote_server url=ftp://SERVER_IP/filepath username=ftpuser password=ftpuser
    """

    log.debug("PROXY zpe_nodegrid apply_settings")
    log.debug("kwargs: ["+ str(kwargs) +"]")

    cmd = ""
    local_system = ["filename"]
    remote_server = ["url", "username", "password"]

    # Mandatory check
    from_destination = kwargs.get("from_destination")
    if not from_destination:
        return "Missing required option: from_destination"

    if from_destination == "local_system":
        ret, msg = _validate_args(kwargs, local_system)
        if not ret:
            return msg
    elif from_destination == "remote_server":
        ret, msg = _validate_args(kwargs, remote_server)
        if not ret:
            return msg
    else:
        return "Required option [from_destination] should be either 'local_system' or 'remote_server', received '" + str(from_destination) + "'"

    if from_destination == "local_system":
        cmd = "apply_settings\nset from=local_system" + \
            "\nset filename="+kwargs["filename"] + \
            "\napply\nyes"
    if from_destination == "remote_server":
        _set_optional_bool_field(kwargs, "absolute_name")
        cmd = "apply_settings\nset from=remote_server" + \
            "\nset url="+kwargs["url"]+"\nset username="+kwargs["username"] + \
            "\nset password="+kwargs["password"] + \
            "\nset the_path_in_url_to_be_used_as_absolute_path_name="+kwargs["absolute_name"] + \
            "\napply\nyes"

    log.debug("apply_settings cmd="+str(cmd))
    log.debug("apply_settings cmd="+str(cmd))
    if cmd:
        ret = __proxy__["nodegrid.cli"](cmd)    # pylint: disable=undefined-variable
        if not "Error" in ret:
            return True
        return ret

    return False


def cp_file(file, destination, **kwargs):
    """
    Returns True if transfer is successfull or Error message in case of failure.

    Get file from master using salt.cp.get_file
    Transfer file from minion to target using SCP

    file
        File with CLI Commands to be executed on the device.
        Located at salt-master file_roots, default: /srv/salt/
        Example: /srv/salt/file.txt
    destination
        Path on target device to transfer file

    CLI Example:
    .. code-block:: bash
    salt nodegrid_host nodegrid.cp_file salt://file.txt /tmp/
    """

    log.debug("PROXY zpe_nodegrid cp_file")
    log.debug("file: ["+ str(file) +"]")
    log.debug("destination: ["+ str(destination) +"]")

    conn_obj, ret = _connect()
    if not conn_obj:
        return ret

    # Send minion file to target device using scp
    if not destination.endswith("/"):
        destination = destination + "/"
    return _file_transfer_target(file, destination, cache=True)


def change_default_password(**kwargs):
    """
    Returns True if default password was changed successfully.

    Launch SSH and Change password to the pillar file password
    Validate if changed to pillar password
    """

    options = " -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
    username = DETAILS["username"]
    host = DETAILS["host"]
    cmd = f"ssh {options} {username}@{host}"
    log.debug(f"zpe_nodegrid change_default_password cmd: {cmd}")

    try:
        conn_obj = pexpect.spawn(cmd, encoding="utf-8")

        conn_obj.expect_exact('Password:')
        conn_obj.sendline("admin")
        conn_obj.expect_exact('Current password:', timeout=10)
        conn_obj.sendline("admin")
        conn_obj.expect_exact('New password:', timeout=10)
        conn_obj.sendline(DETAILS["password"])
        conn_obj.expect_exact('Retype new password:', timeout=10)
        conn_obj.sendline(DETAILS["password"])
        # Just try to capture CLI prompt, if not possible, continue
        ret = conn_obj.expect_exact([']#', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
        if ret == 0:
            log.debug("Could not find CLI prompt after password change.")
        conn_obj.sendline("exit")

        conn_obj, ret = _connect()
        if not ret:
            return (False, "Could not login after password change")

    except (pexpect.exceptions.EOF, pexpect.exceptions.TIMEOUT, Exception) as perror:
        # treat already changed password
        conn_obj, ret = _connect()
        if "OK" in ret:
            return (True, "The password was already changed")
        # treat exception
        _do_log_exception(perror, "_pexpect_connect")
        err = "Error: " + str(perror).splitlines()[0]
        if "Timeout" in err:
            return (False, "Timeout error, please check device credentials")
        return (False, err)

    return (True, "The password has been changed succesfully")


def software_upgrade(**kwargs):
    """
    Returns True if CLI procedure of apply_settings with the given options is successfull.
    In case of error, returns CLI error message.

    :param image_location: Where to get the firmware file (local_system or remote_server)
    :param filename: (local_system) name or the absolute_path of the backup file (/backup/filename)
    :param url: (remote_server) Remote server url to get backup file
    :param username: (remote_server) Name or the absolute_path of the backup file
    :param password: (remote_server) Name or the absolute_path of the backup file
    :param absolute_name: (remote_server, optional) The path in url to be used as absolute path name
    :param format_partitions_before_upgrade: (remote_server, optional, boolean) The path in url to be used as absolute path name
    :param force_boot_mode: (remote_server, optional, boolean) The path in url to be used as absolute path name
    :param if_downgrading: (remote_server, optional, boolean) The path in url to be used as absolute path name
        - apply_factory_default_configuration
        - restore_configuration_saved_on_version_upgrade
    :return: Boolean or Error of Procedure:

    CLI Example:
    .. code-block:: bash
    salt '*' nodegrid.software_upgrade image_location=local_system filename=Nodegrid_Platform_v5.6.9_20230111.iso --timeout 30
    salt '*' nodegrid.software_upgrade destination=remote_server url=ftp://SERVER_IP/Nodegrid_Platform_v5.6.9_20230111.iso username=ftpuser password=ftpuser --timeout 30
    """

    log.debug("PROXY zpe_nodegrid software_upgrade")
    log.debug("kwargs: ["+ str(kwargs) +"]")
    log.debug("kwargs: ["+ str(kwargs) +"]")

    cmd = ""
    cmd_optional = ""
    cmd_commit = "\nupgrade"
    fn_ret = False

    mandatory_field = "image_location"
    local_system = ["filename"]
    remote_server = ["url", "username", "password"]
    global_optional_bool = ["format_partitions_before_upgrade", "force_boot_mode"]

    # Mandatory check
    image_location = kwargs.get(mandatory_field)
    if not image_location:
        return "Missing required option: " + str(mandatory_field)

    if image_location == "local_system":
        ret, msg = _validate_args(kwargs, local_system)
        if not ret:
            return msg
    elif image_location == "remote_server":
        ret, msg = _validate_args(kwargs, remote_server)
        if not ret:
            return msg
    else:
        return "Required option ["+mandatory_field+"] should be either 'local_system' or 'remote_server', received '" + str(image_location) + "'"

    for field in global_optional_bool:
        arg = kwargs.get(field)
        if not arg:
            kwargs.__setitem__(field, "no")
        else:
            kwargs.__setitem__(field, "yes")
        cmd_optional = cmd_optional + "set " + field + "=" + kwargs[field] + "\n"

    arg = kwargs.get("if_downgrading")
    if arg:
        cmd_optional = cmd_optional + "set if_downgrading" + "=" + kwargs["if_downgrading"] + "\n"
    else:
        cmd_optional = cmd_optional + "set if_downgrading" + "=restore_configuration_saved_on_version_upgrade\n"

    if image_location == "local_system":
        cmd = "software_upgrade\nset image_location=local_system" + \
            "\nset filename="+kwargs["filename"] + "\n"
    if image_location == "remote_server":
        _set_optional_bool_field(kwargs, "absolute_name")

        cmd = "software_upgrade\nset image_location=remote_server" + \
            "\nset url="+kwargs["url"]+"\nset username="+kwargs["username"] + \
            "\nset password="+kwargs["password"] + \
            "\nset the_path_in_url_to_be_used_as_absolute_path_name="+kwargs["absolute_name"] + "\n"

    if cmd:
        log.debug("software_upgrade cmd_optional="+str(cmd_optional))
        cmd = cmd + cmd_optional
        cmd = cmd + cmd_commit
        log.debug("software_upgrade cmd="+str(cmd))
        ret = __proxy__["nodegrid.cli"](cmd)    # pylint: disable=undefined-variable
        if "The system is going down for reboot NOW" in ret:
            fn_ret = True
        if not "Error" in ret:
            fn_ret = True
        else:
            return ret

    wait = kwargs.get("wait", True)
    log.debug(f"software_upgrade wait={wait}")

    if wait:
        # Make sure device is down first
        while not __proxy__["nodegrid.ping_icmp"](**kwargs):
            log.debug("software_upgrade waiting reboot...")
            sleep(4)

        log.debug("software_upgrade is now rebooting...")

        # set default opts if not present
        retries = kwargs.get("retries", 150)
        wait_secs = kwargs.get("wait_secs", 5)
        kwargs.__setitem__("retries", retries)
        kwargs.__setitem__("wait_secs", wait_secs)
        # now wait software upgrade proccess using ping
        log.debug("software_upgrade ping opts="+str(kwargs))
        ret = __proxy__["nodegrid.ping_icmp"](**kwargs)
        log.debug("software_upgrade ping_icmp ret="+str(ret))
        if (kwargs.get("format_partitions_before_upgrade") == "yes"):
            log.debug("software_upgrade reformat yes, try change default password")
            ret = __proxy__["nodegrid.change_default_password"](**kwargs)
            log.debug("software_upgrade reformat - change_default_password ret = " + str(ret))

        fn_ret = __proxy__["nodegrid.ping"](**kwargs)

    return fn_ret

