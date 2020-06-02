# ----------------------------------------------------------------- #
#  File   : exception.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #


class ConfigurationError(Exception):
    # When your environment isn't set up right.

    def __init__(self, detail_msg):
        message = "Configuration not Valid: {}.".format(detail_msg)
        Exception.__init__(self, message)


class DataError(Exception):
    # For when data is invalid.

    def __init__(self, detail_msg):
        message = "Invalid Data: {}.".format(detail_msg)
        Exception.__init__(self, message)


class DatabaseError(Exception):

    def __init__(self, detail_msg):
        message = "Database Error: {}".format(detail_msg)
        Exception.__init__(self, message)


class FileError(Exception):
    # When a file is not valid.

    def __init__(self, dir_name):
        message = "File '{}' not found.".format(dir_name)
        Exception.__init__(self, message)


class EnvironmentVariableError(Exception):
    # For when something invalid with environment variable.

    def __init__(self, variable_name):
        message = "Environment Varaible '{}' invalid or not defined.".format(
            variable_name)
        Exception.__init__(self, message)


class NotImplementedError(Exception):
    # For when something hasn't been implemented yet.

    def __init__(self):
        message = "Function or capability not implemented."
        Exception.__init__(self, message)


class PathError(Exception):
    # When a directory is not valid.

    def __init__(self, dir_name):
        message = "Path '{}' not valid.".format(dir_name)
        Exception.__init__(self, message)


class TypeError(Exception):

    def __init__(self, got_type, expected_type):
        message = "Got '{}', expected '{}'.".format(got_type, expected_type)
        Exception.__init__(self, message)
