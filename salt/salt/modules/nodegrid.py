#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Diego Russi <diego.russi@zpesystems.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import

# Import python libs
import logging


# Set up logging
FORMAT = "[%(asctime)s %(filename)s->%(funcName)s:%(lineno)s]: %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__file__)


# This must be present or the Salt loader won't load this module.
__proxyenabled__ = ["nodegrid"]
# Define the module's virtual name
__virtualname__ = "nodegrid"

try:
    import pexpect # pylint: disable=unused-import

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def __virtual__():
    """
    Only load if the pexpect execution module is available.
    """
    if HAS_LIB:
        return __virtualname__

    return False, "The Nodegrid module cannot execute due missing requirements: python-pexpect"


def ping(**kwargs):
    log.debug("MODULE zpe_nodegrid ping status called...")
    return __proxy__["nodegrid.ping"](**kwargs) # pylint: disable=undefined-variable


def ping_icmp(**kwargs):
    log.debug("MODULE zpe_nodegrid ping_icmp called...")
    return __proxy__["nodegrid.ping_icmp"](**kwargs) # pylint: disable=undefined-variable


def check_version(desired_version):
    log.debug("MODULE zpe_nodegrid check_version called...")
    return __proxy__["nodegrid.check_version"](desired_version) # pylint: disable=undefined-variable


def cli(command, **kwargs):
    log.debug("MODULE zpe_nodegrid cli called...")
    return __proxy__["nodegrid.cli"](command, **kwargs) # pylint: disable=undefined-variable


def cli_file(file, **kwargs):
    log.debug("MODULE zpe_nodegrid cli_file called...")
    return __proxy__["nodegrid.cli_file"](file, **kwargs) # pylint: disable=undefined-variable


def cli_shell(command):
    log.debug("MODULE zpe_nodegrid cli_shell called...")
    return __proxy__["nodegrid.cli_shell"](command) # pylint: disable=undefined-variable


def cli_root_shell(command):
    log.debug("MODULE zpe_nodegrid cli_root_shell called...")
    return __proxy__["nodegrid.cli_root_shell"](command) # pylint: disable=undefined-variable


def import_settings(command, **kwargs):
    log.debug("MODULE zpe_nodegrid import_settings called...")
    return __proxy__["nodegrid.import_settings"](command, **kwargs) # pylint: disable=undefined-variable


def import_settings_file(file, **kwargs):
    log.debug("MODULE zpe_nodegrid import_settings_file called...")
    return __proxy__["nodegrid.import_settings_file"](file, **kwargs) # pylint: disable=undefined-variable


def export_settings(path, **kwargs):
    log.debug("MODULE zpe_nodegrid export_settings called...")
    return __proxy__["nodegrid.export_settings"](path, **kwargs) # pylint: disable=undefined-variable


def get_system_about():
    return __proxy__["nodegrid.get_system_about"]() # pylint: disable=undefined-variable


def add_license(lic_key):
    return __proxy__["nodegrid.add_license"](lic_key) # pylint: disable=undefined-variable


def save_settings(**kwargs):
    return __proxy__["nodegrid.save_settings"](**kwargs) # pylint: disable=undefined-variable


def apply_settings(**kwargs):
    return __proxy__["nodegrid.apply_settings"](**kwargs) # pylint: disable=undefined-variable


def cp_file(file, destination, **kwargs):
    return __proxy__["nodegrid.cp_file"](file, destination, **kwargs) # pylint: disable=undefined-variable


def change_default_password(**kwargs):
    return __proxy__["nodegrid.change_default_password"](**kwargs) # pylint: disable=undefined-variable


def software_upgrade(**kwargs):
    return __proxy__["nodegrid.software_upgrade"](**kwargs) # pylint: disable=undefined-variable
