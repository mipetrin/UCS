#!/usr/bin/env python
'''
Simple script to demonstrate how to Convert to UCS Python while performing tasks
in the UCS Manager GUI

Requires the UCS SDK: pip install ucsmsdk

Michael Petrinovic 2018
'''
from ucsmsdk.ucshandle import UcsHandle

# Import my credentials for UCS Login from ucs_my_credentials.py in the same directory
from ucs_my_credentials import *


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
