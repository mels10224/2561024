
@echo off
echo Компиляция скрипта в exe...
pip install pyinstaller
pyinstaller --onefile --hidden-import=pkg_resources.py2_warn main.py

echo Добавление скрипта в автозагрузку...
set SCRIPT_DIR=%~dp0
call python -c "import os, shutil; bat_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'); shutil.copyfile(os.path.join('%SCRIPT_DIR%', 'main.exe'), os.path.join(bat_path, 'OpenBot.bat'))"

echo Компиляция завершена.
pause
