:: batch script to create spec file for weldeasy installer 
@echo off 
setlocal
@REM ############################################################################## PYTHON VERSION VERY IMPORTANT
set "python_version=312"
@REM ############################################################################## other variables
:: Get the user directory 
set "userdir=%userprofile%"
@REM ############################################
@REM get script file dir
set script_dir=%~dp0
@REM Remove trailing backslash
if "%script_dir:~-1%"=="\" set script_dir=%script_dir:~0,-1%
@REM set root dir
set rootdir=%script_dir%/..
@REM set build dir
set build_workspace=%rootdir%\build
set "folder=fmeta"
@REM ############################################
if not exist "%build_workspace%" (
    mkdir "%build_workspace%"
) 
cd %build_workspace%
for %%A in ("%folder%") do set "folder=%%~nxA"
set "name=%folder%-py%python_version%-env"
if exist "%userdir%\envs\%name%" (
    echo Enabling venv.....
) else (
    echo No local environment.
    exit /b 1
)
set "path=%userdir%\envs\%name%\Scripts\activate.bat"
call %path%
@REM ############################################
echo "running pyinstaller....."
pyi-makespec "..\main.py" --onefile -F --noconsole --add-data "..\main.py;."
pause