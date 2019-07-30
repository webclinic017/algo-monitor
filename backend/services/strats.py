# -*- coding: utf-8 -*-

from models.strat import Strat
from repository.firestore import save as fs_save, get as fs_get, get_all as fs_get_all, delete as fs_delete
from repository.storage import upload as st_upload, download as st_download, delete as st_delete
from helpers.helpers import zipdir, unzipdir, unzipdir_bytes
from helpers.interval import Interval
from models.process_manager import ProcessManager
from services.results import dump_local_results
from subprocess import Popen
import os
import platform
import psutil
import zipfile
import io
import json
import shutil

_collection = 'strats'

def save_post_strat(file_bytes, strat: Strat):
    save_strat(file_bytes, strat)
    post_strat(strat)

def save_strat(file_bytes, strat: Strat):
    strat_path = f'public/strat_{strat.id}'
    strat_path_src = f'{strat_path}/src'

    unzipdir_bytes(file_bytes, strat_path)
    unzipdir_bytes(file_bytes, strat_path_src)
    if not os.path.isfile(os.path.join(strat_path_src, strat.entry_path)):
        shutil.rmtree(strat_path, ignore_errors=True)
        return False

    setup_strat_env(strat_path)
    return True

def post_strat(strat: Strat):
    strat_path = f'public/strat_{strat.id}'
    strat_path_src = f'{strat_path}/src'
    temp_path = f'public/temp_{strat.id}.zip'

    zipdir(temp_path, strat_path_src)
    
    st_upload(strat.id, temp_path)
    fs_save(_collection, strat.id, strat.toDict())

    os.remove(temp_path)

def get_strat(strat_id: str):
    strat_dict = fs_get(_collection, strat_id)
    if strat_dict is None: return None

    strat = Strat.fromDict(strat_dict)
    strat_path = f'public/strat_{strat.id}'
    strat_path_src = f'{strat_path}/src'

    if not os.path.isdir(strat_path):
        temp_path = f'public/temp_{strat.id}.zip'
        st_download(strat.id, temp_path)

        unzipdir(temp_path, strat_path)
        unzipdir(temp_path, strat_path_src)

        os.remove(temp_path)
        setup_strat_env(strat_path)
    return strat

def setup_strat_env(strat_path):
    os.system(f'virtualenv {strat_path} --no-site-packages')
    if os.path.isfile(f'{strat_path}/requirements.txt'):
        plat = platform.system()
        if plat == 'Windows':
            os.system(f'cd {strat_path} && Scripts\\pip install -r requirements.txt')
        else:
            os.system(f'cd {strat_path} && bin/pip install -r requirements.txt')

def delete_strat(strat_id: str):
    can_delete = len([x for x in ProcessManager.process_list if x['strat_id'] == strat_id]) == 0
    if can_delete:
        strat_path = f'public/strat_{strat_id}'
        if os.path.isdir(strat_path):
            shutil.rmtree(strat_path, ignore_errors=True)
        fs_delete(_collection, strat_id)
        st_delete(strat_id)
        return True
    return False

def get_strats_list():
    strats = Strat.fromListDict(fs_get_all(_collection))
    return strats

def get_all_strats():
    strats = get_strats_list()
    strats_full = []
    for s in strats:
        strats_full.append(get_strat(s))
    return strats

def create_config(run_id: str, strat_id: str, params: list):
    strat = get_strat(strat_id)
    if strat is None: return None

    config_path = f'public/strat_{strat.id}/config_{run_id}.json'
    with open(config_path, 'w') as file:
        file.write(json.dumps(params))

    return config_path

def remove_config(run_id: str, strat_id: str):    
    config_path = f'public/strat_{strat_id}/config_{run_id}.json'
    if os.path.isfile(config_path):
        os.remove(config_path)

def run_strat(run_id: str, strat_id: str):
    strat = get_strat(strat_id)
    if strat is None: return None

    plat = platform.system()
    if plat == 'Windows':
        # process = Popen(f'python {strat.entry_path} {run_id}', cwd=f'public/strat_{strat.id}') # ORIGINAL
        # process = Popen([f'public/strat_{strat.id}/Scripts/python',f'public/strat_{strat.id}/{strat.entry_path}',run_id]) #FUNCIONOU (working path zuada)
        process = Popen(f'python run.py public/strat_{strat.id} {strat.entry_path} {run_id}')
        # process = Popen(['python',strat.entry_path,run_id], cwd=f'public/strat_{strat.id}')
        # process = Popen([f'public/strat_{strat.id}/Scripts/python',f'public/strat_{strat.id}/{strat.entry_path}',run_id]) #FUNCIONOU (working path zuada), OUTRA IDEIA É CRIAR UM ARQUIVO PYTHON QUE RODA OUTROS ARQUIVOS PYTHONS, E EU PASSO O ID DE QUEM EU QUERO RODAR, AÍ PRO POPEN FICA MAIS FACIL
        #https://stackoverflow.com/questions/6943208/activate-a-virtualenv-with-a-python-script/14792407#14792407
        #https://stackoverflow.com/questions/8052926/running-subprocess-within-different-virtualenv-with-python
        # process = Popen(['cd',f'public/strat_{strat.id}',f'Scripts/python',f'{strat.entry_path}',run_id])#, cwd=f'public\\strat_{strat.id}')

        # process = Popen(['cd','public/strat_00b12360-10b5-4c5a-87d9-71c3f6f82334','Scripts/python','teste.py','123'])
        # process = Popen(['Scripts/python','teste.py','123'], cwd="public/strat_00b12360-10b5-4c5a-87d9-71c3f6f82334")
    else:
        process = Popen(['python','run.py',f'public/strat_{strat.id}',strat.entry_path,run_id])

    return process

# PROCESS

def run_status(process):
    return psutil.pid_exists(process.pid)

def stop_strat(process):
    if run_status(process): process.kill()
    return process.pid    

def start_status_check(interval):
    interval = Interval(lambda: status_check(), interval, 'status_check')
    interval.start()
    return interval

def status_check():
    for p in ProcessManager.process_list[:]:
        if p['process'] is None:
            active_processes = ProcessManager.get_active()
            if len(active_processes) < 1:
                process = run_strat(p['run_id'], p['strat_id'])
                ProcessManager.add_process(p['run_id'], process)
        else:
            dump_local_results(p['run_id'],p['strat_id'])
            if p['process'].poll() is not None: #not run_status(p['process']):
                a,b = p['process'].communicate()
                ProcessManager.remove(p['run_id'])
                remove_config(p['run_id'], p['strat_id'])
