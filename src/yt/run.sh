#!/bin/bash
# execute the package with the .venv python interpreter
# just python3 would use the global python that doesn't have the required packages installed
"$(dirname "$0")/../../.venv/bin/python3" -O "$(dirname "$0")/../yt" "$@"

