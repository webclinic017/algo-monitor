# -*- coding: utf-8 -*-

import os
import sys

path = sys.argv[1]
entry_path = sys.argv[2]
config_guid = sys.argv[3]

os.chdir(path)
os.system(f'Scripts\\python {entry_path} {config_guid}')