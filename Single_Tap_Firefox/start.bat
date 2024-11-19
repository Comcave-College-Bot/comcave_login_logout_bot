@echo off
if exist comcave_bot_single_firefox.exe (
    start comcave_bot_single_firefox.exe
) else (
    :: Suche nach Python in verschiedenen Verzeichnissen
    for /f "delims=" %%i in ('dir /b /s /a:d "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python*" 2^>nul') do (
        if exist "%%i\pythonw.exe" (
            start "%%i\pythonw.exe" gui.py --redirect
            goto :found
        )
    )

    for /f "delims=" %%i in ('dir /b /s /a:d "C:\Python*" 2^>nul') do (
        if exist "%%i\pythonw.exe" (
            start "%%i\pythonw.exe" gui.py --redirect
            goto :found
        )
    )

    for /f "delims=" %%i in ('dir /b /s /a:d "C:\Program Files\Python*" 2^>nul') do (
        if exist "%%i\pythonw.exe" (
            start "%%i\pythonw.exe" gui.py --redirect
            goto :found
        )
    )

    :: Wenn keine Python-Installation gefunden wurde
    echo Python konnte nicht gefunden werden!
    echo Bitte installieren Sie Python (Version 3.x)
    pause
    goto :eof

    :found
)