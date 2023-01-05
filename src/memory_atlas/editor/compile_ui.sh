#!/bin/bash

# Compiles all .ui files in this directory into their appropriate generated .py files. This should be run
# as part of any CI build just to be sure, but we are also checking in the compiled files.
pyside6-uic -o ui_mainwindow.py main_window.ui

# convert line endings in case we're on Windows
dos2unix ui_mainwindow.py