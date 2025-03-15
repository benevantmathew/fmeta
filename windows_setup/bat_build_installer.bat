:: batch script to build installer 
@echo off 
setlocal
@REM ############################################################################## PYTHON VERSION VERY IMPORTANT
set "python_version=312"
@REM ############################################################################## other variables
:: Get the user directory 
set "userdir=%userprofile%"
@REM ##############################################################################
@REM get script file dir
set script_dir=%~dp0
@REM Remove trailing backslash
if "%script_dir:~-1%"=="\" set script_dir=%script_dir:~0,-1%
@REM set root dir
set rootdir=%script_dir%/..

set build_workspace=%rootdir%\build
set "folder=dircomply"
@REM ############################################
@REM get version no
set /p version="Enter version no: "
@REM #####################################################################################
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
@REM #####################################################################################
echo "running pyinstaller....."
pyinstaller --clean main.spec
@REM #####################################################################################
echo "copy installer file....."
@REM #copy installer file
set source_path=.\dist\main.exe
set dest_path=..\releases\v%version%\repo_compare_v%version%.exe
@REM create required directories
if not exist "..\releases" (
    mkdir "..\releases"
)
if not exist "..\releases\v%version%" (
    mkdir "..\releases\v%version%"
)
copy /y "%source_path%" "%dest_path%"
@REM #####################################################################################
pause