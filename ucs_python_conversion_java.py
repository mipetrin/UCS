#!/usr/bin/env python
'''
Simple script to demonstrate how to Convert to UCS Python while performing tasks
in the UCS Manager GUI

Requires the UCS SDK: pip install ucsmsdk


NOTE:
Mac OSX Users - if during the launch of the UCSM GUI, it fails - could be
related to not having the correct version of Java installed:
https://www.java.com/en/download/faq/yosemite_java.xml
https://support.apple.com/kb/DL1572?locale=en_US

Michael Petrinovic 2018
'''
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucsguilaunch import ucs_gui_launch
from ucsmsdk.utils.converttopython import convert_to_ucs_python

# Import my credentials for UCS Login from ucs_my_credentials.py in the same directory
from ucs_my_credentials import *

import time

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
    print ("=" * 50)

    # launch the GUI
    ucs_gui_launch(handle)

    # To prevent the conversion function from using an old/previous UCSM Logfile
    # Delay it's execution until the GUI has completed loading before asking the
    # User to hit "Enter" to continue script execution
    time.sleep(7)
    print("=========================================================")
    print("Hit \"Enter\" AFTER the Java GUI has completely loaded...")
    print("=========================================================")
    wait = raw_input()

    # Start the conversion to UCS Python
    convert_to_ucs_python()

except:
    handle.logout()
    print ("Exception occurred")
    raise

finally:
    print ("Executing finally block")
    handle.logout()

# END
