from models.strat import Strat
from repository.firestore import save as fs_save, get as fs_get, get_all as fs_get_all
from repository.storage import upload as st_upload, download as st_download
from helpers.helpers import zipdir, unzipdir, unzipdir_bytes
from subprocess import Popen
import os
import platform
import psutil
import zipfile
import io
from helpers.interval import Interval

_collection = 'strats'

def upload_strat(file_bytes, strat):
    unzipdir_bytes(file_bytes, f'public/strat_{strat.id}')

def save_strat(strat: Strat):
    strat_path = f'public/strat_{strat.id}'
    temp_path = f'public/temp_{strat.id}.zip'
    zipdir(temp_path, strat_path)
    st_upload(strat.id, temp_path)
    fs_save(_collection, strat.id, strat.toDict())
    os.remove(temp_path)

def get_strat(id: str):
    strat_dict = fs_get(_collection, id)
    if strat_dict is None: return None
    strat = Strat.fromDict(strat_dict)
    strat_path = f'public/strat_{strat.id}'
    if not os.path.isdir(strat_path):
        temp_path = f'public/temp_{strat.id}.zip'
        st_download(strat.id, temp_path)
        unzipdir(temp_path, strat_path)
        os.remove(temp_path)
    return strat

def get_strats_list():
    strats = [Strat.fromDict(s) for s in fs_get_all(_collection)]
    return strats

def get_all_strats():
    strats = get_strats_list()
    strats_full = []
    for s in strats:
        strats_full.append(get_strat(s))
    return strats

def run_strat(id: str):
    strat = get_strat(id)
    if strat is None: return None

    plat = platform.system()
    if plat == 'Windows':
        process = Popen(f'python {strat.entry_path}', cwd=f'public/strat_{strat.id}')
    else:
        process = Popen(['python', strat.entry_path], cwd=f'public/strat_{strat.id}')

    return process

def run_status(process):
    return psutil.pid_exists(process.pid)

def stop_strat(process):
    if run_status(process): process.kill()
    return process.pid
    
def status_check(process_list):
    for p in process_list[:]:
        if not run_status(p):
            process_list.remove(p)

def start_status_check(process_list):
    interval = Interval(lambda: status_check(process_list), 10, 'status_check')
    interval.start()
    return interval