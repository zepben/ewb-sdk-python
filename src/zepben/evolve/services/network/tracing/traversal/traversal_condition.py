#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABC
from typing import TypeVar, Generic

T = TypeVar('T')

class TraversalCondition(ABC, Generic[T]):
    def __init__(self, _func):
        self._func = _func