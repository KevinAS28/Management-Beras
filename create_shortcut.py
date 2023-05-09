import win32com.client
from pathlib import Path
import os

def create_shortcut(target=os.path.join(str(Path.home()), 'Desktop', 'Calculator Beras.lnk')):
    ws = win32com.client.Dispatch("wscript.shell")
    scut = ws.CreateShortcut(target)
    scut.TargetPath = f'\"{os.path.join(os.getcwd(), "Jalankan.bat")}\"'
    scut.IconLocation = f'{os.path.join(os.getcwd(), "icon.ico")}'
    scut.Save()

try:
    create_shortcut()
except:
    create_shortcut(os.path.join(os.getcwd(), 'Calculator Beras.lnk'))   