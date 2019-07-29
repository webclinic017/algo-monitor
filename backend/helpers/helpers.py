# -*- coding: utf-8 -*-

import zipfile
import os
import io
import json

def zipdir(out_path, dir_path):
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                cwd = os.getcwd()
                os.chdir(root.split(os.sep)[0])
                zipf.write(os.path.relpath(os.path.join(root, file), os.path.join(dir_path, './')))
                os.chdir(cwd)

def unzipdir(zip_path, out_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(out_dir)

def unzipdir_bytes(file_bytes, out_dir):
    with zipfile.ZipFile(io.BytesIO(file_bytes), 'r') as zf:
        zf.extractall(out_dir)

def mkdir_conditional(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def is_json(myjson):
	try:
		json_object = json.loads(myjson)
	except:
		return False
	return True