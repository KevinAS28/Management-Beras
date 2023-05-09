from pathlib import Path
import os
import json

with open(os.path.join(str(Path.home()), 'beras.dat'), 'r') as dat_file:
    dat = json.loads(dat_file.read())
    current_dir = dat['project_path']
    python_exe = os.path.join(current_dir, 'python.exe')
    git_exe = os.path.join(current_dir, 'cmd', 'git.exe')

commands = [
    f'{git_exe} add .',
    f'{git_exe} stash',
    f'{git_exe} pull origin main',
]