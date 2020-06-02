#!/usr/bin/env bash
# ----------------------------------------------------------------- #
#  File   : init_environment.sh
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Initializes the environment to run the application.

# Get project location
INIT_DIR=$(pwd)
PROJECT_DIR=$(cd $(dirname $BASH_SOURCE) && pwd)
export APP_ROOT=$PROJECT_DIR

# Turn on the virtual environment
cd $APP_ROOT/virtualenv/bin
source activate

# Add the Python Path
export PYTHONPATH=$PYTHONPATH:$APP_ROOT/lib

# Restore Init working dir
cd $INIT_DIR