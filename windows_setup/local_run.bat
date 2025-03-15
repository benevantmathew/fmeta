@echo off
setlocal
@REM ############################################################################## PYTHON VERSION VERY IMPORTANT
set "python_version=312"
@REM ############################################################################## other variables
:: Get the user directory 
set "userdir=%userprofile%"
@REM ############################################################################## Activate local env
@REM get script file dir
set script_dir=%~dp0
@REM Remove trailing backslash
if "%script_dir:~-1%"=="\" set script_dir=%script_dir:~0,-1%
@REM cd to root dir
cd %script_dir%/..
@REM get current dir path
set "folder=%cd%"
@REM get the dir name alone
for %%A in ("%folder%") do set "folder=%%~nxA"
@REM set the env name
set "name=%folder%-py%python_version%-env"
@REM check if env already exist
if exist "%userdir%\envs\%name%" (
    echo Enabling venv
) else (
    echo No venv. Run local_setup first.
    pause
    exit /b 1
)
@REM Set paths
set "venv_path=%userdir%\envs\%name%\Scripts\activate.bat"
set "git_path=C:\Program Files\Git\bin"
set "win32_path=C:\Windows\System32"
@REM Start new command window with Python venv and Git in PATH
start cmd.exe /k "set PATH=%git_path%;%PATH%;%win32_path% & call %venv_path%"