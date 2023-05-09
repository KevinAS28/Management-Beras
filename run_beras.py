from threading import Thread
import os
import time
from pathlib import Path
import json

with open(os.path.join(str(Path.home()), 'beras.dat'), 'r') as dat_file:
    dat = json.loads(dat_file.read())
    current_dir = dat['project_path']
    python_exe = os.path.join(current_dir, 'python.exe')



def start_server():
    os.system(f'"{python_exe}" {os.path.join(current_dir, "manage.py")} runserver 0.0.0.0:8000')

Thread(target=start_server, args=[]).start()
time.sleep(5)
os.system('explorer http://127.0.0.1:8000/cost_calculator/daily/')