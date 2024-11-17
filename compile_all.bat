@echo off
echo Kompiliere alle Browser-Versionen...

cd Windows_Google_Chrome
call compile.bat

cd ../Windows_Mozilla_Firefox
call compile.bat

cd ../Windows_Microsoft_Edge
call compile.bat

cd ..
echo Alle Versionen wurden kompiliert!
pause