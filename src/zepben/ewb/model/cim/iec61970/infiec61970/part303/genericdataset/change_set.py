#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["ChangeSet"]

from typing import TYPE_CHECKING, Any, Generator

from zepben.ewb import require, nlen, ngen
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.data_set import DataSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set_member import ChangeSetMember
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_stage import NetworkModelProjectStage


@zb_dataclass
class ChangeSet(DataSet):
    """
    Describes a set of changes that can be applied in different situations. A given registered
    target object MRID may only be referenced once by the contained change set members.
    """

    _members: list[ChangeSetMember] | None = None
    network_model_project_stage: NetworkModelProjectStage | None = None
    """NetworkModelProjectStage this ChangeSet belongs to."""

    def __init__(self, mrid: str, *_, members: list[ChangeSetMember] | None = None, **kwargs):
        super(ChangeSet, self).__init__(mrid=mrid, **kwargs)
        if members:
            for member in members:
                self.add_member(member)

    @property
    def members(self) -> list[ChangeSetMember]:
        """Data objects contained in the dataset."""
        return ngen(self._members)

    @property
    def creations(self) -> Generator[ObjectCreation, Any, None]:
        return (m for m in (self._members or []) if isinstance(m, ObjectCreation))

    @property
    def deletions(self) -> Generator[ObjectDeletion, Any, None]:
        return (m for m in (self._members or []) if isinstance(m, ObjectDeletion))

    @property
    def modifications(self) -> Generator[ObjectModification, Any, None]:
        return (m for m in (self._members or []) if isinstance(m, ObjectModification))

    def num_members(self) -> int:
        """Get the number of entries in the `ChangeSetMember` collection."""
        return nlen(self._members)

    def get_member(self, mrid: str) -> ChangeSetMember | None:
        """
        Retrieve the `ChangeSetMember` for the specified `mrid`.

        :param mrid: the `ChangeSetMember.target_object_mrid` to retrieve.
        :return: The `ChangeSetMember` with the specified `target_object_mrid` if it exists, otherwise None.
        """
        for member in self.members:
            if member.target_object_mrid == mrid:
                return member
        return None

    def add_member(self, member: ChangeSetMember) -> ChangeSet:
        """
        Add a `ChangeSetMember` to this `ChangeSet`.
        A `ChangeSetMember.target_object_mrid` may only be referenced by one member in this `ChangeSet`.

        :param member: The `ChangeSetMember` to add.
        :return: this `ChangeSet` for fluent use.
        """
        require(member.change_set is self,
                lambda: f"{type(member).__name__} `change_set` property references {member.change_set.type_name_and_mrid() if member.change_set else None}, expected {self.type_name_and_mrid()}.")
        require(all(m.target_object_mrid != member.target_object_mrid for m in (self._members or [])),
                lambda: f"A ChangeSetMember already exists in {self.type_name_and_mrid()} with target_object_mrid {member.target_object_mrid}.")

        if self._members is None:
            self._members = []
        self._members.append(member)

        return self

    def remove_member(self, member: ChangeSetMember) -> bool:
        """
        Remove a `ChangeSetMember` from this `ChangeSet`.

        :param member: the `ChangeSetMember` to disconnect from this `ChangeSet`.
        :return: true if `member` was removed from this `ChangeSet`.
        """
        if self._members is None:
            return False
        try:
            self._members.remove(member)
        except ValueError:
            return False
        if not self._members:
            self._members = None
        return True
