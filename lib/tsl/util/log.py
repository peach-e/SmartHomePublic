# ----------------------------------------------------------------- #
#  File   : log.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# Used for logging and writing to log files.
# Anything that's worse than an error, just raise an exception.

import tsl.util.path
import re
import traceback

COLORED_LOGGING_ENABLED = True


def _FORMAT_RED(x): return '\033[91m' + str(x) + '\033[39m'


def _FORMAT_YELLOW(x): return '\033[93m' + str(x) + '\033[39m'


_LOG_HEADER_INFO = "INFO"
_LOG_HEADER_WARN = "WARN"
_LOG_HEADER_ERROR = "ERROR"

_MESSAGE_TEMPLATE = "{} [{}:{}]:  {}"
_STACK_NUMBER_OFFSET = -3
_STACK_FILENAME_LINE_REGEX = 'File \"(.*?)\", line ([\d]+)'


def __get_calling_location():
    tb = traceback.format_stack()
    filepath, line = re.search(
        _STACK_FILENAME_LINE_REGEX,
        tb[_STACK_NUMBER_OFFSET]
    ).groups()
    filename = tsl.util.path.get_filename_from_path(filepath)
    return filename, line


def _print(message):
    print(message, flush=True)


def info(message):
    filename, line = __get_calling_location()
    full_message = _MESSAGE_TEMPLATE.format(
        _LOG_HEADER_INFO, filename, line, message)
    _print(full_message)


def warn(message):
    filename, line = __get_calling_location()
    full_message = _MESSAGE_TEMPLATE.format(
        _LOG_HEADER_WARN, filename, line, message)
    if COLORED_LOGGING_ENABLED:
        _print(_FORMAT_YELLOW(full_message))
    else:
        _print(full_message)


def error(message):
    filename, line = __get_calling_location()
    full_message = _MESSAGE_TEMPLATE.format(
        _LOG_HEADER_ERROR, filename, line, message)
    if COLORED_LOGGING_ENABLED:
        _print(_FORMAT_RED(full_message))
    else:
        _print(full_message)
