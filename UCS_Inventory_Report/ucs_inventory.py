#! /usr/bin/env python
"""
Simple script to allow a user to generate a UCS Inventory Report

When it comes to printing the report, the user has 3 options:
    #1 = Use the default and return a wide variety of inventory elements
    #2 = Advanced Usage:
        # OPTION 2A - Custom, which will only return the inventory elements of the custom dictionary (spec=custom_inventory_spec)
        # OPTION 2B - Custom, combine the default inventory_spec dictionary with the custom_inventory_spec dictionary

Be sure to #comment out and uncomment out the option that you want to use


Requires the UCS SDK: pip install ucsmsdk

Michael Petrinovic 2018
"""
import datetime
import os
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.inventory import *
from ConfigParser import SafeConfigParser
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


# Name of Configuration File in the Local/Parent Directory
MY_CONFIG_FILE = "my_credentials.ini"


def get_parser():
    '''
    Get parser object for script
    '''
    #from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter,
                            add_help=True,
                            version="1.0")
    parser.add_argument("-p", "--platform", required=True, help="Specify which UCS Platform to use as defined in your Config File")
    parser.add_argument("-d", "--debug", action="store_true", dest="debug", default=False, help="Enable debug output")
    return parser


def main():
    """
    Main routine to be executed
    """
    # Get the CLI arguements
    args = get_parser().parse_args()
    section_platform = args.platform

    parser = SafeConfigParser()

    # Since when the script executes, it is difficult to assume the relative path - as depends on where you run your Python script from. 
    # Especially if calling it via absolute path and you're not in the actual directory
    # Hence, use the following to effectively obtain the config file as if it were '../my_credentials.ini'
    parent_configFilePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', MY_CONFIG_FILE)
    local_configFilePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.', MY_CONFIG_FILE)


    # Check if MY_CONFIG_FILE is in the current local directory, otherwise check the parent directory. If missing in both, then fail
    if os.path.exists(local_configFilePath):
        # Use the local directory
        # print ("Found in local directory")
        configFilePath = local_configFilePath
    elif os.path.exists(parent_configFilePath):
        # Use the parent directory
        # print ("Found in parent directory")
        configFilePath = parent_configFilePath
    else:
        # Missing completely. Fail
        print ("Unable to locate your Config File: {}. Please ensure that you have it created and available".format(MY_CONFIG_FILE))
        print ("Not found in the local directory: {}".format(local_configFilePath))
        print ("Not found in the Parent directory: {}".format(parent_configFilePath))
        exit(0)

    if args.debug:
        print ("Config File: {}".format(configFilePath))

    # Attempt to read the configuration file
    try:
        result = parser.read(configFilePath)
    except Exception as e :
        print(str(e))
        exit(0)

    if section_platform not in parser.sections():
        print ("Please ensure you select a Platform that you have defined in your {} file".format(MY_CONFIG_FILE))
        print ("Current Platforms defined: " + str(parser.sections()))
        exit(0)
    else:
        try:
            UCSM = parser.get(section_platform, 'UCSM')
            USER = parser.get(section_platform, 'USER')
            PASS = parser.get(section_platform, 'PASS')
        except Exception as e :
            print(str(e),' could not read configuration file')

            for section_name in parser.sections():
                print 'Section:', section_name
                print '  Options:', parser.options(section_name)
                if args.debug:
                    for name, value in parser.items(section_name):
                        print '  %s = %s' % (name, value)
                print
            # Exit due to exception
            exit(0)

    # Rest of normal flow would take place here
    handle = UcsHandle(UCSM, USER, PASS)
    handle.login()

    print ("Logged into UCS Domain: " + handle.ucs)
    # Obtain current date and time
    now = datetime.datetime.now()
    timestamp = now.strftime("%d_%b_%Y_%H_%M")

    output_file_format = "html" # args: json, html, csv

    output_dir = "./ucsBackup" # Take note of the trailing / at the end
    output_name = "Inventory_Report"
    output_filename = handle.ucs + "_" + output_name + "_" + timestamp + "." + output_file_format
    output_file = output_dir + output_filename
    # Generates the following as an example:
    # /Users/mipetrin/Scripts/Cisco_Live/UCSM_Python/ucsBackup/UCS-ACI-PODs_UCSM_Inventory_21_Feb_2018_00_12.html


    #######################################################################################################################
    # OPTION 1
    # Use the default and return a wide variety of inventory elements
    # Function get_inventory automatically returns json formatted inventory data. Hence need to assign to variable

    # UNCOMMENT BELOW IF YOU WANT THIS OPTION
    #my_ucs = get_inventory(handle, file_format=output_file_format, file_name=output_file)


    #######################################################################################################################
    # OPTION 2
    # Advanced Usage
    #
    # Define a dictionary, of just a small list of classes that you want, or a large one including all the default information
    # Can make use of http://<UCSM IP>/visore.html to identify which elements of the class you would like to include
    #
    # Breakdown:
    #
    # Fabric_VLANs = arbitary name to display in the output, ie. Heading
    # class_id: fabricVlan = must be a valid UCS Class ID
    # props = important keyword to denote which properties of the class you would like returned
    # prop: <dn> = the specific property/attribute that you want included in your report

    # UNCOMMENT BELOW IF YOU WANT THIS OPTION WITH OPTION 2A OR 2B

    custom_inventory_spec = {
        "Server_Profiles": {
            "class_id": "lsServer",
            "props": [
                {"prop": "dn"},
                {"prop": "name"},
                {"prop": "assoc_state"},
                {"prop": "usrlbl"},
                {"prop": "oper_state"},
                {"prop": "pndn"}
            ]
        },
        "Compute_Blades": {
            "class_id": "computeBlade",
            "props": [
                {"prop": "dn"},
                {"prop": "name"},
                {"prop": "model"},
                {"prop": "assigned_to_dn"},
                {"prop": "oper_power"},
                {"prop": "serial"},
                {"prop": "usrlbl"},
                {"prop": "total_memory"},
                {"prop": "oper_state"},
                {"prop": "available_memory"}
            ]
        },
        "MAC_Pool_Assignment": {
            "class_id": "macpoolPooled",
            "props": [
                {"prop": "dn"},
                {"prop": "id"},
                {"prop": "assigned"},
                {"prop": "assigned_to_dn"},
            ]
        },
        "IP_Pool_Assignment": {
            "class_id": "ippoolPooled",
            "props": [
                {"prop": "dn"},
                {"prop": "id"},
                {"prop": "assigned_to_dn"},
                {"prop": "def_gw"},
                {"prop": "subnet"},
                {"prop": "prim_dns"},
                {"prop": "sec_dns"}
            ]
        },
        "Fabric_VLANs": {
            "class_id": "fabricVlan",
            "props": [
                {"prop": "dn"},
                {"prop": "id"},
                {"prop": "name"},
                {"prop": "transport"},
                {"prop": "type"},
                {"prop": "switch_id"}
            ]
        },
        "Fabric_VSANs": {
            "class_id": "fabricVsan",
            "props": [
                {"prop": "dn"},
                {"prop": "id"},
                {"prop": "name"},
                {"prop": "fcoe_vlan"},
                {"prop": "transport"},
                {"prop": "type"},
                {"prop": "switch_id"}
            ]
        },
        "VSAN_TO_VHBA_MAPPING": {
            "class_id": "vnicFcIf",
            "props": [
                {"prop": "dn"},
                {"prop": "initiator"},
                {"prop": "name"},
                {"prop": "sharing"},
                {"prop": "switch_id"},
                {"prop": "type"},
                {"prop": "vnet"}
            ]
        },
        "Fabric_Interconnect_Eth_Ports": {
            "class_id": "etherPIo",
            "props": [
                {"prop": "dn"},
                {"prop": "id"},
                {"prop": "admin_state"},
                {"prop": "lic_state"},
                {"prop": "mac"},
                {"prop": "oper_speed"},
                {"prop": "oper_state"},
                {"prop": "slot_id"},
                {"prop": "port_id"},
                {"prop": "switch_id"},
                {"prop": "transport"},
                {"prop": "type"},
                {"prop": "unified_port"},
                {"prop": "xcvr_type"}
            ]
        }
    }


    #######################################################################################################################
    # OPTION 2A
    # ADVANCED: Custom, which will only return the inventory elements of the above dictionary - spec=custom_inventory_spec

    # UNCOMMENT BELOW IF YOU WANT THIS OPTION
    #my_ucs = get_inventory(handle, file_format=output_file_format, file_name=output_file, spec=custom_inventory_spec)


    #######################################################################################################################
    # OPTION 2B
    # ADVANCED: Custom, combine the default inventory_spec dictionary with the custom_inventory_spec
    # Sample of the default inventory_spec dictionary is at the end of this script (found in ucsmsdk.utils.inventory)

    # Make an empty dictionary. Using update, add items from each dictionary
    # First the default (inventory_spec) and then our custom inventory (custom_inventory_spec)
    # This way, if there are any common keys, (custom_inventory_spec) will override those in the default (inventory_spec)

    # UNCOMMENT BELOW 4 LINES IF YOU WANT THIS OPTION
    custom_spec = {}
    custom_spec.update(inventory_spec)
    custom_spec.update(custom_inventory_spec)
    my_ucs = get_inventory(handle, file_format=output_file_format, file_name=output_file, spec=custom_spec)

    #######################################################################################################################

    print ("Output file is: " + output_file)

    handle.logout()

if __name__ == '__main__':
    main()


'''
Current definition of the default inventory_spec (found in ucsmsdk.utils.inventory)
ucsmsdk==0.9.3.1
------------------------------------------------

inventory_spec = {
    "cpu": {
        "class_id": "ProcessorUnit",
        "props": [
            {"prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "arch"},
            {"prop": "cores"},
            {"prop": "cores_enabled"},
            {"prop": "oper_state"},
            {"prop": "socket_designation"},
            {"prop": "speed"},
            {"prop": "stepping"},
            {"prop": "threads"}
        ]
    },
    "fabric_interconnect": {
        "class_id": "NetworkElement",
        "props": [
            {"prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "oob_if_gw"},
            {"prop": "oob_if_ip"},
            {"prop": "oob_if_mask"},
            {"prop": "total_memory"}
        ]
    },
    "memory": {
        "class_id": "MemoryUnit",
        "ignore": [
            {"prop": "presence", "value": "missing"}
        ],
        "props": [
            {"prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "capacity"},
            {"prop": "clock"},
            {"prop": "presence"}]
    },
    "psu": {
        "class_id": "EquipmentPsu",
        "ignore": [
            {"prop": "presence", "value": "missing"}
        ],
        "props": [
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "type"},
            {"prop": "oper_state"}
        ]
    },
    "pci": {
        "class_id": "PciEquipSlot",
        "props": [
            {"label": "Server", "prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "mac_left"},
            {"prop": "mac_right"},
            {"prop": "smbios_id"},
            {"prop": "discovery_state"},
            {"prop": "controller_reported"}]
    },
    "vic": {
        "class_id": "AdaptorUnit",
        "props": [
            {"label": "Server", "prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "blade_id"},
            {"prop": "chassis_id"},
            {"prop": "oper_state"},
            {"prop": "operability"},
            {"prop": "presence"},
            {"prop": "part_number"},
            {"prop": "admin_power_state"},
            {"prop": "base_mac"},
            {"prop": "conn_path"},
            {"prop": "conn_status"},
            {"prop": "perf"},
            {"prop": "voltage"},
            {"prop": "thermal"},
            {"prop": "pci_addr"},
            {"prop": "pci_slot"}]
    },
    "storage": {
        "class_id": "StorageController",
        "props": [
            {"label": "Server", "prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "type"},
            {"prop": "oper_state"},
            {"prop": "operability"},
            {"prop": "oprom_boot_status"},
            {"prop": "raid_support"},
        ],
    },
    "disks": {
        "class_id": "StorageLocalDisk",
        "props": [
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "device_type"},
            {"prop": "connection_protocol"},
            {"prop": "disk_state"},
            {"prop": "block_size"},
            {"prop": "bootable"},
            {"prop": "link_speed"},
            {"prop": "number_of_blocks"},
            {"prop": "operability"},
            {"prop": "presence"},
            {"prop": "size"},
            {"prop": "power_state"}
        ]
    },
    "vNICs": {
        "class_id": "AdaptorHostEthIf",
        "props": [
            {"prop": "id"},
            {"prop": "dn"},
            {"prop": "name"},
            {"prop": "cdn_name"},
            {"prop": "mac"},
            {"prop": "mtu"},
            {"prop": "admin_state"},
            {"prop": "boot_dev"},
            {"prop": "chassis_id"},
            {"prop": "side"},
            {"prop": "slot_id"},
            {"prop": "switch_id"},
            {"prop": "presence"},
            {"prop": "discovery"},
            {"prop": "link_state"},
            {"prop": "oper_state"},
            {"prop": "operability"},
            {"prop": "ep_dn"},
            {"prop": "host_port"},
            {"prop": "if_type"},
            {"prop": "if_role"},
            {"prop": "order"},
            {"prop": "original_mac"}
        ]
    },
    "vHBAs": {
        "class_id": "AdaptorHostFcIf",
        "props": [
            {"prop": "id"},
            {"prop": "dn"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "wwn"},
            {"prop": "node_wwn"},
            {"prop": "admin_state"},
            {"prop": "order"},
            {"prop": "boot_dev"},
            {"prop": "cdn_name"},
            {"prop": "discovery"},
            {"prop": "chassis_id"},
            {"prop": "ep_dn"},
            {"prop": "host_port"},
            {"prop": "name"},
            {"prop": "if_role"},
            {"prop": "if_type"},
            {"prop": "link_state"},
            {"prop": "max_data_field_size"},
            {"prop": "presence"},
            {"prop": "oper_state"},
            {"prop": "operability"},
            {"prop": "original_node_wwn"},
            {"prop": "original_wwn"}
        ]
    }
}
'''
