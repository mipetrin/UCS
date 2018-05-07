#! /usr/bin/env python
"""
Simple script to allow a user to launch a KVM session for a blade / Service Profile

Requires the UCS SDK: pip install ucsmsdk

NOTE: Launching KVM session still requires that your host has Java installed and functioning correctly

Michael Petrinovic 2018
"""
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucskvmlaunch import ucs_kvm_launch
from tabulate import tabulate
# Import my credentials for UCS Login from ucs_my_credentials.py in the same directory
from ucs_my_credentials import *

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
