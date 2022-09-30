import pexpect

def get_nodegrid_os_details():
    cmd = "cli -c show /system/about"
    output = pexpect.run(cmd)
    output = output.decode('UTF-8').strip()
    output_dict = {}
    if "Error" in output or "error" in output:
        if "Error: Invalid argument:" in output:
            output_dict["error"] = "Error getting system information"
        else:
            output_dict["error"] = output
    for line in output.splitlines():
        if ":" in line:
            # output_dict[line] = line.split(':',1)
            key, value = line.split(':', 1)
            if key == 'software':
                version_details, version_dates = value.split('(', 1)
                output_dict['version_dates'] = version_dates.replace(')', '').strip()
                majorversion, minorversion, subversion = version_details.split('.')
                output_dict['software_major'] = majorversion.replace('v', '').strip()
                output_dict['software_minor'] = minorversion.strip()
                output_dict['software_sub'] = subversion.strip()
            output_dict[key.strip()] = value.strip()
    return output_dict
