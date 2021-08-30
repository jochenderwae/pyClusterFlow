#!/bin/bash

VENV_PATH="worker_venv"

sudo apt install libffi-dev libssl-dev

pip install --upgrade pip
pip install bcrypt cryptography
pip install pynacl

python3 -m venv $VENV_PATH
source ./$VENV_PATH/bin/activate
python setup.py install