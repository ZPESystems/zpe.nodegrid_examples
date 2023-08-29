# zpe.nodegrid_examples
This repository contains automation examples and libraries that can be used with Nodegrid OS. 
The repository aims to help customers start the automation journey with Nodegrid OS. We invite customers to provide feedback and suggestions on examples that can be added in the future.

It is recommended to use the latest Nodegrid OS version (5.8.2 or higher) with the examples.

The examples currently include multiple technologies with their own repositories:

## Ansible
- **Ansible Nodegrid Library:** The Ansible Nodegrid Library provides an Ansible library that helps to configure and manage Nodegrid appliances. The library enables customers to perform Zero Touch Provisioning, Firmware updates, Backup, Restores, and full Nodegrid configuration examples. The library and examples can be found [here](https://github.com/ZPESystems/Ansible)
- **Ansible Device Library:** The Device Library enables customers to interact with connected devices, typically through a console connection. The library and examples can be found [here](https://github.com/ZPESystems/zpe.device_connection)

## Salt
- **Salt Proxy Minion:** The Salt Proxy Minion Library can be used to configure Nodegrid appliances. It implements features that allow for ZTP deployments using this library. The library and examples can be found [here](https://github.com/ZPESystems/Salt)

## Cloudflare
- **Cloudflare Docker agent:** The repo explains how a Cloudflare agent can be deployed on a Nodegrid appliance. The implementation explores multiple use cases, including providing Zero Trust Access to individual end devices that can not directly support Cloudflares ZTNA agents. The repo and examples can be found [here](https://github.com/ZPESystems/cloudflare)

