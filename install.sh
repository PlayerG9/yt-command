#!/bin/bash

# change directory to this projects directory
cd "$(dirname "$0")" || exit 1

# create virtual environment to prevent installation of the required libraries in the global python interpreter
python3 -m venv .venv || exit 1

# install required libraries
.venv/bin/pip -q install --upgrade pip
.venv/bin/pip -q install -r ./requirements.txt

echo
echo "Virtual environment was created/updated"
echo

# add alias command (create if not exists)
ALIAS_COMMAND="alias yt='$(realpath src/yt/run.sh)'"
BASHRC_FILE="$HOME/.bashrc"
ALIAS_FILE="$HOME/.bash_aliases"
if [[ -f "$ALIAS_FILE" ]]; then
  # check if the command already exists in the file
  if grep -Fxq "$ALIAS_COMMAND" "$ALIAS_FILE"; then
    echo "'yt'-alias already exists"
  else
    echo "$ALIAS_COMMAND" >> "$ALIAS_FILE"
  fi
#elif [[ -f "$BASHRC_FILE" ]]; then
#  # check if the command already exists in the file
#  if grep -Fxq "$ALIAS_COMMAND" "$BASHRC_FILE"; then
#    echo "alias already exists"
#  else
#    echo "$ALIAS_COMMAND" >> "$BASHRC_FILE"
#  fi
else
  echo "Failed to create 'yt'-alias"
fi

# add bash completion (gets always replaced)
COMPLETION_DIRECTORY="$HOME/.bash_completion.d"
if [[ ! -d "$COMPLETION_DIRECTORY" ]]; then
  echo "Created '$COMPLETION_DIRECTORY' because it didn't exists"
  mkdir "$COMPLETION_DIRECTORY"
fi

COMPLETION_FILE="$COMPLETION_DIRECTORY/yt-completion.bash"
: > "$COMPLETION_FILE" # empty or create the file
echo '#!/usr/bin/env bash
complete -W "--help download search" yt
' >> "$COMPLETION_FILE"

RUN_COMPLETION_COMMAND="source \"$COMPLETION_FILE\""
eval "$RUN_COMPLETION_COMMAND"  # run once to update
if ! grep -Fxq "$RUN_COMPLETION_COMMAND" "$BASHRC_FILE"; then
  echo "$RUN_COMPLETION_COMMAND" >> "$BASHRC_FILE"
fi

# simple output for the user as confirmation
echo
echo "Project is ready to go"
echo
