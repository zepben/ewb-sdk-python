#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

# TODO: this seems like a massive python antipattern, writing interface objects that are
#  essentially just setters and getters, but for consistency with the kotlin codebase, they exist.

# TODO: remove this comment before PR, as it more or less just a reminder for me to have a conversation about it

from abc import ABC, abstractmethod

class StateOperator(ABC):  # TODO: this feels kinda dirty...
    NORMAL = None
    CURRENT = None