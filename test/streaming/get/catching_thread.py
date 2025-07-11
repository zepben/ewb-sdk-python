#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import threading
import traceback
from typing import Optional


class CatchingThread(threading.Thread):

    def __init__(self, target=None, *args, **kwargs):
        threading.Thread.__init__(self, target=target, daemon=True, *args, **kwargs)
        self.exception: Optional[Exception] = None

    def run(self):
        try:
            threading.Thread.run(self)
        except Exception as e:
            # We need to log the exception as the pytest logging only gives the outcome of errors
            # in the client test if they also fail, not which line actually caused it.
            print(traceback.format_exc())
            self.exception = e
