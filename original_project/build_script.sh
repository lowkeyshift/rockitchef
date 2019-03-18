#!/usr/bin/env bash

set -e

vDir="./rockitchef/"
readonly sourceFile="webapp"
FILE="./requirements.txt"
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
PY_ARRAY=(python3.6 python3-pip python3-venv sqlite3 libpq-dev postgresql postgresql-contrib)
for package in "${PY_ARRAY[@]}"; do
    if command -v $package &>/dev/null; then
        echo $package " is installed"
    else
        echo "Installing "$package" now..."
        sudo apt-get install -y $package
        echo "====================================="
        echo "PIP installs for rockitchef."
        echo "====================================="
    fi
done

echo "====================================="
echo "Installing Postgres"
echo "====================================="

# Constants
declare -r PSQL_USER="sudo -i -u postgres"
declare -r PSQL_COMMAND="/usr/bin/psql -U postgres -c"
declare -r PSQL_CHECK_COMMAND="/usr/bin/psql -tAc -U postgres -c"
declare CHECK_INSTALLED=$(basename $(which psql))

declare -r DB_USER="rockitmaster"
declare -r PSSWD="Testingmybiscuits"
declare -r DB_NAME="recipes"

function install_postgres() {
  # Checking wether postgresql is installed or not
  if [ $CHECK_INSTALLED == 'psql' ]
  then
      echo "PostgreSQL already installed."
  else
    echo "Installing PostgreSQL." \
    sudo apt-get update \
    sudo apt-get install -y libpq-dev postgresql postgresql-contrib
  fi
}

function create_user() {
  # Here I am running the createuser command as the postgres user to create a read-only datadog user
  # -D=Cannot create databases, -R=Cannot create roles, -S=Not Superuser
  if $PSQL_USER createuser -U postgres -D -R -S $DB_USER && echo "$DB_USER user has been created.";
  then
      echo "...${DB_USER} user has been created..."
  else
      echo "...${DB_USER} user aleady exists..."
  fi
}

function create_db() {
     # Will create a database with the name provided, or fail if exists
     $PSQL_USER createdb $DB_NAME && echo "Database $DB_NAME has been created."
}

function auth_priveledge() {
  # Give the user a password and databse privileges
  $PSQL_USER $PSQL_COMMAND "ALTER USER $DB_USER WITH PASSWORD '$PSSWD'"
  #$PSQL_USER $PSQL_COMMAND "GRANT SELECT ON DATABASE $DB_NAME TO $DB_USER"
  $PSQL_USER $PSQL_COMMAND "GRANT SELECT ON pg_stat_database TO $DB_USER"
}

echo "...Checking if Postgres installed..." && install_postgres && \
echo "...Creating user ${DB_USER}..." && create_user && \

# Check is DB already exists
if create_db;
then
    echo "Database ${DB_NAME} already exists"
else
    echo "####-- Database ${DB_NAME} does not exist --####"
    echo "...Creating Database ${DB_NAME}..."
fi

echo "...Granting Auth PRIVILEGES..." && auth_priveledge

#sudo -H pip3 install -r requirements.txt
#sudo -H -u postgres -c "psql CREATE DATABASE ${psql_database};"
#sudo -H -u postgres -c "psql CREATE USER ${psql_user} WITH PASSWORD '@^EE^WGBDY#ZZ&@JSH#UYI';"
#sudo -H -u postgres -c "psql ALTER ROLE ${psql_user} SET client_encoding TO 'utf8';"
#sudo -H -u postgres -c "psql ALTER ROLE ${psql_user} SET default_transaction_isolation TO 'read committed';"
#sudo -H -u postgres -c "psql ALTER ROLE ${psql_user} SET timezone TO 'UTC';"
#sudo -H -u postgres -c "psql GRANT ALL PRIVILEGES ON DATABASE ${psql_database} TO ${psql_user};"

echo "====================================="
echo "Building VENV for rockitchef."
echo "====================================="
if [ ! -d ${vDir} ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir ${vDir}
  python3 -m venv ${vDir}${sourceFile}
else
    echo "...${vDir} already exists..."
fi

#source ${vDir}${sourceFile}/bin/activate
echo "####################################################################"
echo "#${sourceFile} virtual environment is now available.                      #"
echo "#To activate virtualenv:                                           #"
echo "#Run command: source ${vDir}${sourceFile}/bin/activate.             #"
echo "####################################################################"
echo "-----------------------------------------------------------------------------------"
echo "Install Datadog."
echo "====================================="
declare CHECK_DD_INSTALLED=$(basename $(which datadog-agent))
if [ $CHECK_DD_INSTALLED == 'datadog-agent' ]
then
    echo "datadog-agent already installed."
else
  echo "Installing datadog-agent." \
  echo "Enter Datadog API KEY: "
  read DD_API_KEY
  export DD_API_KEY=${DD_API_KEY}
  bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
  echo "====================================="
  echo "Starting Datadog."
  echo "====================================="
  sudo systemctl start datadog-agent
  echo "====================================="
  echo "Datadog Restarted & Running...."
  echo "====================================="
fi
