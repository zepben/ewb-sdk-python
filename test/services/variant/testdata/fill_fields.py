#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Ported from `com.zepben.ewb.services.variant.testdata.FillFields.kt`.
#
# The JVM declares these as `fillFields` extension functions on each CIM class. In Python they become
# module-level functions taking the object as the first argument, named `<receiver>_fill_fields` so the
# overloads (all named `fillFields` on the JVM) don't collide.

from __future__ import annotations

import datetime

from zepben.ewb import generate_id
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.annotated_project_dependency import AnnotatedProjectDependency
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.dependency_kind import DependencyKind
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_stage import NetworkModelProjectStage
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set_member import ChangeSetMember
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.data_set import DataSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project import NetworkModelProject
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_component import NetworkModelProjectComponent
from zepben.ewb.services.common.base_service import BaseService


def _now() -> datetime.datetime:
    # NOTE: The protobuf `ToDatetime()` extension returns a *naive* datetime, so these fillers must
    # populate naive datetimes for the translator round-trip to compare equal (matching the convention in
    # `test/cim/fill_fields.py`, which uses naive `hypothesis.datetimes()`).
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


def fill_fields_common(obj: IdentifiedObject, service: BaseService, include_runtime: bool = True) -> IdentifiedObject:
    """
    Mirrors the JVM `IdentifiedObject.fillFieldsCommon` (from `services.common.testdata`).

    NOTE: The JVM also sets `numDiagramObjects = 2`, but the Python `IdentifiedObject` does not carry that
    field, so it is skipped here.
    """
    obj.name = "1"
    obj.description = "the description"

    for i in range(0, 2):
        try:
            name_type = service.get_name_type(f"name_type {i}")
        except KeyError:
            name_type = NameType(f"name_type {i}")
            name_type.description = f"name_type_{i}_description"
            service.add_name_type(name_type)
        obj.add_name(name_type, f"name_{i}")

    return obj


# #######################################################
# # Extensions IEC61970 InfPart303 NetworkModelProjects #
# #######################################################

def network_model_project_fill_fields(project: NetworkModelProject, service: BaseService, include_runtime: bool = True) -> NetworkModelProject:
    network_model_project_component_fill_fields(project, service, include_runtime)
    project.external_status = "Probably Fine"
    project.forecast_commission_date = _now() + datetime.timedelta(seconds=600)
    project.external_driver = "Capacity"

    if include_runtime:
        for i in range(0, 2):
            child = NetworkModelProjectStage(f"{project.mrid}-child-{i}")
            service.add(child)
            project.add_child(child)

    return project


def network_model_project_component_fill_fields(component: NetworkModelProjectComponent, service: BaseService, include_runtime: bool = True) -> NetworkModelProjectComponent:
    fill_fields_common(component, service, include_runtime)

    component.created = _now() - datetime.timedelta(seconds=10)
    component.closed = _now()

    parent = NetworkModelProject("parent-project")
    parent.add_child(component)
    service.add(parent)
    component.parent = parent

    # TODO
    return component


# ############################################
# # IEC61970 InfPart303 NetworkModelProjects #
# ############################################

def annotated_project_dependency_fill_fields(dependency: AnnotatedProjectDependency, service: BaseService, include_runtime: bool = True) -> AnnotatedProjectDependency:
    # `AnnotatedProjectDependency` is a plain `Identifiable` (not an `IdentifiedObject`), so the JVM
    # `Identifiable.fillFieldsCommon` no-op applies here.
    dependency.dependency_type = DependencyKind.mutuallyExclusive
    dependency.dependency_dependent_on_stage = NetworkModelProjectStage(generate_id())
    service.add(dependency.dependency_dependent_on_stage)
    dependency.dependency_depending_stage = NetworkModelProjectStage(generate_id())
    service.add(dependency.dependency_depending_stage)

    return dependency


def network_model_project_stage_fill_fields(stage: NetworkModelProjectStage, service: BaseService, include_runtime: bool = True) -> NetworkModelProjectStage:
    network_model_project_component_fill_fields(stage, service, include_runtime)
    stage.planned_commissioned_date = _now() + datetime.timedelta(seconds=3200)
    stage.confidence_level = 10
    stage.base_model_version = "2025-10-12"
    stage.last_conflict_checked_at = _now() - datetime.timedelta(seconds=20000)
    stage.user_comments = "Dodgy network, probably dont use this in production..."
    change_set = ChangeSet(generate_id())
    service.add(change_set)
    change_set.network_model_project_stage = stage
    stage.change_set = change_set

    depending_stage = NetworkModelProjectStage(generate_id())
    service.add(depending_stage)
    dependent_stage = NetworkModelProjectStage(generate_id())
    service.add(dependent_stage)
    stage.add_dependency(AnnotatedProjectDependency(
        generate_id(),
        dependency_depending_stage=stage,
        dependency_dependent_on_stage=dependent_stage,
    ))
    stage.add_dependency(AnnotatedProjectDependency(
        generate_id(),
        dependency_dependent_on_stage=stage,
        dependency_depending_stage=depending_stage,
    ))

    stage.add_container(generate_id())

    return stage


# ###################################
# # IEC61970 Part303 GenericDataSet #
# ###################################

def change_set_fill_fields(change_set: ChangeSet, service: BaseService, include_runtime: bool = True) -> ChangeSet:
    data_set_fill_fields(change_set, service, include_runtime)

    stage = NetworkModelProjectStage(generate_id())
    stage.change_set = change_set
    service.add(stage)
    change_set.network_model_project_stage = stage

    creation = ObjectCreation()
    creation.change_set = change_set
    creation.target_object_mrid = "creation"
    service.add(creation)
    change_set.add_member(creation)

    return change_set


def data_set_fill_fields(data_set: DataSet, service: BaseService, include_runtime: bool = True) -> DataSet:
    data_set.name = "1"
    data_set.description = "the description"

    return data_set


def change_set_member_fill_fields(member: ChangeSetMember, service: BaseService, include_runtime: bool) -> ChangeSetMember:
    # `ChangeSetMember` is a plain `Identifiable`, so the JVM `Identifiable.fillFieldsCommon` no-op applies here.
    cs = ChangeSet(generate_id())
    service.add(cs)
    member.change_set = cs
    cs.add_member(member)
    member.target_object_mrid = generate_id()

    return member


def object_creation_fill_fields(creation: ObjectCreation, service: BaseService, include_runtime: bool = True) -> ObjectCreation:
    return change_set_member_fill_fields(creation, service, include_runtime)


def object_deletion_fill_fields(deletion: ObjectDeletion, service: BaseService, include_runtime: bool = True) -> ObjectDeletion:
    return change_set_member_fill_fields(deletion, service, include_runtime)


def object_modification_fill_fields(modification: ObjectModification, service: BaseService, include_runtime: bool = True) -> ObjectModification:
    return change_set_member_fill_fields(modification, service, include_runtime)
