#!/bin/bash

bash build.sh "$@"

pip3 install --upgrade --force-reinstall dist/ai_search-*.whl
