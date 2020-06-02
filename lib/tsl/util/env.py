# ----------------------------------------------------------------- #
#  File   : env.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #
# For environment related operations.
import tsl.util.exception
import tsl.util.path

from docopt import docopt
import importlib.util
import sys
import os


def get_command_line_args(doc_string):
    # Wrapper for the docopt library
    return docopt(doc_string)


def get_environment():
    # Return a copy of our whole environment.
    return os.environ.copy()


def get_environment_variable(key, assert_exists=True):
    # Return the value of an environment variable if it exists.
    value = os.getenv(str(key))
    if assert_exists and (value == None):
        raise tsl.util.exception.EnvironmentVariableError(key)
    return value


def get_os_platform():
    # This CAN be used to identify the operating system. However,
    # only tsl.os should be using it.
    return sys.platform.lower()


def get_prefix():
    # Return the prefix of our current python binary.
    return sys.prefix


def get_python_version():
    ver = sys.version_info
    return (ver.major, ver.minor, ver.micro)


def import_module_from_file(module_path):
    # When a file is not on the python path, this will load the
    # file and make it available through module_name.
    #
    #
    # Example: for file test.py with contents:
    #  1 | print('importing a test.py module')
    #  2 | x = 555
    #  3 | def test():
    #  4 |     print('hello')
    #
    # Then you would run
    # >>> MyModule = import_module_from_file('test.py')
    # >>> MyModule.x
    #        555
    # >>> MyModule.test()
    #        hello
    #
    # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    tsl.util.path.assert_file_exists(module_path)
    spec = importlib.util.spec_from_file_location(
        "imported_module", module_path)
    module_handle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module_handle)
    return module_handle


def is_virtual_environment():
    return hasattr(sys, 'real_prefix')


def set_environment_variable(key, value):
    key = str(key)
    value = str(value)
    os.environ[key] = value


def umask(new_umask):
    # Set the umask of the current shell. Note that new_umask
    # must be specified in decimal, not octal, so to get the
    # behavior of `$ umask 022` you need to call umask(18).
    os.umask(new_umask)
