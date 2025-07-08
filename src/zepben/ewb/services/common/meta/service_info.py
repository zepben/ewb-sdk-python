#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ServiceInfo"]

from typing import TYPE_CHECKING, List

from zepben.ewb.dataclassy import dataclass
if TYPE_CHECKING:
    from zepben.ewb import DataSource


@dataclass(slots=True)
class ServiceInfo(object):
    """Container for `Service` metadata"""
    title: str
    version: str
    data_sources: List[DataSource]
