# thread that is able to be stopped while running

import threading

class StoppableThread(threading.Thread):
    def __init__(self, target, args=(), daemon = False):
        super().__init__(daemon = daemon)
        self._active_event = threading.Event()
        self._target = target
        self._target_args = args

    def deactivate(self):
        self._active_event.clear()

    def activate(self):
        self._active_event.set()

    def activated(self):
        return self._active_event.is_set()

    def run(self):
        self._target(self, *self._target_args)