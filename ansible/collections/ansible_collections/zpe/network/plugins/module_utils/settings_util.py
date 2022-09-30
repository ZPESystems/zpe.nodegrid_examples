def get_module_params():
    module_args = dict(
        # state=dict(type='str', choices=['up', 'down', 'exist', 'absent'], required=False, default='exist'),
        hostname=dict(type='str', required=False, default='nodegrid'),
        domain_name=dict(type='str', required=False, default='localdomain'),
        dns_proxy=dict(type='str', required=False),
        enable_ipv4_ip_forward=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
        enable_ipv6_ip_forward=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
        ipv4_loopback=dict(type='str', required=False),
        ipv6_loopback=dict(type='str', required=False),
        reverse_path_filtering=dict(type='str', choices=['disabled', 'loose_mode', 'strict_mode'], required=False,
                                    default='strict_mode'),
        enable_multiple_routing_tables=dict(type='str', choices=['yes', 'no'], required=False, default='yes'),
        enable_dynamic_dns=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
        ddns_server_name=dict(type='str', required=False),
        ddns_server_tcp_port=dict(type='str', required=False, default='53'),
        zone=dict(type='str', required=False),
        failover_hostname=dict(type='str', required=False),
        username=dict(type='str', required=False),
        algorithm=dict(type='str',
                       choices=['HMAC-MD5', 'HMAC-SHA1', 'HMAC-SHA224', 'HMAC-SHA256', 'HMAC-SHA384', 'HMAC-SHA512'],
                       required=False, default='HMAC-MD5'),
        key_size=dict(type='str', required=False, default='512'),
        enable_bluetooth_network=dict(type='str', choices=['yes', 'no'], required=False, default='yes')
    )

    return module_args


def get_nodegrid_dict():
    nodegrid_keys = dict(
        hostname=dict(
            ansible_name="hostname",
            cli_name="hostname",
            cli_default="nodegrid",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        ),
        domain_name=dict(
            ansible_name="domain_name",
            cli_name="domain_name",
            cli_default="localdomain",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        ),
        dns_proxy=dict(
            ansible_name="dns_proxy",
            cli_name="dns_proxy",
            cli_default="",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        ),
        enable_ipv4_ip_forward=dict(
            ansible_name="enable_ipv4_ip_forward",
            cli_name="enable_ipv4_ip_forward",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        ),
        enable_ipv6_ip_forward=dict(
            ansible_name="enable_ipv6_ip_forward",
            cli_name="enable_ipv6_ip_forward",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        ),
        ipv4_loopback=dict(
            ansible_name="ipv4_loopback",
            cli_name="ipv4_loopback",
            cli_default="",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        ),
        ipv6_loopback=dict(
            ansible_name="ipv6_loopback",
            cli_name="ipv6_loopback",
            cli_default="",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        ),
        reverse_path_filtering=dict(
            ansible_name="reverse_path_filtering",
            cli_name="reverse_path_filtering",
            cli_default="strict_mode",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        ),
        enable_multiple_routing_tables=dict(
            ansible_name="enable_multiple_routing_tables",
            cli_name="enable_multiple_routing_tables",
            cli_default="yes",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        ),
        enable_dynamic_dns=dict(
            ansible_name="enable_dynamic_dns",
            cli_name="enable_dynamic_dns",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        ),
        ddns_server_name=dict(
            ansible_name="ddns_server_name",
            cli_name="ddns_server_name",
            cli_default="",
            parent=True,
            parent_ansible_name="enable_dynamic_dns",
            parent_value=['yes'],
            import_template = "/settings/network_settings {cli_name}={value}"
        ),
        ddns_server_tcp_port = dict(
            ansible_name="ddns_server_tcp_port",
            cli_name="ddns_server_tcp_port",
            cli_default="53",
            parent=True,
            parent_ansible_name="enable_dynamic_dns",
            parent_value=['yes'],
            import_template = "/settings/network_settings {cli_name}={value}"
        ),
        zone = dict(
            ansible_name="zone",
            cli_name="zone",
            cli_default="",
            parent=True,
            parent_ansible_name="enable_dynamic_dns",
            parent_value=['yes'],
            import_template = "/settings/network_settings {cli_name}={value}"
        ),
        failover_hostname = dict(
            ansible_name="failover_hostname",
            cli_name="failover_hostname",
            cli_default="",
            parent=True,
            parent_ansible_name="enable_dynamic_dns",
            parent_value=['yes'],
            import_template = "/settings/network_settings {cli_name}={value}"
        ),
        username = dict(
            ansible_name="username",
            cli_name="username",
            cli_default="",
            parent=True,
            parent_ansible_name="enable_dynamic_dns",
            parent_value=['yes'],
            import_template = "/settings/network_settings {cli_name}={value}"
        ),
        algorithm = dict(
            ansible_name="algorithm",
            cli_name="algorithm",
            cli_default="HMAC-MD5",
            parent=True,
            parent_ansible_name="enable_dynamic_dns",
            parent_value=['yes'],
            import_template = "/settings/network_settings {cli_name}={value}"
        ),
        key_size = dict(
            ansible_name="key_size",
            cli_name="key_size",
            cli_default="512",
            parent=True,
            parent_ansible_name="enable_dynamic_dns",
            parent_value=['yes'],
            import_template = "/settings/network_settings {cli_name}={value}"
        ),
        enable_bluetooth_network = dict(
            ansible_name="enable_bluetooth_network",
            cli_name="enable_bluetooth_network",
            cli_default="yes",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_settings {cli_name}={value}"
        )
    )
    return nodegrid_keys
