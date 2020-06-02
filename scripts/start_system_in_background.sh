#!/usr/bin/env bash
# ----------------------------------------------------------------- #
#  File   : start_system_in_background.sh
#  Author : peach
#  Date   : 11 November 2019
# ----------------------------------------------------------------- #

# This script is intended to be run by root as a single point of entry
# for firing up the system in production.

# This script should be called by the root user on system startup.

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
PROJECT_DIR=$(cd $SCRIPT_DIR/.. && pwd)

source "$SCRIPT_DIR/script_utils.sh"

if ! is_raspberry_pi; then
   error "This script is for Raspberry Pi only."
   exit 1
fi

if [ $(whoami) != 'root' ]; then
  error "This script must be run as root."
  exit 1
fi

cd $PROJECT_DIR

source ./init_environment.sh
nohup ./app/run_system.py >> system.log 2>&1 &
