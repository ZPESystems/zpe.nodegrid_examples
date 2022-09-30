def get_module_params():
    module_args = dict(
        state=dict(type='str', choices=['up', 'down', 'exist', 'absent'], required=False, default='exist'),
        connection_name=dict(type='str', required=True),
        connection_type=dict(type='str',
                             choices=['analog_modem', 'bridge', 'loopback', 'pppoe', 'wifi', 'bonding', 'ethernet',
                                      'mobile_broadband_gsm', 'vlan'], required=False, default='ethernet'),
        set_as_primary_connection=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
        block_unsolicited_incoming_packets=dict(type='str', choices=['yes', 'no'], required=False),
        connect_automatically=dict(type='str', choices=['yes', 'no'], default='yes'),
        ipv4_mode=dict(type='str', choices=['no_ipv4_address', 'dhcp', 'static'], required=False, default='dhcp'),
        ipv4_address=dict(type='str', required=False),
        ipv4_bitmask=dict(type='str', required=False),
        ipv4_dns_server=dict(type='str', required=False),
        ipv4_gateway=dict(type='str', required=False),
        ipv4_default_route_metric=dict(type='str', required=False, default='100'),
        ipv4_ignore_obtained_default_gateway=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
        ipv4_ignore_obtained_dns_server=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
        ipv6_mode=dict(type='str',
                       choices=['no_ipv6_address', 'address_auto_configuration', 'link-local_only', 'stateful_dhcpv6',
                                'static'], required=False, default='no_ipv6_address'),
        ipv6_address=dict(type='str', required=False),
        ipv6_prefix_length=dict(type='str', required=False),
        ipv6_dns_server=dict(type='str', required=False),
        ipv6_gateway=dict(type='str', required=False),
        ipv6_default_route_metric=dict(type='str', required=False, default='100'),
        ipv6_ignore_obtained_default_gateway=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
        ipv6_ignore_obtained_dns_server=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
        enable_ip_passthrough=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
        ethernet_connection=dict(type='str', required=False),
        mac_address=dict(type='str', required=False),
        port_intercepts=dict(type='str', required=False),
        vlan_id=dict(type='str', required=False),
        ethernet_interface=dict(type='str', required=False),
        enable_lldp=dict(type='str', choices=['yes', 'no'], required=False),
        ethernet_link_mode=dict(type='str',
                                choices=['100m|full', '100m|half', '10m|full', '10m|half', '1g|full', 'auto'],
                                required=False, default='auto'),
        enable_data_usage_monitoring=dict(type='str', choices=['yes', 'no'], required=False, default='yes'),
        enable_second_sim_card=dict(type='str', choices=['yes', 'no'], required=False, default='no'),
        sim_1_apn_configuration=dict(type='str', choices=['automatic', 'manual'], required=False, default='automatic'),
        sim_1_mtu=dict(type='str', required=False, default='auto'),
        sim_1_personal_identification_number=dict(type='str', required=False),
        sim_1_user_name=dict(type='str', required=False),
        sim_1_password=dict(type='str', required=False, no_log=True),
        sim_1_access_point_name=dict(type='str', required=False),
        bridge_interfaces=dict(type='str', required=False),
        enable_spanning_tree_protocol=dict(type='str', choices=['yes', 'no'], required=False, default='yes'),
        forward_delay=dict(type='str', required=False, default='5'),
        hello_time=dict(type='str', required=False, default='2'),
        max_age=dict(type='str', required=False, default='20')
    )

    return module_args


def get_nodegrid_dict():
    nodegrid_keys = dict(
        connection_name=dict(
            ansible_name="connection_name",
            cli_name="name",
            cli_default="",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        connection_type=dict(
            ansible_name="connection_type",
            cli_name="type",
            cli_default="ethernet",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        set_as_primary_connection=dict(
            ansible_name="set_as_primary_connection",
            cli_name="set_as_primary_connection",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        block_unsolicited_incoming_packets=dict(
            ansible_name="block_unsolicited_incoming_packets",
            cli_name="block_unsolicited_incoming_packets",
            cli_default="",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        connect_automatically=dict(
            ansible_name="connect_automatically",
            cli_name="connect_automatically",
            cli_default="yes",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv4_mode=dict(
            ansible_name="ipv4_mode",
            cli_name="ipv4_mode",
            cli_default="dhcp",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv4_address=dict(
            ansible_name="ipv4_address",
            cli_name="ipv4_address",
            cli_default="",
            parent=True,
            parent_ansible_name="ipv4_mode",
            parent_value=['static'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv4_bitmask=dict(
            ansible_name="ipv4_bitmask",
            cli_name="ipv4_bitmask",
            cli_default="",
            parent=True,
            parent_ansible_name="ipv4_mode",
            parent_value=['static'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv4_dns_server=dict(
            ansible_name="ipv4_dns_server",
            cli_name="ipv4_dns_server",
            cli_default="",
            parent=True,
            parent_ansible_name="ipv4_mode",
            parent_value=['static'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv4_gateway=dict(
            ansible_name="ipv4_gateway",
            cli_name="ipv4_gateway",
            cli_default="",
            parent=True,
            parent_ansible_name="ipv4_mode",
            parent_value=['static'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv4_default_route_metric=dict(
            ansible_name="ipv4_default_route_metric",
            cli_name="ipv4_default_route_metric",
            cli_default="100",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv4_ignore_obtained_default_gateway=dict(
            ansible_name="ipv4_ignore_obtained_default_gateway",
            cli_name="ipv4_ignore_obtained_default_gateway",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv4_ignore_obtained_dns_server=dict(
            ansible_name="ipv4_ignore_obtained_dns_server",
            cli_name="ipv4_ignore_obtained_dns_server",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv6_mode=dict(
            ansible_name="ipv6_mode",
            cli_name="ipv6_mode",
            cli_default="no_ipv6_address",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv6_address=dict(
            ansible_name="ipv6_address",
            cli_name="ipv6_address",
            cli_default="",
            parent=True,
            parent_ansible_name="ipv6_mode",
            parent_value=['static'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv6_prefix_length=dict(
            ansible_name="ipv6_prefix_length",
            cli_name="ipv6_prefix_length",
            cli_default="",
            parent=True,
            parent_ansible_name="ipv6_mode",
            parent_value=['static'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv6_dns_server=dict(
            ansible_name="ipv6_dns_server",
            cli_name="ipv6_dns_server",
            cli_default="",
            parent=True,
            parent_ansible_name="ipv6_mode",
            parent_value=['static'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv6_gateway=dict(
            ansible_name="ipv6_gateway",
            cli_name="ipv6_gateway",
            cli_default="",
            parent=True,
            parent_ansible_name="ipv6_mode",
            parent_value=['static'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv6_default_route_metric=dict(
            ansible_name="ipv6_default_route_metric",
            cli_name="ipv6_default_route_metric",
            cli_default="100",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv6_ignore_obtained_default_gateway=dict(
            ansible_name="ipv6_ignore_obtained_default_gateway",
            cli_name="ipv6_ignore_obtained_default_gateway",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ipv6_ignore_obtained_dns_server=dict(
            ansible_name="ipv6_ignore_obtained_dns_server",
            cli_name="ipv6_ignore_obtained_dns_server",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        enable_ip_passthrough=dict(
            ansible_name="enable_ip_passthrough",
            cli_name="enable_ip_passthrough",
            cli_default="no",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Mobile Broadband GSM', 'mobile_broadband_gsm', 'Ethernet', 'ethernet'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ethernet_connection=dict(
            ansible_name="ethernet_connection",
            cli_name="ethernet_connection",
            cli_default="",
            parent=True,
            parent_ansible_name="enable_ip_passthrough",
            parent_value=['yes'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        mac_address=dict(
            ansible_name="mac_address",
            cli_name="mac_address",
            cli_default="",
            parent=True,
            parent_ansible_name="enable_ip_passthrough",
            parent_value=['yes'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        port_intercepts=dict(
            ansible_name="port_intercepts",
            cli_name="port_intercepts",
            cli_default="",
            parent=True,
            parent_ansible_name="enable_ip_passthrough",
            parent_value=['yes'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        vlan_id=dict(
            ansible_name="vlan_id",
            cli_name="vlan_id",
            cli_default="",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['VLAN', 'vlan'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ethernet_interface=dict(
            ansible_name="ethernet_interface",
            cli_name="ethernet_interface",
            cli_default="",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Ethernet', 'ethernet', 'VLAN', 'vlan'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        enable_lldp=dict(
            ansible_name="enable_lldp",
            cli_name="enable_lldp",
            cli_default="",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Ethernet', 'ethernet'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        ethernet_link_mode=dict(
            ansible_name="ethernet_link_mode",
            cli_name="ethernet_link_mode",
            cli_default="auto",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Ethernet', 'ethernet'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        enable_data_usage_monitoring=dict(
            ansible_name="enable_data_usage_monitoring",
            cli_name="enable_data_usage_monitoring",
            cli_default="yes",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Mobile Broadband GSM', 'mobile_broadband_gsm'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        enable_second_sim_card=dict(
            ansible_name="enable_second_sim_card",
            cli_name="enable_second_sim_card",
            cli_default="no",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Mobile Broadband GSM', 'mobile_broadband_gsm'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        sim_1_apn_configuration=dict(
            ansible_name="sim_1_apn_configuration",
            cli_name="sim-1_apn_configuration",
            cli_default="automatic",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Mobile Broadband GSM', 'mobile_broadband_gsm'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        sim_1_mtu=dict(
            ansible_name="sim_1_mtu",
            cli_name="sim-1_mtu",
            cli_default="auto",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Mobile Broadband GSM', 'mobile_broadband_gsm'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        sim_1_personal_identification_number=dict(
            ansible_name="sim_1_personal_identification_number",
            cli_name="sim-1_personal_identification_number",
            cli_default="",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Mobile Broadband GSM', 'mobile_broadband_gsm'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        sim_1_user_name=dict(
            ansible_name="sim_1_user_name",
            cli_name="sim-1_user_name",
            cli_default="",
            parent=True,
            parent_ansible_name="sim_1_apn_configuration",
            parent_value=['manual'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        sim_1_password=dict(
            ansible_name="sim_1_password",
            cli_name="sim-1_password",
            cli_default="",
            parent=True,
            parent_ansible_name="sim_1_apn_configuration",
            parent_value=['manual'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        sim_1_access_point_name=dict(
            ansible_name="sim_1_access_point_name",
            cli_name="sim-1_access_point_name",
            cli_default="",
            parent=True,
            parent_ansible_name="sim_1_apn_configuration",
            parent_value=['manual'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        bridge_interfaces=dict(
            ansible_name="bridge_interfaces",
            cli_name="bridge_interfaces",
            cli_default="",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Bridge', 'bridge'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        enable_spanning_tree_protocol=dict(
            ansible_name="enable_spanning_tree_protocol",
            cli_name="enable_spanning_tree_protocol",
            cli_default="yes",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Bridge', 'bridge'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        forward_delay=dict(
            ansible_name="forward_delay",
            cli_name="forward_delay",
            cli_default="5",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Bridge', 'bridge'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        hello_time=dict(
            ansible_name="hello_time",
            cli_name="hello_time",
            cli_default="2",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Bridge', 'bridge'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),
        max_age=dict(
            ansible_name="max_age",
            cli_name="max_age",
            cli_default="20",
            parent=True,
            parent_ansible_name="connection_type",
            parent_value=['Bridge', 'bridge'],
            import_template="/settings/network_connections/{name} {cli_name}={value}"
        ),

    )
    return nodegrid_keys
