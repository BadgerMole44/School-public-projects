# Filename_cleaner.py
## Add Program to the System Path:
Below will describe how to enable program execution from the system path for Windows and Linux (Specifically WSL Ubuntu).
### Windows: Add Directory to Path 
1. Place the .py script file in a directory.
2. Go to Advanced System Settings > Environment Variables.
3. Under system variables Click Path and then click Edit..
4. Click New, type the absolute path to the directory, and click ok.
5. Under system variables if PATHEXT does not have a .py extension association (;.PY;.PYW) add it.
6. Go to Default Apps.
7. Scroll down to .py.
8. If .py is not already associated with python select it.
9. Restart your computer.
### Linux: Add Script to Path
*Note: Scripts were developed and tested on WSL Ubuntu so some steps may need to be altered for other linux distributions*
1. The first line of each script in python-scripts contains the shebang #!/usr/bin/python3. Shebangs tell the Linux OS what interpreter to use to execute the file.
2. Place the script within a any directory.
3. Ensure the script is executable using by running the following from the terminal: chmod +x script_name.py
4. Create a link from the script to executables using the following from, the terminal: ls -s absolute/path/to/script_name.py /usr/local/bin/executable_name. The executable name need not include the .py extension. 