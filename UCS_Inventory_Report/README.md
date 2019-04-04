Sample UCS Python Script that will obtain information about your UCS Domain and generate a HTML Report for you - that you can then interactively search through and find details. It can also be extended to include additional details within the report, by using the built in reporting capabilities of UCS. See source code for how it can be extended.

> By default, the script will look for the my_credentials.ini in the current directory before searching the parent directory. Be sure to modify the groups (available UCS Domains) and username/password variables to match your environment. You can then use the -p or --platform to specify the UCS Domain to use for Script execution.

Sample Usage:

```YAML
# python ucs_inventory.py --platform real
```

> Could also make use of the [ucs_python_classid_info.py](https://github.com/mipetrin/UCS/blob/master/UCS_Convert_to_Python/ucs_python_classid_info.py) found in my [UCS/UCS_Convert_to_Python Folder](https://github.com/mipetrin/UCS/tree/master/UCS_Convert_to_Python) of my GitHub to identify what other elements could be called upon for the Inventory Spec


Created by Michael Petrinovic 2018

WARNING:

These scripts are meant for educational/proof of concept purposes only - as demonstrated at Cisco Live and/or my other presentations. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and I am not responsible for any damage or data loss incurred as a result of their use
