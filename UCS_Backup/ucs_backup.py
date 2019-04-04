#! /usr/bin/env python
"""
Simple script to allow a user to backup UCS configuration

Requires the UCS SDK: pip install ucsmsdk

Michael Petrinovic 2018
"""
import os
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucsbackup import backup_ucs
import datetime
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
    handle = UcsHandle(UCSM,USER,PASS,secure=False)
    handle.login()

    # Obtain current date and time
    now = datetime.datetime.now()
    timestamp = now.strftime("%d_%b_%Y_%H_%M")

    # Path to location where you want the UCS Backup to be saved
    backup_dir = "./ucsBackup"
    # NOTE: There is a 128 char limit for the full path of backup_dir + backup_filename.
    # If exceeded, ucsmsdk will throw a vague validation exception error


    '''
    'full-state' system backup creates a snapshot of the entire system and places it in a binary file. In the event of a disaster, the file generated from this backup can be used to perform a full restoration of the system using
    the same or a different fabric interconnect. You can restore from this file, but you cannot import the file using the Cisco UCS Manager GUI.

    'config-all' backup creates an XML file that includes all the system and logical configuration settings. You can use these to import the configuration settings to the original or different Cisco UCS domain. This backup
    cannot be used for a full-state system restoration operation, and it does not include passwords for locally authenticated users.

    'config-logical' backup creates an XML file that includes all logical configuration settings such as Cisco UCS service profiles, VLANs, VSANs, pools, and policies.

    'config-system' backup creates an XML file that includes all system configuration settings such as user names, roles, and locales.
    '''
    # BACKUP Types. Simply uncomment the type that you are interested in

    #backup_type = "full-state"   # Is currently timing out. Need to fix
    backup_type = "config-all"
    #backup_type = "config-logical"
    #backup_type = "config-system"

    # Ensure the right backup extension is automatically used
    if backup_type == "full-state":
        backup_extension = ".tar.gz"
    else:
        backup_extension = ".xml"

    # Auto generated filename, including UCSM Name, Backup, Timestamp and the correct extension
    backup_filename = handle.ucs + "_" + backup_type + "_" + timestamp + backup_extension

    # Perform the actual backup
    backup_ucs(handle, backup_type, backup_dir, backup_filename, timeout_in_sec=600, preserve_pooled_values=True)

    handle.logout()

if __name__ == '__main__':
    main()
