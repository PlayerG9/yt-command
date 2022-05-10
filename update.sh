#!/bin/bash
cd "$(dirname "$0")" || exit
git pull || exit
./install.sh || exit

echo "Project should be updated"
