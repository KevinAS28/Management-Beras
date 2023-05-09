import os
# import winshell

current_dir = os.getcwd()
python_exe = os.path.join(current_dir, 'python', 'python.exe')

with open('Updater.bat', 'w+') as updater_file:
    git_dir = os.path.join(current_dir, 'portablegit')
    updater_content = f'''set gitdir={git_dir}\nset path=%gitdir%\cmd;%path%\ngit add beraspakde cost_calculator static templates create_shortcut.py get-pip.py install_run.py manage.py shell_module.py\npause'''    
    updater_file.write(updater_content)

with open('Install.bat', 'w+') as install_file:
    python_dir = os.path.join(current_dir, 'python', 'python.exe')
    install_content = f'''call '{python_exe}' get-pip.py\ncall .\python\Scripts\pip.exe install Django pywin32'''
    install_file.write(install_content)

with open('Jalankan.bat', 'w+') as run_file:
    python_dir = os.path.join(current_dir, 'python', 'python.exe')
    run_content = f'''start {python_exe} manage.py runserver 0.0.0.0:8000\ntimeout 5\nexplorer http://127.0.0.1:8000/cost_calculator/daily/\npause'''    
    run_file.write(run_content)

os.system(f'call Install.bat')
os.system(f'call "Buat Shortcut.bat"')
os.system(f'call Jalankan.bat')
# os.getlogin()


print('Done')
input()