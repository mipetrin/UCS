#!/usr/bin/env python
'''
Simple skeleton script to take the output of the convert_to_ucs_python function
and have it work with this basic code framework

Requires the UCS SDK: pip install ucsmsdk

Michael Petrinovic 2018
'''

# Import the "UcsHandle" class from the "ucshandle" module in the ucsmsdk directory
from ucsmsdk.ucshandle import UcsHandle

# Import my credentials for UCS Login from ucs_my_credentials.py in the same directory
from ucs_my_credentials import *


# init handle and login
handle = UcsHandle(UCSM,USER,PASS,secure=False)
handle.login()

# Insert Generated Script below this line

##### Start-Of-PythonScript #####

# Auto generated code from convert_to_ucs_python() in either the Java or XML version

##### End-Of-PythonScript #####


# Logout after script is executed
handle.logout()
