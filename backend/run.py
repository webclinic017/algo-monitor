# -*- coding: utf-8 -*-

import os
import sys
import platform
import subprocess

path = sys.argv[1]
entry_path = sys.argv[2]
config_guid = sys.argv[3]

os.chdir(path)
    
plat = platform.system()
if plat == 'Windows':
    subprocess.call(f'Scripts\\python {entry_path} {config_guid}')
else:
    subprocess.call(['bin/python',entry_path,config_guid])
