#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from zepben.evolve.dataclassy import dataclass
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from zepben.evolve import DataSource

__all__ = ["ServiceInfo"]


@dataclass(slots=True)
class ServiceInfo(object):
    """Container for `Service` metadata"""
    title: str
    version: str
    data_sources: List[DataSource]
