@echo off
REM make a shortcut to this so you can call it from anywhere.
start cmd /c "Scripts\activate && python run.py"
REM pausing in case of errors to show them.
pause