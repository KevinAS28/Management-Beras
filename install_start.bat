set PYTHONPATH=C:\Users\kevin\Documents\beraspakde\python.exe
call python.exe get-pip.py
call .\Scripts\pip.exe install Django 
start python.exe manage.py runserver 0.0.0.0:8000
timeout 3
explorer http://127.0.0.1:8000
pause