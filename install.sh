#!/bin/bash

# change directory to this projects directory
cd "$(dirname "$0")" || exit 1

# create virtual environment to prevent installation of the required libraries in the global python interpreter
python3 -m venv .venv || exit 1

# install required libraries
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r ./requirements.txt

echo
echo "If you want this command to available from everywhere, then add the following line to ~/.bash_aliases"
echo "alias yt='$(realpath src/yt/run.sh)'"

# simple output for the user
echo
echo "Project is ready to go"
echo
