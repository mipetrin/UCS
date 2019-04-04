#! /usr/bin/env python
"""
Simple script to allow a user to compare UCS Domain - Fabric VLANs

1. Login to 2 systems
2. Print the names of each system and their reference (left/right)
3. Pull the list of fabricVlan on each system
4. List out how many on left_ucs, right_ucs
5. Compare them and see if there are differences
6. Print list of common vlans across both systems based on VLAN ID = but print the name if different
7. Print list of VLANs only on the left UCS
8. Print list of VLANs only on the right UCS

Requires the UCS SDK: pip install ucsmsdk

Michael Petrinovic 2018
"""
import time
import os
from ConfigParser import SafeConfigParser
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.comparesyncmo import compare_ucs_mo, write_mo_diff
from tabulate import tabulate


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
    parser.add_argument("-p", "--platform", nargs=2, required=True, help="Specify which UCS Platform to use as defined in your Config File")
    parser.add_argument("-d", "--debug", action="store_true", dest="debug", default=False, help="Enable debug output")
    return parser


def query_dn_for_vlan_id(my_handle, my_dn):
    '''
    '''
    x = my_handle.query_dn(my_dn)
    return x.id


def main():
    """
    Main routine to be executed
    """
    # Get the CLI arguements
    args = get_parser().parse_args()
    section_platform_left = args.platform[0]
    section_platform_right = args.platform[1]

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

    if (section_platform_left not in parser.sections()) or (section_platform_right not in parser.sections()):
        print ("Please ensure you select a Platform that you have defined in your {} file".format(MY_CONFIG_FILE))
        print ("Current Platforms defined: " + str(parser.sections()))
        exit(0)
    else:
        try:
            UCSM_LEFT = parser.get(section_platform_left, 'UCSM')
            USER_LEFT = parser.get(section_platform_left, 'USER')
            PASS_LEFT = parser.get(section_platform_left, 'PASS')

            UCSM_RIGHT = parser.get(section_platform_right, 'UCSM')
            USER_RIGHT = parser.get(section_platform_right, 'USER')
            PASS_RIGHT = parser.get(section_platform_right, 'PASS')
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
    start_time = time.time()

    left_ucs = UcsHandle(UCSM_LEFT, USER_LEFT, PASS_LEFT,secure=False)
    right_ucs = UcsHandle(UCSM_RIGHT, USER_RIGHT, PASS_RIGHT,secure=False)
    left_ucs.login()
    right_ucs.login()

    #print (" Left UCS Name: " + left_ucs.ucs)
    #print ("Right UCS Name: " + right_ucs.ucs)
    #print "=" * 80

    left_ucs_vlans = left_ucs.query_classid("fabricVlan")
    right_ucs_vlans = right_ucs.query_classid("fabricVlan")

    # Combined Dictionary to keep track of DN/VLAN mapping per UCS Domain (Left/Right)
    dn_to_vlan_mapping = {}
    dn_to_vlan_mapping["left"] = {}
    dn_to_vlan_mapping["right"] = {}

    # Loop through the data we previously collected with the query_classid lookups.
    # Doing this for speed instead of having to make subsequent query lookups per VLAN/DN
    # Reduced from 99 seconds down to 7 seconds
    for element in left_ucs_vlans:
        dn_to_vlan_mapping["left"][element.dn] = element.id
    for element in right_ucs_vlans:
        dn_to_vlan_mapping["right"][element.dn] = element.id

    # Using the built in compare function, identify what MO's have differences. Returns an object
    difference_vlans = compare_ucs_mo(left_ucs_vlans, right_ucs_vlans, include_equal=True)

    # Built in function to print the differences, with some information, however no real logic applied
    #write_mo_diff(difference_vlans)

    difference_in_vlan = []
    left_only_vlans = [] # VLANs found to only exist in one UCS Domain, i.e Left
    right_only_vlans = [] # VLANs found to only exist in one UCS Domain, i.e. Right
    common_vlans = [] # VLANs found to exist in BOTH UCS Domains and are the SAME, i.e. VLAN NAME and VLAN ID

    for item in difference_vlans:
        if item.diff_property == None:
            if item.side_indicator == "<=":
                # lov is left only vlan
                lov = dn_to_vlan_mapping["left"][item.dn]
                left_only_vlans.append((item.dn, lov))
            elif item.side_indicator == "=>":
                # rov is right only vlan
                rov = dn_to_vlan_mapping["right"][item.dn]
                right_only_vlans.append((item.dn, rov))
            else:
                # Extremely slow. Need to figure out how to speed up
                # Since the same, doesn't matter which UCS Domain we query
                # cv is common vlan
                cv = dn_to_vlan_mapping["left"][item.dn]
                common_vlans.append((item.dn, cv))
        else:
            '''
            # item.diff_property != None therefore has some different property values
            print "DN: " + item.dn
            print "Class ID: " + str(item.input_object.get_class_id())
            print "Side indicator: " + item.side_indicator
            print "Diff Property: " + str(item.diff_property)
            for key, value in item.diff_prop_values.iteritems():
                print "Key: " + key
                print "Value: " + value
            '''
            left_ucs_query = query_dn_for_vlan_id(left_ucs, item.dn)
            right_ucs_query = query_dn_for_vlan_id(right_ucs, item.dn)

            difference_in_vlan.append((item.input_object.get_class_id(), item.dn, left_ucs.ucs,
                        left_ucs_query, right_ucs_query, right_ucs.ucs))

    # Display the various data in table format
    print ("")
    print ("=" * 80)
    print ("")
    print ("VLAN/s unique to the Left UCS Domain: " + left_ucs.ucs)
    print ("")
    print (tabulate(left_only_vlans, headers=["DN", "VLAN ID"], tablefmt="simple"))
    print ("")
    print ("=" * 80)
    print ("")
    print ("VLAN/s unique to the Right UCS Domain: " + right_ucs.ucs)
    print ("")
    print (tabulate(right_only_vlans, headers=["DN", "VLAN ID"], tablefmt="simple"))
    print ("")
    print ("=" * 80)
    print ("")
    print ("Common VLANs, configured the same in both UCS Domains: " + left_ucs.ucs + "  //  " + right_ucs.ucs)
    print ("")
    print (tabulate(common_vlans, headers=["DN", "VLAN ID"], tablefmt="simple"))
    print ("")
    print ("=" * 80)
    print ("")
    print ("VLAN/s by the same name exist on both UCS Domains however there is a difference in the VLAN ID")
    print ("")
    print (tabulate(difference_in_vlan, headers=["ClassID", "Affected DN", "Left UCS", "VLAN ID", "VLAN ID", "Right UCS"], tablefmt="simple"))
    print ("")
    print ("=" * 80)
    print ("=" * 80)
    print ("Summary:")
    print ("Left UCS: %s has %s unique VLANs" % (left_ucs.ucs, len(left_only_vlans)))
    print ("Right UCS: %s has %s unique VLANs" % (right_ucs.ucs, len(right_only_vlans)))
    print ("There are %s common VLANs" % (len(common_vlans)))
    print ("There is potential issues with %s VLANs due to differences" % (len(difference_in_vlan)))
    print ("=" * 80)
    print("--- Execution Time: %s seconds ---" % (time.time() - start_time))

    left_ucs.logout()
    right_ucs.logout()

if __name__ == '__main__':
    main()
