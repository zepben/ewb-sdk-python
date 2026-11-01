#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["DataSet"]

from abc import ABCMeta
from typing import Optional

from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable


@zb_dataclass
class DataSet(Identifiable, metaclass=ABCMeta):
    """
    A generic container of a version of instance data. The mRID can be used in an audit trail, not
    in reusable script intended to work with new versions of data. A dataset could be serialized
    multiple times and in multiple technologies, yet retain the same identity.
    """

    name: Optional[str] = None
    """is any free human-readable and possibly non-unique text naming the object."""

    description: Optional[str] = None
    """a free human-readable text describing or naming the object. It may be non-unique and may not correlate to a naming hierarchy."""
