@echo off
echo Cleaning build directories...

:: Run the clean.py script to remove old build artifacts
python pypi_setup\clean.py

echo Building distribution packages...
python setup.py sdist bdist_wheel

:: Find the latest .whl file in the dist folder
for /f %%i in ('dir /b /o-d dist\*.whl') do set latest_whl=dist\%%i & goto install

:install
if not exist "%latest_whl%" (
    echo ERROR: No wheel file found in dist directory!
    exit /b 1
)

echo Installing package locally...
pip install --force-reinstall "%latest_whl%"

echo Done!
