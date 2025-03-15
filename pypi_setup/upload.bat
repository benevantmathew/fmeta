@echo off
echo Cleaning build directories...

:: Run the clean.py script to remove old build artifacts
python pypi_setup\clean.py

echo Building distribution packages...
python setup.py sdist bdist_wheel

echo Uploading to PyPI...
twine upload dist/*

echo Done!
