#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["NetworkModelProjectStage"]

import datetime
from typing import TYPE_CHECKING, Generator

from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_component import NetworkModelProjectComponent
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.annotated_project_dependency import AnnotatedProjectDependency
from zepben.ewb.util import get_by_mrid, ngen, nlen

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet


@zbex
@zb_dataclass
class NetworkModelProjectStage(NetworkModelProjectComponent):
    """
    A specific phase in a network model project.
    """

    planned_commissioned_date: datetime.datetime | None = None
    """The date expected for this stage to be commissioned."""

    commissioned_date: datetime.datetime | None = None
    """The date this stage was commissioned."""

    confidence_level: int | None = None
    """[ZBEX] The percentage confidence that this project will be committed to."""

    base_model_version: str | None = None
    """[ZBEX] The version of the base model this stage was imported against."""

    last_conflict_checked_at: datetime.datetime | None = None
    """[ZBEX] The time the last conflict check occurred."""

    user_comments: str | None = None
    """[ZBEX] User comments."""

    change_set: ChangeSet | None = None
    """[ZBEX] The set of changes that this stage of the project will do."""

    _dependencies: list[AnnotatedProjectDependency] | None = None
    _equipment_container_mrids: list[str] | None = None

    @property
    def dependencies(self) -> Generator[AnnotatedProjectDependency, None, None]:
        """The stages that depend on this stage."""
        return ngen(self._dependencies)

    @property
    def equipment_container_mrids(self) -> Generator[str, None, None]:
        """[ZBEX] The equipment containers this stage is related to."""
        return ngen(self._equipment_container_mrids)

    def num_dependent_on_stages(self) -> int:
        """Get the number of stages that are dependent on this stage."""
        return len([d for d in (self._dependencies or []) if d.dependency_dependent_on_stage is not self])

    def num_depending_stages(self) -> int:
        """Get the number of stages that are depending on this stage."""
        return len([d for d in (self._dependencies or []) if d.dependency_depending_stage is not self])

    def get_dependency(self, mrid: str) -> AnnotatedProjectDependency | None:
        """
        Get a dependent `AnnotatedProjectDependency` for this stage.

        :param mrid: the mRID of the required `AnnotatedProjectDependency`.
        :return: The `AnnotatedProjectDependency` with the specified `mrid` if it exists, otherwise None.
        :raises KeyError: if no dependency with the given `mrid` exists.
        """
        return get_by_mrid(self._dependencies, mrid)

    def add_dependency(self, dependency: AnnotatedProjectDependency) -> NetworkModelProjectStage:
        """
        Create an `AnnotatedProjectDependency` where this stage depends on the other stage in `dependency`.

        eg:
          to apply the `ChangeSet`s in the other stage we do not resolve the dependency.
          to apply the `ChangeSet`s in this stage we MUST resolve the dependency.

        :param dependency: the `AnnotatedProjectDependency` that depends on this stage.
        :return: A reference to this `NetworkModelProjectStage` to allow fluent use.
        """
        if self._validate_reference(dependency, self.get_dependency, "An AnnotatedProjectDependency"):
            return self

        if self._dependencies is None:
            self._dependencies = []
        self._dependencies.append(dependency)

        return self

    def remove_dependency(self, dependency: AnnotatedProjectDependency) -> bool:
        """
        :param dependency: the `AnnotatedProjectDependency` to remove its dependency on this stage.
        :return: true if `dependency` was removed as a dependency from this stage.
        """
        if self._dependencies is None:
            return False
        try:
            self._dependencies.remove(dependency)
        except ValueError:
            return False
        if not self._dependencies:
            self._dependencies = None
        return True

    def clear_dependencies(self) -> NetworkModelProjectStage:
        """
        Clear this `NetworkModelProjectStage`'s `dependencies` collection.

        :return: this `NetworkModelProjectStage`
        """
        self._dependencies = None
        return self

    def num_containers(self) -> int:
        """Get the number of entries in the `equipment_container_mrids` collection."""
        return nlen(self._equipment_container_mrids)

    def contains(self, mrid: str) -> bool:
        return mrid in (self._equipment_container_mrids or [])

    def add_container(self, equipment_container_mrid: str) -> NetworkModelProjectStage:
        """
        Associate an `EquipmentContainer` with this `NetworkModelProjectStage` by its mRID.

        :param equipment_container_mrid: The `EquipmentContainer` mRID to associate.
        :return: this `NetworkModelProjectStage` for fluent use.
        """
        if self._equipment_container_mrids is None:
            self._equipment_container_mrids = []
        self._equipment_container_mrids.append(equipment_container_mrid)

        return self

    def _get_container(self, mrid: str) -> str | None:
        """Helper method to make use of existing tests."""
        return mrid if mrid in (self._equipment_container_mrids or []) else None

    def remove_container(self, equipment_container_mrid: str) -> bool:
        """
        :param equipment_container_mrid: the equipment container to disassociate with this equipment.
        :return: `true` if `equipment_container_mrid` has been successfully removed; `false` if it was not present in the set.
        """
        if self._equipment_container_mrids is None:
            return False
        try:
            self._equipment_container_mrids.remove(equipment_container_mrid)
        except ValueError:
            return False
        if not self._equipment_container_mrids:
            self._equipment_container_mrids = None
        return True

    def clear_containers(self) -> NetworkModelProjectStage:
        """
        Clear this `NetworkModelProjectStage`'s associated `EquipmentContainer`s.

        :return: this `NetworkModelProjectStage`
        """
        self._equipment_container_mrids = None
        return self
