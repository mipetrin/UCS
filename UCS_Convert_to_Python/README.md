A collection of Simple UCS Python Scripts that will help get you started with the UCS SDK. These are helper scripts to make your life easier.

> By default, the script will look for the my_credentials.ini in the current directory before searching the parent directory. Be sure to modify the groups (available UCS Domains) and username/password variables to match your environment. You can then use the -p or --platform to specify the UCS Domain to use for Script execution.

Detailed explanation of what each script achieves:
* ucs_python_classid_info.py
  * Extract all available Meta information about each UCS SDK Python Class
* ucs_python_conversion_java.py
  * Use this script to launch the UCS Java Client and then convert all actions you perform to the relevant Python UCS Code
* ucs_python_conversion_xml.py
  * After enabling the HTML 5 XML Recording link () and you have generated the log file, you can then use this script to convernt the XML Log file to the relevant Python UCS Code
* ucs_python_skeleton_code.py
  * Skeleton code structure that you can use as a template to paste the Python UCS Code (from the outputs of ucs_python_conversion_java.py and ucs_python_conversion_xml.py) to then be able to successfully execute the Python code


Sample Usage:

```YAML
# ucs_python_classid_info.py
```

```YAML
# python ucs_python_conversion_java.py --platform real
```

"Ctrl + Alt + Q" to enable recording XML Link
```YAML
# python ucs_python_conversion_xml.py
```

```YAML
# python ucs_python_skeleton_code.py
```


Created by Michael Petrinovic 2018

WARNING:

These scripts are meant for educational/proof of concept purposes only - as demonstrated at Cisco Live and/or my other presentations. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and I am not responsible for any damage or data loss incurred as a result of their use
