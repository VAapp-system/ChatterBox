#!/bin/bash

python3 setup/category_extract.py $1
python3 setup/app_extract.py $1
python3 setup/page.py $1
python3 setup/command.py $1
python3 setup/name.py $1
python3 setup/description.py $1
python3 setup/NEextract.py $1

mkdir debug
mkdir logfile
mkdir error
mkdir user_storage
mkdir canvas
mkdir tree
mkdir check
