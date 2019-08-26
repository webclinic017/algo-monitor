import zipfile
import os

def zipdir(out_path, dir_path):
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(dir_path)))

for dir_name in next(os.walk('.'))[1]:
    zipdir(f'{dir_name}.zip',dir_name)