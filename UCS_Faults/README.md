Sample UCS Python Script that will allow you to obtain all the Faults currently active within an ACI Environment.

> It will then produce a simple report for you, that includes all the faults, what severity, how many occurrences, possible causes, etc.

> By default, the script will look for the my_credentials.ini in the current directory before searching the parent directory. Be sure to modify the groups (available UCS Domains) and username/password variables to match your environment. You can then use the -p or --platform to specify the UCS Domain to use for Script execution.

Sample Usage:

```YAML
# python ucs_faults.py --platform real
```

Created by Michael Petrinovic 2018

WARNING:

These scripts are meant for educational/proof of concept purposes only - as demonstrated at Cisco Live and/or my other presentations. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and I am not responsible for any damage or data loss incurred as a result of their use
