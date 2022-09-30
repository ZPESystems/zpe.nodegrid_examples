def get_module_params():
    module_args = dict(
            address_location=dict(type='str', required=False),
            coordinates=dict(type='str', required=False),
            help_url=dict(type='str', required=False, default='https://www.zpesystems.com/ng/v5_6/NodegridManual5.6.html'),
            idle_timeout=dict(type='str', required=False, default='300'),
            revision_tag=dict(type='str', required=False, default='r1'),
            show_hostname_on_webui_header=dict(type='str', choices=['yes', 'no'], required=False, default='yes'),
#            webui_header_hostname_color=dict(type='str', required=False, default='#000000'),
            logo_image=dict(type='str', choices=['remote_server', 'use_default_logo_image'], required=False, default='use_default_logo_image'),
            logo_download_url=dict(type='str', required=False),
            logo_download_username=dict(type='str', required=False),
            logo_download_password=dict(type='str', required=False),
            logo_download_path_is_absolute_path_name=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
            enable_banner=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
            banner=dict(type='str', required=False, default='"WARNING: This private system is provided for authorized use only and it may be \r\nmonitored for all lawful purposes to ensure its use. All information\r\nincluding personal information, placed on or sent over this system may be\r\nmonitored and recorded. Use of this system, authorized or unauthorized,\r\nconstitutes consent to monitoring your session. Unauthorized use may \r\nsubject you to criminal prosecution. Evidence of any such unauthorized\r\nuse may be used for administrative, criminal and/or legal actions.\r\n"'),
            enable_license_utilization_rate=dict(type='str', choices=['yes', 'no'], required=False, default='yes'),
            percentage_to_trigger_events=dict(type='str', required=False, default='90'),
            unit_ipv4_address=dict(type='str', required=False, default='192.168.160.1'),
            unit_netmask=dict(type='str', required=False, default='255.255.255.0'),
            unit_interface=dict(type='str', required=False, default='eth0'),
            iso_url=dict(type='str', required=False, default='http://ServerIPAddress/PATH/FILENAME.ISO'),
#            allow_sata_card_in_slot_5=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
            console_port_speed=dict(type='str', choices=['115200', '19200', '38400', '57600', '9600'], required=False, default='115200'),
#            enable_alarm_sound_on_fan_failure=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
            enable_alarm_sound_when_one_power_supply_is_powered_off=dict(type='str', choices=['yes', 'no'], required=False, default='yes'),
            enable_local_serial_ports_utilization_rate=dict(type='str', choices=['yes', 'no'], required=False, default='no')
    )
    return module_args

def get_nodegrid_dict():
    nodegrid_keys = dict(
        address_location=dict(
            ansible_name="address_location",
            cli_name="address_location",
            cli_default="",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        coordinates=dict(
            ansible_name="coordinates",
            cli_name="coordinates",
            cli_default="",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        help_url=dict(
            ansible_name="help_url",
            cli_name="help_url",
            cli_default="https://www.zpesystems.com/ng/v5_6/NodegridManual5.6.html",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        idle_timeout=dict(
            ansible_name="idle_timeout",
            cli_name="idle_timeout",
            cli_default="300",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        revision_tag=dict(
            ansible_name="revision_tag",
            cli_name="revision_tag",
            cli_default="r1",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        show_hostname_on_webui_header=dict(
            ansible_name="show_hostname_on_webui_header",
            cli_name="show_hostname_on_webui_header",
            cli_default="yes",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        webui_header_hostname_color=dict(
            ansible_name="webui_header_hostname_color",
            cli_name="webui_header_hostname_color",
            cli_default="#000000",
            parent=True,
            parent_ansible_name="show_hostname_on_webui_header",
            parent_value=['yes'],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        logo_image=dict(
            ansible_name="logo_image",
            cli_name="logo_image",
            cli_default="use_default_logo_image",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        logo_download_url=dict(
            ansible_name="logo_download_url",
            cli_name="logo_download_url",
            cli_default="",
            parent=True,
            parent_ansible_name="logo_image",
            parent_value=['remote_server'],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        logo_download_username=dict(
            ansible_name="logo_download_username",
            cli_name="logo_download_username",
            cli_default="",
            parent=True,
            parent_ansible_name="logo_image",
            parent_value=['remote_server'],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        logo_download_password=dict(
            ansible_name="logo_download_password",
            cli_name="logo_download_password",
            cli_default="",
            parent=True,
            parent_ansible_name="logo_image",
            parent_value=['remote_server'],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        logo_download_path_is_absolute_path_name=dict(
            ansible_name="logo_download_path_is_absolute_path_name",
            cli_name="logo_download_path_is_absolute_path_name",
            cli_default="no",
            parent=True,
            parent_ansible_name="logo_image",
            parent_value=['remote_server'],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        enable_banner=dict(
            ansible_name="enable_banner",
            cli_name="enable_banner",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        banner=dict(
            ansible_name="banner",
            cli_name="banner",
            cli_default="WARNING: This private system is provided for authorized use only and it may be \r\nmonitored for all lawful purposes to ensure its use. All information\r\nincluding personal information, placed on or sent over this system may be\r\nmonitored and recorded. Use of this system, authorized or unauthorized,\r\nconstitutes consent to monitoring your session. Unauthorized use may \r\nsubject you to criminal prosecution. Evidence of any such unauthorized\r\nuse may be used for administrative, criminal and/or legal actions. \r\n\r\n",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        enable_license_utilization_rate=dict(
            ansible_name="enable_license_utilization_rate",
            cli_name="enable_license_utilization_rate",
            cli_default="yes",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        percentage_to_trigger_events=dict(
            ansible_name="percentage_to_trigger_events",
            cli_name="percentage_to_trigger_events",
            cli_default="90",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        unit_ipv4_address=dict(
            ansible_name="unit_ipv4_address",
            cli_name="unit_ipv4_address",
            cli_default="192.168.160.1",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        unit_netmask=dict(
            ansible_name="unit_netmask",
            cli_name="unit_netmask",
            cli_default="255.255.255.0",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        unit_interface=dict(
            ansible_name="unit_interface",
            cli_name="unit_interface",
            cli_default="eth0",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        iso_url=dict(
            ansible_name="iso_url",
            cli_name="iso_url",
            cli_default="http://ServerIPAddress/PATH/FILENAME.ISO",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        allow_sata_card_in_slot_5=dict(
            ansible_name="allow_sata_card_in_slot_5",
            cli_name="allow_sata_card_in_slot_5",
            cli_default="",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        console_port_speed=dict(
            ansible_name="console_port_speed",
            cli_name="console_port_speed",
            cli_default="115200",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        enable_alarm_sound_on_fan_failure=dict(
            ansible_name="enable_alarm_sound_on_fan_failure",
            cli_name="enable_alarm_sound_on_fan_failure",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        enable_alarm_sound_when_one_power_supply_is_powered_off=dict(
            ansible_name="enable_alarm_sound_when_one_power_supply_is_powered_off",
            cli_name="enable_alarm_sound_when_one_power_supply_is_powered_off",
            cli_default="yes",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
        enable_local_serial_ports_utilization_rate=dict(
            ansible_name="enable_local_serial_ports_utilization_rate",
            cli_name="enable_local_serial_ports_utilization_rate",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/system_preferences/ {cli_name}={value}"
        ),
    )
    return nodegrid_keys
