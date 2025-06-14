#!/bin/bash

rm -rf build || mkdir -p build && rsync -avc --progress . build --exclude build

cd build || exit

python3 setup.py install_requires

python3 setup.py build_ext --inplace

# if $1 is not dev
if [ "$1" != "dev" ]; then
  #remove all python file except __init__.py
  find . -name "*.py" ! -name "__init__.py" ! -name "setup.py" -type f -delete
  find . -name "*.c" -type f -delete
fi

python3 setup.py bdist_wheel

cd .. || exit

cp -r build/dist dist && rm -rf build
