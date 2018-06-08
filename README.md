Created by Michael Petrinovic 2018

Sample UCSM Python Scripts for:
* Cisco Live Melbourne 2018: BRKDCN-2602
* Cisco Live USA 2018: BRKDCN-2011

Be sure to copy the sample_ucs_my_credentials file. Modify the variables to specify your hostname and password. Save this file as ucs_my_credentials.py - as that it was all the scripts look for. Furthermore, within each script, it specifies during the connect phase if it will use UCSM or UCSM2, etc, so as to match up to the credentials file

Sample Usage:

```YAML
# python ucs_backup.py

# python ucs_inventory.py

# python ucs_compare.py

# python ucs_compute_details.py

# python ucs_python_conversion_java.py
```

"Ctrl + Alt + Q" to enable recording XML Link
```YAML
# python ucs_python_conversion_xml.py

# python ucs_python_skeleton_code.py

# python ucs_faults.py

# python ucs_kvm_launcher.py
```


WARNING:

These scripts are meant for educational/proof of concept purposes only - as demonstrated at Cisco Live and/or my other presentations. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and I am not responsible for any damage or data loss incurred as a result of their use
