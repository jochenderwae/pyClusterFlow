#!/bin/bash

VENV_PATH="worker_venv"

pip install pynacl

python3 -m venv $VENV_PATH
source ./$VENV_PATH/bin/activate
python setup.py install