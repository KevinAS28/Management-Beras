from pathlib import Path
import os
import subprocess
import json


with open(os.path.join(str(Path.home()), 'beras.dat'), 'r') as dat_file:
    dat = json.loads(dat_file.read())
    current_dir = dat['project_path']
    python_exe = os.path.join(current_dir, 'python.exe')
    git_exe = os.path.join(current_dir, 'portablegit', 'cmd', 'git.exe')

commands = [
    f'call "{git_exe}" add .',
    f'call "{git_exe}" stash',
    f'call "{git_exe}" pull origin main',
]

def updater(out=True):
    for com in commands:
        o = subprocess.check_output(com, shell=True)
        if out:
            print(o)

if __name__=='__main__':
    updater()