# ----------------------------------------------------------------- #
#  File   : app.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

# For initializing and cleaning up python scripts.
import tsl.util.log

INITIAL_WORKING_DIRECTORY = None


def _setup_logging():
    # Some day, this can include things like writing to log files.
    tsl.util.log.COLORED_LOGGING_ENABLED = True


def initialize():
    global INITIAL_WORKING_DIRECTORY

    # Capture initial directory.
    if INITIAL_WORKING_DIRECTORY is None:
        INITIAL_WORKING_DIRECTORY = tsl.util.path.get_cwd()

    # Get logging and external tools ready to go.
    _setup_logging()
    tsl.util.log.info('App Infrastructure Initialized.')


def clean_up():
    global INITIAL_WORKING_DIRECTORY

    # Restore initial directory.
    if INITIAL_WORKING_DIRECTORY is not None:
        tsl.util.path.cd(INITIAL_WORKING_DIRECTORY)
        tsl.util.log.info('Restoring Initial Directory.')
        INITIAL_WORKING_DIRECTORY = None
