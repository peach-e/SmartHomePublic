# ----------------------------------------------------------------- #
#  File   : worker.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.constants
import tsl.services
import tsl.util.log

import time
from threading import Thread


class Worker (Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self._stop_requested = False

    def run(self):
        tsl.util.log.info("{} - Worker Started".format(time.asctime()))

        # Apply what should be immediate.
        tsl.services.apply_por_states()

        # Every so so, enforce the system.
        try:
            while not self._stop_requested:
                time.sleep(tsl.constants.WORKER_POLL_INTERVAL)
                tsl.services.enforce_peripheral_schedules()
        except KeyboardInterrupt:
            pass

        tsl.util.log.info("{} - Worker Stopped".format(time.asctime()))

    def stop(self):
        self._stop_requested = True
