# thread that is able to be stopped while running

import threading

class StoppableThread(threading.Thread):
    def __init__(self, target, args=(), daemon = False):
        super().__init__(daemon = daemon)
        self._stop_event = threading.Event()
        self._target = target
        self._target_args = args

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self._target(self, *self._target_args)