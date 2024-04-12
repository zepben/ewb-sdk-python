#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import asyncio
import unittest


class AsyncHypothesisTestCase(unittest.IsolatedAsyncioTestCase):
    """
    A base class you can use when you have async tests that need to use @given to inject hypothesis data.
    """

    @staticmethod
    def execute_example(f):
        asyncio.run(f())
