#! /usr/bin/env python
"""
Simple script to allow a user to obtain the list of active Fault Instances in the UCS Domain

Requires the UCS SDK: pip install ucsmsdk

Michael Petrinovic 2018
"""
import os
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.comparesyncmo import compare_ucs_mo, write_mo_diff
from operator import itemgetter
from ConfigParser import SafeConfigParser
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


# Name of Configuration File in the Local/Parent Directory
MY_CONFIG_FILE = "my_credentials.ini"


def query_fault(handle, sev):
    '''
    Custom function to return the set of faultInst objects that match the severity, using a classID query with filter
    '''
    filter_str = '(severity, "' + sev + '")'
    fi = handle.query_classid(class_id="faultInst", filter_str=filter_str)
    return fi


def print_fault(severity, mo_list):
    '''
    Custom function to print the list of faults, using the format of my choosing
    '''
    print "=" * 80
    print ("[" + severity + "] Faults Summary. Total = " + str(len(mo_list)))
    print "=" * 80

    # Check if the list is empty or not
    if len(mo_list) >= 1:
        for mo in mo_list:
            print ("# [" + mo.code + "] : [Description = " + mo.descr + "] [Occurence: " + mo.occur + "] [Last Transition: " + mo.last_transition + "]")
    else:
        print ("N/A")


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

    # Available severity codes for UCS Fault Instances
    fault_severity = ["critical", "major", "minor", "warning", "info", "condition", "cleared", "soaking", "suppressed"]

    fault_lookup = {} # Dictionary to be used to store the returned MO's, with the key being the severity
    fault_severity_count = {} # Dictionary to track total faults per severity

    # Loop through all fault severity types, perform a fault lookup in the system and return the list of MO's.
    # Assign to the fault_lookup dictionary, with severity as the key
    for fault_type in fault_severity:
        fault_lookup[fault_type] = query_fault(handle, fault_type)
        # Find out the length of the inner list, based off the fault severity in the lookup
        # eg: fault_lookup["critical"] = [x,y,z]
        fault_severity_count[fault_type] = len(fault_lookup[fault_type])

    # Loop through each severity, sort by faultCode and then print it out
    for item in fault_severity:
        print_fault(item, fault_lookup[item])

    print "=" * 80
    print ("Summary of total faults")
    print "-" * 80

    for fault_summary in fault_severity:
        print (fault_summary + " = " + str(fault_severity_count[fault_summary]))

    print "=" * 80
    # {'info': 48, 'major': 123, 'soaking': 0, 'critical': 6,
    # 'suppressed': 0, 'minor': 0, 'cleared': 0, 'warning': 120, 'condition': 0}

    handle.logout()

if __name__ == '__main__':
    main()
