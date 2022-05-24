#!/bin/bash
cd "$(dirname "$0")" || exit
git pull -q || exit
./install.sh || exit

echo "Project should be updated"
