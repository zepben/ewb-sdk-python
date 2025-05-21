#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABC


class StateOperator(ABC):
    NORMAL = None
    CURRENT = None

    def __init__(self):
        raise TypeError('Any class subclassing (StateOperators) should not be instantiated or have state.')
