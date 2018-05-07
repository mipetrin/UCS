#!/usr/bin/env python
'''
Simple script to demonstrate how to Convert to UCS Python while performing tasks
in the UCS Manager GUI

Requires the UCS SDK: pip install ucsmsdk

NOTE: UCSM HTML5 Users - Since there is no Java, take note of the following
https://communities.cisco.com/thread/85792

Michael Petrinovic 2018
'''

from ucsmsdk.utils.converttopython import convert_to_ucs_python

# Log file that you downloaded of the XML Recording
log_path = "/Users/mipetrin/Downloads/mipetrin-clone-3-create-delete_xmlReq.log"

# Call the conversion method and execute it with the log file and print to screen
convert_to_ucs_python(xml=True, path=log_path)

# END
