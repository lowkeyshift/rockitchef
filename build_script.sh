#!/usr/bin/env bash

vDir="./rockitchef/"
readonly sourceFile="webapp"
FILE="./requirements.txt"
echo "Enter Datadog API KEY: "
read DD_API_KEY
export DD_API_KEY=${DD_API_KEY}
# Check to make sure things are up to date.
echo "====================================="
echo "Updating Ubuntu"
echo "====================================="

sudo apt update > /dev/null 2>&1 && echo "Update complete..."

# Writing requirements file for pip.
echo "====================================="
echo "Writing Requirements File."
echo "====================================="
/bin/cat <<EOM >$FILE
beautifulsoup4==4.6.0
fake-useragent==0.1.11
Jinja2==2.10
jsondiff==1.1.2
PyYAML==3.12
requests==2.21.0
virtualenv==16.4.3
EOM

echo "====================================="
echo "Starting PIP installs for rockitchef."
echo "====================================="

# Installing Python 3 and dependancies
PY_ARRAY=(python3.6 python3-pip python3-venv sqlite3)  
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

echo "====================================="
echo "Building VENV for rockitchef."
echo "====================================="
mkdir ${vDir}
python3 -m venv ${vDir}${sourceFile}
source ${vDir}${sourceFile}/bin/activate
echo "===================================== \n"
echo "${sourceFile} virtual environment is now running.\n"
echo "====================================="
echo "\n"
echo "====================================="
echo "Install Datadog."
echo "====================================="
bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
sudo systemctl start datadog-agent
echo "====================================="
echo "Starting Datadog."
echo "====================================="

