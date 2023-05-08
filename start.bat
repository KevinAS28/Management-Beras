set PYTHONPATH=C:\Users\kevin\Documents\beraspakde\python.exe
start python.exe manage.py runserver 0.0.0.0:8000
timeout 3
explorer http://127.0.0.1:8000/cost_calculator/daily/
pause