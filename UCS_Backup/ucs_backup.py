#! /usr/bin/env python
"""
Simple script to allow a user to backup UCS configuration

Requires the UCS SDK: pip install ucsmsdk

Michael Petrinovic 2018
"""
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucsbackup import backup_ucs
import datetime
# Import my credentials for UCS Login from ucs_my_credentials.py in the same directory
from ucs_my_credentials import *

handle = UcsHandle(UCSM2,USER2,PASS2,secure=False)
handle.login()

# Obtain current date and time
now = datetime.datetime.now()
timestamp = now.strftime("%d_%b_%Y_%H_%M")

# Path to location where you want the UCS Backup to be saved
backup_dir = "/Users/mipetrin/Scripts/Cisco_Live_Melbourne_2018/UCSM_Python/ucsBackup"
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
