#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["AnnotatedProjectDependency"]

from typing import TYPE_CHECKING

from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.dependency_kind import DependencyKind

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_stage import NetworkModelProjectStage


@zb_dataclass
class AnnotatedProjectDependency(Identifiable):
    """
    Represents the relationship between two network model project stages.
    """

    dependency_type: DependencyKind = DependencyKind.UNKNOWN
    """Describes the dependency relationship between the two classes."""

    dependency_dependent_on_stage: NetworkModelProjectStage | None = None
    """NetworkModelProjectStage required by this stage."""

    dependency_depending_stage: NetworkModelProjectStage | None = None
    """NetworkModelProjectStages that cannot be applied alongside this stage."""

    def __init__(self, mrid: str, *_, dependency_type: DependencyKind = DependencyKind.UNKNOWN,
                 dependency_dependent_on_stage: NetworkModelProjectStage | None = None,
                 dependency_depending_stage: NetworkModelProjectStage | None = None, **kwargs):
        super(AnnotatedProjectDependency, self).__init__(mrid=mrid, dependency_type=dependency_type,
                                                         dependency_dependent_on_stage=dependency_dependent_on_stage,
                                                         dependency_depending_stage=dependency_depending_stage, **kwargs)

    def name_and_mrid(self) -> str:
        return self.mrid

    def type_name_and_mrid(self) -> str:
        return f"{self.__class__.__name__} {self.mrid}"

    def content_equals(self, other: AnnotatedProjectDependency) -> bool:
        if (self.dependency_type != other.dependency_type
                or self.dependency_depending_stage != other.dependency_depending_stage
                or self.dependency_dependent_on_stage != other.dependency_dependent_on_stage):
            return False
        return True
