@echo off
rc resources.rc
if errorlevel 1 goto :error
cl comcave_bot.cpp resources.res /Fe:comcave_bot.exe
if errorlevel 1 goto :error
echo Build erfolgreich abgeschlossen!
goto :end

:error
echo Fehler beim Build-Prozess.

:end
pause
