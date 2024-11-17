@echo off
echo Starte Build-Prozess...

:: Navigiere zum Verzeichnis mit den Projektdateien
cd C:\Users\CC-Student\projects\comcave_login_logout_bot\Windows_Google_Chrome

:: Kompiliere die Resource-Datei (.rc) zu einer .res-Datei
rc resources.rc
if errorlevel 1 goto :error

:: Kompiliere den Quellcode und verlinke die .res-Datei, um eine .exe mit Icon zu erstellen
cl comcave_bot.cpp resources.res /Fe:comcave_bot.exe
if errorlevel 1 goto :error

echo Build erfolgreich abgeschlossen!
goto :end

:error
echo Fehler beim Build-Prozess.
pause

:end
pause
