#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import functools


def log_on_failure(func):
    """
    A decorator that will print the captured log if an exception is thrown by the function. Should be used on test functions that use caplog.

    You can set an `unmute` property to `True` on the `caplog` to enable logging of the output regardless of the test outcome. e.g. `self.caplog.unmute = True`

    :param func: The test function to decorate
    :return: The decorated test function
    """

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        caplog = self.caplog or kwargs["caplog"]
        if not caplog:
            raise ValueError("No caplog available. Please make sure you are using the caplog fixture.")

        def print_caplog():
            print()
            print("----------------------------------------")
            print()
            if caplog:
                print(caplog.text)
            else:
                print("No caplog available. Please make sure you are using the caplog fixture.")
            print("----------------------------------------")

        try:
            await func(self, *args, **kwargs)
            if getattr(caplog, 'unmute', False):
                print_caplog()
        except Exception as e:
            print_caplog()
            raise e

    return wrapper
