#! /usr/bin/env python
"""
Simple script to allow a user to launch a KVM session for a blade / Service Profile

Requires the UCS SDK: pip install ucsmsdk

NOTE: Launching KVM session still requires that your host has Java installed and functioning correctly

Michael Petrinovic 2018
"""
import os
from ConfigParser import SafeConfigParser
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucskvmlaunch import ucs_kvm_launch
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
    handle = UcsHandle(UCSM, USER, PASS,secure=False)
    handle.login()

    # Obtain all the blade servers available in the UCS Domain
    blade_mo = handle.query_classid(class_id="computeBlade")

    server_data = []
    server_dict = {}
    count = 1

    for line in blade_mo:
        # assign to dictionary, count:line.dn
        server_dict[count] = line.dn

        # assign to a list that will be used by tabulate to format nicely
        server_data.append((count, line.dn, line.association, line.discovery, line.name, line.model, line.server_id, line.serial, line.operability, line.oper_power))
        count += 1

    # Display the data in table format
    print tabulate(server_data, headers=["KVM Launch ID", "Blade DN", "Association", "Discovery Status",
                        "Blade Name", "Blade Model", "Blade ID", "Blade S/N", "Operability", "Power Status"], tablefmt="grid")

    # Ask user to pick a server based off count ID, type(int)
    # Check that the ID selected is valid, ie, exists in server_dict, otherwise throw error to pick again
    while 1:
        selection = int(input("Select a KVM ID to Launch [1-" + str((count - 1)) + "]:   "))

        if selection < 1 or selection > (count - 1):
            print "Please select a KVM Launch ID between 1 and " + str((count - 1))
            print "Try again..."
        else:
            break

    # Once selection is made, do another lookup to query_dn based off line.dn
    # Used the returned object to launch the KVM
    selected_blade_mo = handle.query_dn(server_dict[selection])
    # Need to use query_dn instead of query_classid due to the returned object.
    # query_dn returns a class object
    # query_classid returns a list
    # The ucs_kvm_launch expects to be able to call blade_mo.dn directly via a class object

    print "=" * 80
    print selected_blade_mo
    print "=" * 80

    # Since launching via a service profile, use the blade object, obtain the assigned Service Profile
    # then perform another lookup to that specific DN to obtain a lsServer class object to launch
    selected_sp_mo = handle.query_dn(selected_blade_mo.assigned_to_dn)

    # sp_mo is of type LsServer
    ucs_kvm_launch(handle, service_profile=selected_sp_mo)

    # blade_mo is of type ComputeBlade. Can't seem to get this version to work
    # ucs_kvm_launch(handle, blade=selected_blade_mo, need_url=True)

    handle.logout()


if __name__ == '__main__':
    main()
