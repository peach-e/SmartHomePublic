#!/usr/bin/env bash
# ----------------------------------------------------------------- #
#  File   : setup_dev_environment.sh
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
PROJECT_DIR=$(cd $SCRIPT_DIR/.. && pwd)
VIRTUAL_ENV="virtualenv"

source "$SCRIPT_DIR/script_utils.sh"

function verify_software_installed {
    SW=$1
    SW_RESULT="$(which $SW)"
    if [ -z $SW_RESULT ]; then
        error "Required software '$SW' not found."
        exit 1
    fi
    info "Found $SW at $SW_RESULT"
}

verify_software_installed pip3

info "Installing Global Python Packages"
export PATH="$PATH:~/.local/bin"
pip3 install virtualenv

cd $PROJECT_DIR
virtualenv $VIRTUAL_ENV

info "Activating Virtual Environment"
source init_environment.sh

info "Installing Project Python Packages"
pip install docopt
pip install pyserial

if is_raspberry_pi; then
    info "Installing Raspberry Pi-Specific Packages"
    pip install RPi.GPIO

    info "Linking RF24 Modules"
    cd $VIRTUAL_ENV/lib/python3.7/site-packages
    echo "/usr/local/lib/python3.7/dist-packages/" >> dist.pth
    echo "/usr/local/lib/python3.7/dist-packages/RF24-1.3.3-py3.7-linux-armv7l.egg/" >> dist.pth
    cd $PROJECT_DIR
fi

info "Setting up Database"
$SCRIPT_DIR/re_initialize_database.py

info "Copying in Git Hooks"
hook_directory="$PROJECT_DIR/../General/Tools"
if ( is_directory "$hook_directory" ); then
    cp $hook_directory/pre-commit.pl "$PROJECT_DIR/.git/hooks/pre-commit"
fi

info "Done"
