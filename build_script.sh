#!/usr/bin/env bash

# Check to make sure things are up to date.
echo "====================================="
echo "Updating Ubuntu"
echo "====================================="

sudo apt update > /dev/null 2>&1 && echo "Update complete..."

echo "====================================="
echo "Starting PIP installs for rockitchef."
echo "====================================="

# Installing Python 3 and dependancies
PY_ARRAY=(python3.6 python3-pip python3-django python3-venv)
for package in "${PY_ARRAY[@]}"; do
    if command -v $package &>/dev/null; then
        echo $package " is installed"
    else
        echo "Installing "$package" now..."
        sudo apt-get install -y $package
        echo "====================================="
        echo "PIP installs for rockitchef."
        echo "====================================="
        sudo -H pip3 install -r requirements.txt
    fi
done
