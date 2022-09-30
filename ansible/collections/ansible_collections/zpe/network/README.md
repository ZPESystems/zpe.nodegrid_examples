# Install the collection
## Manually on a Nodegrid:
- Open a shell 
- Create the folder 'collections' with
`mkdir /var/local/file_manager/admin_group/collections`
- Copy the collection to into the folder

In fututure versions will we suport direct installtion via ansible-galaxy commands 

`ansible-galaxy collection install git@github.com:ZPESystems/zpe_os_network_priv.git#collections/ansible_collections/zpe/network,main`

#Usage
The collection is designed to apply a full configuration and currently dose not support induvidial configuration changes.
Configurations Options which are not defined, will be reset to default values.

The collection supports ansible check_mode, and diff mode. 
In check_mode no changes are performed, but the playbook will indicate if a change would be required
In diff mode, the playbook with display the performed changes. Both modes can be combined.

## Examples
- Create a playbook and define a task to configure a network interface
### Create or Update a Ethernet connection
```
    - name: Configure Ethernet Connection - BACKPLANE0
      zpe.network.connection:
          connection_name: "BACKPLANE0"
          connect_automatically: 'no'
          set_as_primary_connection: 'no'
          enable_lldp: 'yes'
          block_unsolicited_incoming_packets: 'no'
          ethernet_link_mode: 'auto'
          enable_ip_passthrough: 'no'
          ipv4_mode: 'no_ipv4_address'
          ipv4_default_route_metric: '100'
          ipv4_ignore_obtained_default_gateway: 'no'
          ipv4_ignore_obtained_dns_server: 'no'
          ipv6_mode: 'no_ipv6_address'
          ipv6_default_route_metric: '100'
          ipv6_ignore_obtained_default_gateway: 'no'
          ipv6_ignore_obtained_dns_server: 'no'
```

### Create or Update a Celluar connection
```
- name: Create Connection
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
```

For more samples review test cases in teh collection Roles or review the documentation.

## Read documentation
```
ansible-doc -t module zpe.network.connection
```






