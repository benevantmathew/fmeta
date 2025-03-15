@echo off
setlocal
echo =================================
echo Welcome to setup. This setup will create local virtual env
echo you can rerun this without any issue
@REM ############################################################################## notes
@REM python 3.9 tested
@REM ############################################################################## PYTHON VERSION VERY IMPORTANT
set "python_version=312"
echo Using Python %python_version%
@REM ############################################################################## other variables
:: Get the user directory 
set "userdir=%userprofile%"
@REM ############################################################################## Python exe
if exist "%userdir%\AppData\Local\Programs\Python\Python%python_version%\python.exe" (
    set python_exe="%userdir%\AppData\Local\Programs\Python\Python%python_version%\python.exe"
) else (
    if exist "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python%python_version%_64\python.exe" (
        set python_exe="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python%python_version%_64\python.exe"
    ) else (
        exit
    )
)
@REM ##############################################################################
@REM get script file dir
set script_dir=%~dp0
@REM Remove trailing backslash
if "%script_dir:~-1%"=="\" set script_dir=%script_dir:~0,-1%
@REM set root dir
set rootdir=%script_dir%/..
@REM cd to root dir
cd %rootdir%
@REM get dir name
set "folder=%cd%"
@REM get the dir name alone
for %%A in ("%folder%") do set "folder=%%~nxA"
@REM set the env name
set "name=%folder%-py%python_version%-env"
@REM create envs folder is not exist
if not exist "%userdir%\envs" (
    mkdir "%userdir%\envs"
) 
@REM check if env already exist
if exist "%userdir%\envs\%name%" (
    echo "%userdir%\envs\%name%" folder exists
) else (
    echo Creating envs
    %python_exe% -m venv "%userdir%\envs\%name%"
)
call %userdir%\envs\%name%\Scripts\activate
python -m pip install --upgrade pip
@REM ##############################################################################
deactivate
pause