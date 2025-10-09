#!/bin/bash
# Get the directory where the script is located, which is the project root
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Change to the project root directory
cd "$SCRIPT_DIR" || exit

# Set PYTHONPATH to the project root
export PYTHONPATH="$SCRIPT_DIR"

# Fixing UI scaling on Rocky Linux. Default seems to be enlarged.
export QT_SCALE_FACTOR=1.0

# Run the python application as a module
/opt/Autodesk/python/2026.1/bin/python -m src.app
