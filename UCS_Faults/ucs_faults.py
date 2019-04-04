#! /usr/bin/env python
"""
Simple script to allow a user to obtain the list of active Fault Instances in the UCS Domain

Requires the UCS SDK: pip install ucsmsdk

Michael Petrinovic 2018
"""
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.comparesyncmo import compare_ucs_mo, write_mo_diff
from operator import itemgetter

# Import my credentials for UCS Login from ucs_my_credentials.py in the same directory
from ucs_my_credentials import *


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
'''


'''
handle.logout()
