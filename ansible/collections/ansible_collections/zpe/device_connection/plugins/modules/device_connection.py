#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Rene Neumann <rene.neumann@zpesystems.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: connection
author: Rene Neumann (@zpe-rneumann)
short_description: This module handles connection details on Nodegrid OS
version_added: "1.0.0"
description: The module is used to create, delete and update network connections on Nodegrid OS 5.6 or newer
options:
    state:
        description: State of the connection
        required: False
        choices: ['up','down', 'exist', 'absent']
        default: 'exist'
        type: str
    connection_name:
        description: Name of the connection
        required: True
        choices: []
        default: 
        type: str
    connection_type:
        description: Type of connection to be used
        required: False
        choices: ['analog_modem', 'bridge', 'loopback', 'pppoe', 'wifi', 'bonding', 'ethernet', 'mobile_broadband_gsm', 'vlan']
        default: 'ethernet'
        type: str
    set_as_primary_connection:
        description: Should this connection be the primary connection, only one connection can be primary
        required: False
        choices: ['yes', 'no']
        default: 'no'
        type: str
    block_unsolicited_incoming_packets:
        description: Enable firewall rules to block incomming packets
        required: False
        choices: ['yes', 'no']
        default: 
        type: str
    connect_automatically:
        description: Enable the connection automatically
        required: False
        choices: ['yes', 'no']
        default: 'yes'
        type: str
    ipv4_mode:
        description: Define the IPv4 mode
        required: False
        choices: ['no_ipv4_address', 'dhcp', 'static']
        default: 'dhcp'
        type: str
    ipv4_address:
        description: Define the IPv4 Address
        required: False
        choices: []
        default: 
        type: str
    ipv4_bitmask:
        description: Define IPv4 Bitmask  i.e. 16 or 24
        required: False
        choices: []
        default: 
        type: str
    ipv4_dns_server:
        description: Define manually a IPv4 dns server address
        required: False
        choices: []
        default: 
        type: str
    ipv4_gateway:
        description: Define a IPv4 gateway address
        required: False
        choices: []
        default: 
        type: str
    ipv4_default_route_metric:
        description: Define a IPv4 default route metric for the connection
        required: False
        choices: []
        default: '100'
        type: str
    ipv4_ignore_obtained_default_gateway:
        description: Define if the default gateway settings which were received through DHCP should be ignored
        required: False
        choices: ['yes', 'no']
        default: 'no'
        type: str
    ipv4_ignore_obtained_dns_server:
        description: Define if the dns server  settings which were received through DHCP should be ignored
        required: False
        choices: ['yes', 'no']
        default: 'no'
        type: str
    ipv6_mode:
        description: Define the IPv6 mode
        required: False
        choices: ['no_ipv6_address', 'address_auto_configuration', 'link-local_only', 'stateful_dhcpv6', 'static']
        default: 'no_ipv6_address'
        type: str
    ipv6_address:
        description: Define the IPv6 Address
        required: False
        choices: []
        default: 
        type: str
    ipv6_prefix_length:
        description: Define IPv6 prefix  i.e. 64 or 128
        required: False
        choices: []
        default: 
        type: str
    ipv6_dns_server:
        description: Define manually a IPv6 dns server address
        required: False
        choices: []
        default: 
        type: str
    ipv6_gateway:
        description: Define a IPv6 gateway address
        required: False
        choices: []
        default: 
        type: str
    ipv6_default_route_metric:
        description: Define a IPv6 default route metric for the connection
        required: False
        choices: []
        default: '100'
        type: str
    ipv6_ignore_obtained_default_gateway:
        description: Define if the default gateway settings which were received through DHCP should be ignored
        required: False
        choices: ['yes', 'no']
        default: 'no'
        type: str
    ipv6_ignore_obtained_dns_server:
        description: Define if the dns server  settings which were received through DHCP should be ignored
        required: False
        choices: ['yes', 'no']
        default: 'no'
        type: str
    enable_ip_passthrough:
        description: Define if IP_Passthrough should be enabled or not
        required: False
        choices: ['yes', 'no']
        default: 'no'
        type: str
    ethernet_connection:
        description: Define the connection name which should be used for IP passthrough
        required: False
        choices: []
        default: 
        type: str
    mac_address:
        description: Define a specific client mac address, client defined will be receiving the forwarded traffic
        required: False
        choices: []
        default: 
        type: str
    port_intercepts:
        description: Define port intercepts which will not be forwarded to the client
        required: False
        choices: []
        default: 
        type: str
    vlan_id:
        description: Define a vlan id for a VLAN connection
        required: False
        choices: []
        default: 
        type: str
    ethernet_interface:
        description: Name of the physical ethernet interface to be used
        required: False
        choices: []
        default: 
        type: str
    enable_lldp:
        description: Enable LLDP on the connection
        required: False
        choices: ['yes', 'no']
        default: 
        type: str
    ethernet_link_mode:
        description: Allow the definition of link mode
        required: False
        choices: ['100m|full', '100m|half', '10m|full', '10m|half', '1g|full', 'auto']
        default: 'auto'
        type: str
    enable_data_usage_monitoring:
        description: Define if data use monitoring is enabled or not
        required: False
        choices: ['yes', 'no']
        default: 'yes'
        type: str
    enable_second_sim_card:
        description: Define if a 2nd SIM card is present for a CELLULAR connection
        required: False
        choices: ['yes', 'no']
        default: 'no'
        type: str
    sim_1_apn_configuration:
        description: SIM 1 APN configuration
        required: False
        choices: ['automatic', 'manual']
        default: 'automatic'
        type: str
    sim_1_mtu:
        description: Defines SIM1 MTU value
        required: False
        choices: []
        default: 'auto'
        type: str
    sim_1_personal_identification_number:
        description: Defines SIM 1 PIN if required for the card
        required: False
        choices: []
        default: 
        type: str
    sim_1_user_name:
        description: Allows definition of SIM1 APN user name for manual configuration
        required: False
        choices: []
        default: 
        type: str
    sim_1_password:
        description: Allows definition of SIM1 APN password for manual configuration
        required: False
        choices: []
        default: 
        type: str
    sim_1_access_point_name:
        description: Allows definition of SIM1 APN for manual configuration
        required: False
        choices: []
        default: 
        type: str
    bridge_interfaces:
        description: Defines the physical interfaces which are used for the bridge interface
        required: False
        choices: []
        default: 
        type: str
    enable_spanning_tree_protocol:
        description: Defines if Spanning Tree should enabled on the bridge interface
        required: False
        choices: ['yes', 'no']
        default: 'yes'
        type: str
    forward_delay:
        description: Defines STP forwarding delay setting on the bridge interface
        required: False
        choices: []
        default: '5'
        type: str
    hello_time:
        description: Defines STP hello time setting on the bridge interface
        required: False
        choices: []
        default: '2'
        type: str
    max_age:
        description: Defines STP max time setting on the bridge interface
        required: False
        choices: []
        default: '20'
        type: str


'''

EXAMPLES = r'''
- name: Delete Connection
  zpe.network.connection:
    connection_name: "CONNECTION_TEST_CELL"
    state: 'absent'

- name: Create Cellular Connection
  zpe.network.connection:
    connection_name: "CONNECTION_TEST_CELL"
    connection_type: 'mobile_broadband_gsm'
    ethernet_interface: 'cdc-wdm1'
    connect_automatically: 'yes'
    ipv4_mode: 'dhcp'
    ipv6_mode: 'no_ipv6_address'
    enable_data_usage_monitoring: 'yes'
    sim_1_apn_configuration: 'automatic'
    sim_1_mtu: 'auto'
    enable_second_sim_card: 'no'

- name: Create Ethernet Connection with DHCP
  zpe.network.connection:
    connection_name: "ETH0"
    connection_type: 'ethernet'
    ethernet_interface: 'eth0'
    connect_automatically: 'yes'
    ipv4_mode: 'dhcp'
    ipv6_mode: 'no_ipv6_address'

- name: Update Ethernet Connection
  zpe.network.connection:
    connection_name: "ETH0"
    connection_type: 'ethernet'
    ethernet_interface: 'eth0'
    connect_automatically: 'yes'
    ipv4_mode: 'static'
    ipv4_address: '192.168.29.20'
    ipv4_bitmask: '24'
    ipv4_dns_server: '8.8.8.8'
    ipv4_gateway: '192.168.29.1'
    ipv4_default_route_metric: '100'
    ipv4_ignore_obtained_default_gateway: 'yes'
    ipv4_ignore_obtained_dns_server: 'yes'
    ethernet_link_mode: '1g|full'

- name: Create VLAN Connection
  zpe.network.connection:
    connection_name: "CONNECTION_TEST_VLAN"
    connection_type: 'vlan'
    ethernet_interface: 'eth0'
    connect_automatically: 'yes'
    ipv4_mode: 'dhcp'
    vlan_id: '105'

- name: Create Bridge Connection
  zpe.network.connection:
    connection_name: "CONNECTION_TEST_BRIDGE"
    connection_type: 'bridge'
    bridge_interfaces: 'backplane0'
    connect_automatically: 'yes'
    ipv4_mode: 'dhcp'
    enable_spanning_tree_protocol: 'no'
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zpe.device_connection.plugins.module_utils.connection_util import get_module_params
from ansible_collections.zpe.device_connection.plugins.module_utils.connection_util import get_connection_args
from ansible_collections.zpe.device_connection.plugins.module_utils.connection import NodegridDeviceConnection
from ansible.utils.display import Display
import os

# We have to remove the SID from the Environmental settings, to avoid an issue
# were we can not run pexpect.run multiple times
if "DLITF_SID" in os.environ:
    del os.environ["DLITF_SID"]
if "DLITF_SID_ENCRYPT" in os.environ:
    del os.environ["DLITF_SID_ENCRYPT"]
# import logging
display = Display()


def run_module():
    try:
        # define available arguments/parameters a user can pass to the module
        module_args = get_module_params()

        # seed the result dict in the object
        # we primarily care about changed and state
        # changed is if this module effectively modified the target
        # state will include any data that you want your module to pass back
        # for consumption, for example, in a subsequent task
        result = dict(
            changed=False,
            message=''
        )

        # the AnsibleModule object will be our abstraction working with Ansible
        # this includes instantiation, a couple of common attr would be the
        # args/params passed to the execution, as well as if the module
        # supports check mode
        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )
    except Exception as e:
        result['failed'] = True
        result['message'] = "Error: setting up module"
        result['error_details'] = str(e)
        module.exit_json(**result)
    #
    # Nodegrid OS section starts here
    #
    # Lets get the connection details
    try:
        connection_args = get_connection_args(target_type=module.params['target_os'], module=module.params)
        if not connection_args['target_found']:
            result['failed'] = True
            result['target_check'] = connection_args['target_check']
            result['message'] = connection_args['message']
            result['error'] = connection_args['error']
            module.exit_json(**result)
    except Exception as e:
        result['failed'] = True
        result['message'] = "Error: get device information for device type"
        result['error_conn_details'] = str(e)
        module.exit_json(**result)

    try:
        ngconnection = NodegridDeviceConnection(connection_args)
        device_connection, device_connections_status, debug_output = ngconnection.local_get_connection()
    except Exception as e:
        result['failed'] = True
        result['message'] = "Error: opening device connection "
        result['error_details'] = str(e)
        module.exit_json(**result)

    if device_connections_status == 0:
        # First lets setup the connection Init
        cmds_init_debug = list()
        cmds_output = list()
        cmds_close_debug = list()
        if len(connection_args['cmds_init']) > 0 and connection_args['send_cmds_init']:
            for cmd in connection_args['cmds_init']:
                send_cmds_status, debug_action_list = ngconnection.local_send_cmd(device_connection, cmd)
                cmds_init_debug.append(debug_action_list)
        else:
            send_cmds_status = 0
        # if we found a prompt and the connection init was successful
        # on the device then we can start sending commands
        if send_cmds_status in [0]:
            # Then lets send the cmds
            for cmd in connection_args['cmds']:
                send_cmds_status, output = ngconnection.local_send_cmd(device_connection, cmd)
                cmds_output.append(output)
            # Now lets exit from the connection
            if len(connection_args['cmds_close']) > 0 and connection_args['send_cmds_close']:
                for cmd in connection_args['cmds_close']:
                    send_cmds_status, output = ngconnection.local_send_cmd(device_connection, cmd)
                    cmds_close_debug.append(output)
        else:
            result['failed'] = True
            result['message'] = "Error: init of target device, error code : {}".format(send_cmds_status)
            module.exit_json(**result)
        result['cmds_output'] = cmds_output
    else:
        result['failed'] = True
        result['message'] = "Error: Connection to target device failed, error code : {}".format(device_connections_status)
        result['connection_status'] = device_connections_status
        module.exit_json(**result)
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    error = False
    result['changed'] = True
    result['message'] = ''
    if error:
        module.fail_json(msg='Some Error'.format(''), **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
