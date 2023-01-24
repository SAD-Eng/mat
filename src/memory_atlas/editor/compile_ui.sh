#!/bin/bash

# https://stackoverflow.com/a/246128
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Compiles all .ui files in this directory into their appropriate generated .py files. This should be run
# as part of any CI build just to be sure, but we are also checking in the compiled files.
pyside6-uic -o "${SCRIPT_DIR}/ui_main_window.py" "${SCRIPT_DIR}/main_window.ui"
pyside6-rcc -o "${SCRIPT_DIR}/icons/ui_icons.py" "${SCRIPT_DIR}/icons/icons.qrc"

# convert line endings in case we're on Windows
dos2unix "${SCRIPT_DIR}/ui_main_window.py"
dos2unix "${SCRIPT_DIR}/icons/ui_icons.py"