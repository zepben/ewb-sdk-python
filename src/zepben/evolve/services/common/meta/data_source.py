#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime

from dataclassy import dataclass

__all__ = ["DataSource"]


@dataclass(slots=True)
class DataSource(object):
    source: str
    version: str
    timestamp: datetime = datetime.now()
