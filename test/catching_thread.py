import threading
from typing import Optional


class CatchingThread(threading.Thread):

    def __init__(self, target=None, *args, **kwargs):
        threading.Thread.__init__(self, target=target, daemon=True, *args, **kwargs)
        self.exception: Optional[Exception] = None

    def run(self):
        try:
            threading.Thread.run(self)
        except Exception as e:
            self.exception = e
