#!/usr/bin/env python
# ----------------------------------------------------------------- #
#  File   : run_server.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.app
import tsl.constants
import tsl.server
import tsl.worker
import tsl.util.env


def run():
    worker = tsl.worker.Worker()
    server = tsl.server.Server(tsl.constants.SERVER_HOSTNAME, tsl.constants.SERVER_PORT)

    worker.start()  # Worker is a daemon thread so start it first.
    server.start()

if __name__ == "__main__":
    doc_string = """

Smarthome Server

Usage:
  run_server.py
  run_server.py (-h | --help)

Options:
  -h --help     Show this screen.
  """

    tsl.util.env.get_command_line_args(doc_string)
    tsl.app.initialize()
    run()
    tsl.app.clean_up()
