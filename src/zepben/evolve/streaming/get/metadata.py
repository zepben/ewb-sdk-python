#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from dataclassy import dataclass
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from zepben.evolve import DataSource

__all__ = ["MetaData"]


@dataclass(slots=True)
class MetaData(object):
    """Container for `NetworkService` metadata"""
    title: str
    version: str
    data_sources: Dict[str, DataSource]  # y u no list?
