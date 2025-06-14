@echo off

REM Remove or create build directory
if exist build (
    rmdir /s /q build
) else (
    mkdir build
)

REM Copy files to build directory excluding build itself
xcopy . build /E /I /Y /EXCLUDE:exclude.txt

REM Create exclude.txt temporarily for xcopy
echo build\ > exclude.txt
echo .git\ >> exclude.txt
del exclude.txt

REM Change to build directory
cd build || exit /b

REM Install requirements
python setup.py install_requires

REM Build extensions in place
python setup.py build_ext --inplace

REM Check if first argument is not "dev"
if not "%1"=="dev" (
    REM Remove all .py files except __init__.py and setup.py
    for /r %%f in (*.py) do (
        if not "%%~nxf"=="__init__.py" if not "%%~nxf"=="setup.py" del "%%f"
    )
    REM Remove all .c files
    for /r %%f in (*.c) do del "%%f"
)

REM Build wheel
python setup.py bdist_wheel

REM Go back to parent directory
cd .. || exit /b

REM Copy dist folder and remove build
xcopy build\dist dist /E /I /Y
rmdir /s /q build