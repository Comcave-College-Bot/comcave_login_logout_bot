@echo off
echo Kompiliere ComCave Bot - Single Tap Edge Version...
windres resources.rc -O coff -o resources.res
cl.exe /nologo /EHsc comcave_bot.cpp resources.res /link shell32.lib user32.lib /out:comcave_bot_single_edge.exe
if %errorlevel% equ 0 (
    echo Kompilierung erfolgreich! comcave_bot_single_edge.exe wurde erstellt.
    del *.obj *.res
) else (
    echo Fehler bei der Kompilierung!
)
pause