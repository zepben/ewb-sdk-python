#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["VariantService"]

import datetime
from typing import Optional, Generator, Type

from zepben.ewb.services.common.base_service import BaseService
from zepben.ewb.services.common.meta.metadata_collection import MetadataCollection
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project import NetworkModelProject
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_component import NetworkModelProjectComponent
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.annotated_project_dependency import AnnotatedProjectDependency
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_stage import NetworkModelProjectStage
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification


class VariantService(BaseService):
    """
    Maintains an in-memory model of variants for the network.
    """

    supported_types = {
        NetworkModelProject, NetworkModelProjectStage, AnnotatedProjectDependency,
        ChangeSet, ObjectCreation, ObjectDeletion, ObjectModification,
    }

    def __init__(
        self,
        name: str = "variants",
        metadata: Optional[MetadataCollection] = None
    ):
        super().__init__(name, metadata)

    def get_components_between(self, start: datetime.datetime, end: datetime.datetime,
                               type_: Type[NetworkModelProjectComponent] = NetworkModelProjectComponent) -> Generator[NetworkModelProjectComponent, None, None]:
        """
        Get the components of the given type whose `created` date falls within [start, end].

        :param start: the start of the date range (inclusive).
        :param end: the end of the date range (inclusive).
        :param type_: the `NetworkModelProjectComponent` type to filter on.
        """
        for component in self.objects(type_):
            created = component.created
            if created is not None and start <= created <= end:
                yield component

    def get_projects_by_driver(self, driver: Optional[str]) -> Generator[NetworkModelProject, None, None]:
        """
        Get the `NetworkModelProject`s with the given `external_driver`.

        :param driver: the driver to filter by.
        """
        for project in self.objects(NetworkModelProject):
            if project.external_driver == driver:
                yield project
