#!/usr/bin/env python
'''
Simple script to obtain Meta info about a specific classId

Requires the UCS SDK: pip install ucsmsdk

Michael Petrinovic 2018
'''

from ucsmsdk.ucscoreutils import get_meta_info

# Change the class_id to be whatever Class you want to find out more details about
meta = get_meta_info(class_id="ComputeBlade") # Compute Blades
# meta = get_meta_info(class_id="faultInst") # UCS Fault Instances
# meta = get_meta_info(class_id="networkElement") # Fabric Interconnects
# meta = get_meta_info(class_id="lsServer") # Service Profile
# meta = get_meta_info(class_id="fabricVlan") # VLANs
# meta = get_meta_info(class_id="fabricVsan") # VSANs
# meta = get_meta_info(class_id="aaaModLR") # Audit Logs

'''
To find the Python class of the managed object:
* In the Cisco UCS Manager GUI, right-click any object and select the Copy XML option.
* Paste the XML in a text editor. The first word following < is the class identifier (class ID) of the object.
'''
# Print out all internal information regarding the class selected
print meta
