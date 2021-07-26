# linux-wireguard-notification
A simple notification for wireguard connection status on linux

# Steps to build and use:
1. Compile the cpp file using your compiler of choice
2. Make the owner of the executable from step 1 `root`, then add execution privileges to your own user. Use [SUID](https://www.linuxnix.com/suid-set-suid-linuxunix/) so that you don't have to run the program as `root` each time you want to use it. Make sure no user except `root` has the permission to write this file, otherwise you have an active privilege escalation exploit in your system!
3. Adjust the python script so that it matches your own paths.
4. Install the python script dependencies (you need pygobject)
5. (Optional) Add a keyboard shortcut to your DE so that you can easily use this tool!
