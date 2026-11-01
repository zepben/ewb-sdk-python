#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["ChangeSetMember"]

from abc import ABCMeta
from typing import TYPE_CHECKING, Optional

from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet


class ChangeSetMember(Identifiable, metaclass=ABCMeta):
    """
    A CRUD-style data object.

    `change_set` and `target_object_mrid` must be set prior to use.
    """

    __slots__ = ("change_set", "target_object_mrid")

    change_set: ChangeSet | None
    """The `ChangeSet` this `ChangeSetMember` belongs to."""

    target_object_mrid: str | None
    """The CIM object `change_set` applies to."""

    def __init__(self):
        # mrid is computed from change_set + target_object_mrid, so it is not stored.
        # This is a plain class (mirroring the JVM `lateinit` fields), so we set the
        # slots directly rather than running the dataclass base init.
        self.change_set = None
        self.target_object_mrid = None

    @property
    def mrid(self) -> str:
        return f"{self.change_set.mrid}_{self.target_object_mrid}"

    def name_and_mrid(self) -> str:
        return self.mrid

    def type_name_and_mrid(self) -> str:
        return f"{self.__class__.__name__} {self.mrid}"
