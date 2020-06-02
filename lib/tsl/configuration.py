# ----------------------------------------------------------------- #
#  File   : configuration.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.constants
import tsl.util.env
import tsl.util.path
import tsl.util.log

import re
import sys

_APP_ROOT = tsl.util.env.get_environment_variable('APP_ROOT')
_CONFIG_FILE_LOCATION = tsl.util.path.join_paths(
    _APP_ROOT,
    tsl.constants.CONFIG_FILE_LOCATION)

CFG = {}

# ------------------------------------------------
#    Private Methods
# ------------------------------------------------


def _ensure_config_file_exists():
    # Make sure the conf file is there. If it isn't, we create
    # one from the sample file or otherwise alert a warning.
    template_file = _CONFIG_FILE_LOCATION + ".template"
    if tsl.util.path.exists_file(_CONFIG_FILE_LOCATION):
        return True
    elif tsl.util.path.exists_file(template_file):
        tsl.util.path.copy(template_file, _CONFIG_FILE_LOCATION)
        tsl.util.log.info('Copying config file from template.')
        return True
    else:
        tsl.util.log.error(
            'Unable to read config File. Configuration not initialized.')
        return False


def _parseIntegerOrFloat(val):
    # Converts a found value into either an int or float or leave it as a
    # string.
    try:
        refinedType = int(val)
    except:
        try:
            refinedType = float(val)
        except:
            refinedType = val
    return refinedType


def _initialize():
    global CFG

    if not _ensure_config_file_exists():
        return

    # Check to see if the conf file is there. If it isn't, try and copy over
    # the template conf file.
    tsl.util.log.info(
        "Loading configuration from {}.".format(_CONFIG_FILE_LOCATION))

    settingsDict = {}

    f = open(_CONFIG_FILE_LOCATION, 'r')
    # Search for something like
    #      abc =  fasjfkl
    # and
    pattern1 = re.compile('^\s*(\S+)\s*=\s*(.+)\s*$')
    pattern2 = re.compile('#')
    for line in f:
        # Ignore comments in conf file.
        if (pattern2.search(line)):
            continue
        searchResult = pattern1.match(line)
        if not (searchResult):
            continue
        key = searchResult.group(1)
        val = searchResult.group(2)

        settingsDict[key] = _parseIntegerOrFloat(val)
    f.close()

    CFG = settingsDict

    return

# ------------------------------------------------
#    Public Methods
# ------------------------------------------------


def val(key):
    # Try to get the number version of the value
    if exists(key):
        return CFG[key]
    else:
        return None


def exists(key):
    return key in CFG.keys()


_initialize()
