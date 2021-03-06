#!/usr/bin/env python
'''
Simple script to demonstrate how to Convert to UCS Python while performing tasks
in the UCS Manager GUI

Requires the UCS SDK: pip install ucsmsdk

Michael Petrinovic 2018
'''
import os
from ucsmsdk.ucshandle import UcsHandle
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
    try:
        handle=UcsHandle(UCSM, USER, PASS)

        # Login to UCSM
        handle.login()

        # If successful, print some details
        print ("Login was successful")
        print ("=" * 50)
        print ("UCS Cookie: " + handle.cookie)
        print ("UCS IP: " + handle.ip)
        print ("UCS Name: " + handle.ucs)
        print ("UCS Version: " + str(handle.version))
        print ("=" * 50)

        print ("Compute Blade Output")
        mo_list = handle.query_classid("ComputeBlade")
        for blade in mo_list:
            print blade.serial, blade.rn, blade.oper_state, blade.oper_power, blade.server_id, blade.availability, blade.name
        print ("=" * 50)

        print ("Associated blades only")
        filter_exp='(oper_state,"ok")'
        mo_list=handle.query_classid("ComputeBlade",filter_str=filter_exp)
        for blade in mo_list:
            print blade.serial
        print ("=" * 50)

        print ("Specific Serial Prefix Search")
        filter_exp='(serial,"^QCI\d{4}", type="re")'
        mo_list=handle.query_classid("ComputeBlade",filter_str=filter_exp)
        for blade in mo_list:
            print blade.serial
        print ("=" * 50)

        print ("Rack Unit Output")
        mo_list = handle.query_classid("ComputeRackUnit")
        for blade in mo_list:
            print blade.serial, blade.rn, blade.oper_state, blade.oper_power, blade.server_id, blade.availability, blade.name
        print ("=" * 50)

    except:
        handle.logout()
        print ("Exception occurred")
        raise

    finally:
        handle.logout()

if __name__ == '__main__':
    main()
