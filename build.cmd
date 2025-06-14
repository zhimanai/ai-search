@echo off
REM Remove build directory if it exists
IF EXIST build (
    rmdir /s /q build
)
mkdir build

REM Copy all files except build directory itself
xcopy * build\ /E /I /EXCLUDE:build

cd build || exit /b

python setup.py install_requires

python setup.py build_ext --inplace

REM Check if first argument is not "dev"
IF NOT "%1"=="dev" (
    REM Remove all .py files except __init__.py and setup.py
    for /r %%f in (*.py) do (
        if /I not "%%~nxf"=="__init__.py" if /I not "%%~nxf"=="setup.py" del "%%f"
    )
    REM Remove all .c files
    for /r %%f in (*.c) do del "%%f"
)

python setup.py bdist_wheel

cd .. || exit /b

xcopy build\dist dist\ /E /I
rmdir /s /q build