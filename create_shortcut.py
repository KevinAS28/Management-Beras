import win32com.client
from pathlib import Path
import os

ws = win32com.client.Dispatch("wscript.shell")
scut = ws.CreateShortcut(os.path.join(str(Path.home()), 'Desktop', 'Calculator Beras.lnk'))
scut.TargetPath = f'\"{os.path.join(os.getcwd(), "Jalankan.bat")}\"'
scut.IconLocation = f'{os.path.join(os.getcwd(), "icon.ico")}'
scut.Save()