#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

from zepben.ewb.services.common.base_service_comparator import BaseServiceComparator
from zepben.ewb.services.common.difference import ObjectDifference
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project import NetworkModelProject
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_component import NetworkModelProjectComponent
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.annotated_project_dependency import AnnotatedProjectDependency
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_stage import NetworkModelProjectStage
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set_member import ChangeSetMember
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.data_set import DataSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification


class VariantServiceComparator(BaseServiceComparator):
    """
    A class for comparing the contents of a `VariantService`.

    NOTE: Unused functions have been suppressed for this class as they are accessed by reflection rather than
    directly. This means they are always flagged as unused. By suppressing the warning it also means you might not
    be testing every function, so make sure you check the code coverage.
    """

    def _compare_network_model_project_component(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_identified_object(diff)
        self._compare_values(
            diff,
            NetworkModelProjectComponent.created,
            NetworkModelProjectComponent.updated,
            NetworkModelProjectComponent.closed,
        )
        return self._compare_id_references(diff, NetworkModelProjectComponent.parent)

    def _compare_network_model_project(self, source: NetworkModelProject, target: NetworkModelProject) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        self._compare_network_model_project_component(diff)
        self._compare_values(
            diff,
            NetworkModelProject.external_status,
            NetworkModelProject.forecast_commission_date,
            NetworkModelProject.external_driver,
        )
        return self._compare_id_reference_collections(diff, NetworkModelProject.children)

    def _compare_network_model_project_stage(self, source: NetworkModelProjectStage, target: NetworkModelProjectStage) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        self._compare_network_model_project_component(diff)
        self._compare_values(
            diff,
            NetworkModelProjectStage.planned_commissioned_date,
            NetworkModelProjectStage.commissioned_date,
            NetworkModelProjectStage.confidence_level,
            NetworkModelProjectStage.base_model_version,
            NetworkModelProjectStage.last_conflict_checked_at,
            NetworkModelProjectStage.user_comments,
        )
        self._compare_id_references(diff, NetworkModelProjectStage.change_set)
        self._compare_indexed_value_collections(diff, NetworkModelProjectStage.equipment_container_mrids)
        return self._compare_id_reference_collections(diff, NetworkModelProjectStage.dependencies)

    def _compare_annotated_project_dependencies(self, source: AnnotatedProjectDependency, target: AnnotatedProjectDependency) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        self._compare_identifiable(diff)
        self._compare_values(
            diff,
            AnnotatedProjectDependency.dependency_type,
        )
        return self._compare_id_references(
            diff,
            AnnotatedProjectDependency.dependency_dependent_on_stage,
            AnnotatedProjectDependency.dependency_depending_stage,
        )

    def _compare_data_set(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_identifiable(diff)
        return self._compare_values(diff, DataSet.name, DataSet.description)

    def _compare_change_sets(self, source: ChangeSet, target: ChangeSet) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        self._compare_data_set(diff)
        self._compare_id_reference_collections(diff, ChangeSet.members)
        return self._compare_id_references(diff, ChangeSet.network_model_project_stage)

    def _compare_change_set_member(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_identifiable(diff)
        self._compare_values(diff, ChangeSetMember.target_object_mrid)
        return self._compare_id_references(diff, ChangeSetMember.change_set)

    def _compare_object_creation(self, source: ObjectCreation, target: ObjectCreation) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        return self._compare_change_set_member(diff)

    def _compare_object_deletion(self, source: ObjectDeletion, target: ObjectDeletion) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        return self._compare_change_set_member(diff)

    def _compare_object_modification(self, source: ObjectModification, target: ObjectModification) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        return self._compare_change_set_member(diff)
