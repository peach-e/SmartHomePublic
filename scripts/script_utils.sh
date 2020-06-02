# ----------------------------------------------------------------- #
#  File   : script_utils.sh
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Script utilities for general use.

# Usage:
# if ( is_directory dirname ); then echo it exists; else echo nope; fi
function is_directory {
    if [ -d "$1" ]; then
        return 0
    fi
    return 1
}

function is_raspberry_pi {
    if [ ! -z "$(lsb_release -a 2>/dev/null | grep Raspbian)" ]; then
        return 0
    fi
    return 1
}

function info {
  echo "## INFO: $1"
}

function error {
    echo -n $(tput setaf 1)
    echo -n "## ERROR: $1"
    echo $(tput setaf sgr0)
}

function warn {
    echo -n $(tput setaf 3)
    echo -n "## WARN: $1"
    echo $(tput setaf sgr0)
}

info "Script Utilities sourced."
