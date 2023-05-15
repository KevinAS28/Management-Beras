import os
import json
from pathlib import Path
# import winshell

current_dir = os.getcwd()
python_exe = os.path.join(current_dir, 'python.exe')



with open('Install.bat', 'w+') as install_file:
    install_content = f'''call "{python_exe}" get-pip.py\ncall .\Scripts\pip.exe install Django pywin32 requests'''
    install_file.write(install_content)

with open('Jalankan.bat', 'w+') as run_file:
    run_content = f'''call "{python_exe}" "{os.path.join(current_dir, "run_beras.py")}"\necho "Selesai"\npause'''    
    run_file.write(run_content)

with open('Updater.bat', 'w+') as run_file:
    run_content = f'''call "{python_exe}" "{os.path.join(current_dir, "updater.py")}"\necho "Selesai"\npause'''    
    run_file.write(run_content)


with open(os.path.join(str(Path.home()), 'beras.dat'), 'w+') as dat_file:
    dat_file.write(json.dumps(
        {'project_path': current_dir}
    ))

os.system(f'call run_install_all.bat')

# os.getlogin()


print('Done')
input()