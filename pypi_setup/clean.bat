@echo off
echo Cleaning build directories...

:: Run the clean.py script to remove old build artifacts
python pypi_setup\clean.py

echo Done!
