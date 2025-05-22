### CONFIGURATION SCRIPT ###########################
# Authors: ACG
# Usage: python3 configure.py 'configs/filename.cfg' 
# Notes:
####################################################

import os
import sys
import csv
from commands.helper_functions import *

if len(sys.argv) < 3:
    print("Error: please specify serial interface *and* configuration (.cfg) file")
    sys.exit()
interface = sys.argv[1]
config_file = sys.argv[2]

settings_string = read_config_file(config_file)
serial_command = make_serial_command(settings_string)
os.system(f'python3 commands/serial_interface.py {interface} {serial_command}')


