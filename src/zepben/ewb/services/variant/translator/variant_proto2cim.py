#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["add_from_pb", "network_model_project_to_cim", "network_model_project_stage_to_cim", "annotated_project_dependency_to_cim",
           "change_set_to_cim", "object_creation_to_cim", "object_deletion_to_cim", "object_modification_to_cim", "AddFromPbResult"]

from dataclasses import dataclass
from typing import Callable, Optional

from zepben.protobuf.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.NetworkModelProject_pb2 import NetworkModelProject as PBNetworkModelProject
from zepben.protobuf.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.NetworkModelProjectComponent_pb2 import NetworkModelProjectComponent as PBNetworkModelProjectComponent
from zepben.protobuf.cim.iec61970.infiec61970.infpart303.networkmodelprojects.AnnotatedProjectDependency_pb2 import AnnotatedProjectDependency as PBAnnotatedProjectDependency
from zepben.protobuf.cim.iec61970.infiec61970.infpart303.networkmodelprojects.NetworkModelProjectStage_pb2 import NetworkModelProjectStage as PBNetworkModelProjectStage
from zepben.protobuf.cim.iec61970.infiec61970.part303.genericdataset.ChangeSet_pb2 import ChangeSet as PBChangeSet
from zepben.protobuf.cim.iec61970.infiec61970.part303.genericdataset.ChangeSetMember_pb2 import ChangeSetMember as PBChangeSetMember
from zepben.protobuf.cim.iec61970.infiec61970.part303.genericdataset.DataSet_pb2 import DataSet as PBDataSet
from zepben.protobuf.cim.iec61970.infiec61970.part303.genericdataset.ObjectCreation_pb2 import ObjectCreation as PBObjectCreation
from zepben.protobuf.cim.iec61970.infiec61970.part303.genericdataset.ObjectDeletion_pb2 import ObjectDeletion as PBObjectDeletion
from zepben.protobuf.cim.iec61970.infiec61970.part303.genericdataset.ObjectModification_pb2 import ObjectModification as PBObjectModification
from zepben.protobuf.vc.vc_data_pb2 import VariantObject

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
from zepben.ewb.services.common import resolver
from zepben.ewb.services.common.base_service import BaseService
from zepben.ewb.services.common.translator.base_proto2cim import bind_to_cim, get_nullable, identified_object_to_cim
from zepben.ewb.services.variant.translator import variant_pb_extensions  # noqa: F401  (applies the pb `mrid()` extensions)
from zepben.ewb.services.variant.variant_service import VariantService


@dataclass
class AddFromPbResult:
    """
    The result of trying to add any top level protobuf wrapper class to a service.

    NOTE: If an existing item is found in the service with the same mRID, it will be returned without merging any
    properties from the protobuf item.

    :param mrid: The mRID of the object, even if it wasn't added to the service.
    :param identifiable: The `Identifiable` reference if it was either added to the service, or `None` if there was an
        error adding it. This may be a reference to an existing object if it already existed in the service.
    :param reused_existing: `True` if the `identifiable` was found in the service, or `False` if a newly added item was created.
    """
    mrid: str
    identifiable: Optional[object]
    reused_existing: bool


def _get_or_add_from_pb(service: BaseService, mrid: str, add_from_pb: Callable[[], Optional[object]]) -> AddFromPbResult:
    existing = service.get(mrid, default=None)
    if existing is not None:
        return AddFromPbResult(mrid, existing, reused_existing=True)
    return AddFromPbResult(mrid, add_from_pb(), reused_existing=False)


def add_from_pb(pb: VariantObject, service: VariantService) -> AddFromPbResult:
    """
    Add a converted copy of the protobuf `VariantObject` to the `VariantService`.
    """
    case = pb.WhichOneof("object")
    if case == "networkModelProject":
        return _get_or_add_from_pb(service, pb.networkModelProject.mrid(), lambda: _add_from_pb_network_model_project(pb.networkModelProject, service))
    if case == "networkModelProjectStage":
        return _get_or_add_from_pb(service, pb.networkModelProjectStage.mrid(), lambda: _add_from_pb_network_model_project_stage(pb.networkModelProjectStage, service))
    if case == "annotatedProjectDependency":
        return _get_or_add_from_pb(service, pb.annotatedProjectDependency.mrid(), lambda: _add_from_pb_annotated_project_dependency(pb.annotatedProjectDependency, service))
    if case == "changeSet":
        return _get_or_add_from_pb(service, pb.changeSet.mrid(), lambda: _add_from_pb_change_set(pb.changeSet, service))
    if case == "objectCreation":
        return _get_or_add_from_pb(service, pb.objectCreation.csm.mrid(), lambda: _add_from_pb_object_creation(pb.objectCreation, service))
    if case == "objectDeletion":
        return _get_or_add_from_pb(service, pb.objectDeletion.csm.mrid(), lambda: _add_from_pb_object_deletion(pb.objectDeletion, service))
    if case == "objectModification":
        return _get_or_add_from_pb(service, pb.objectModification.csm.mrid(), lambda: _add_from_pb_object_modification(pb.objectModification, service))
    raise UnsupportedOperationException(f"Object type {case} is not supported by the variant service")


class UnsupportedOperationException(Exception):
    pass


# ###################################################################
# # Extensions IEC61970 InfIEC61970 InfPart303 NetworkModelProjects #
# ###################################################################

@bind_to_cim
def network_model_project_to_cim(pb: PBNetworkModelProject, service: VariantService) -> NetworkModelProject:
    """
    Convert the protobuf `PBNetworkModelProject` into its CIM counterpart.
    """
    cim = NetworkModelProject(mrid=pb.mrid())
    cim.external_status = get_nullable(pb, 'externalStatus')
    forecast = get_nullable(pb, 'forecastCommissionDate')
    cim.forecast_commission_date = forecast.ToDatetime() if forecast else None
    cim.external_driver = get_nullable(pb, 'externalDriver')
    for child in pb.childrenMRIDs:
        service.resolve_or_defer_reference(resolver.network_model_project_components(cim), child)
    network_model_project_component_to_cim(pb.nmpc, cim, service)
    return cim


def network_model_project_component_to_cim(pb: PBNetworkModelProjectComponent, cim: NetworkModelProjectComponent,
                                           service: VariantService) -> NetworkModelProjectComponent:
    """
    Convert the protobuf `PBNetworkModelProjectComponent` into its CIM counterpart.
    """
    created = get_nullable(pb, 'created')
    cim.created = created.ToDatetime() if created else None
    updated = get_nullable(pb, 'updated')
    cim.updated = updated.ToDatetime() if updated else None
    closed = get_nullable(pb, 'closed')
    cim.closed = closed.ToDatetime() if closed else None

    service.resolve_or_defer_reference(resolver.network_model_projects(cim), pb.parentMRID)

    identified_object_to_cim(pb.io, cim, service)
    return cim


# ########################################################
# # IEC61970 InfIEC61970 InfPart303 NetworkModelProjects #
# ########################################################

@bind_to_cim
def network_model_project_stage_to_cim(pb: PBNetworkModelProjectStage, service: VariantService) -> NetworkModelProjectStage:
    """
    Convert the protobuf `PBNetworkModelProjectStage` into its CIM counterpart.
    """
    cim = NetworkModelProjectStage(mrid=pb.mrid())
    planned = get_nullable(pb, 'plannedCommissionedDate')
    cim.planned_commissioned_date = planned.ToDatetime() if planned else None
    commissioned = get_nullable(pb, 'commissionedDate')
    cim.commissioned_date = commissioned.ToDatetime() if commissioned else None
    cim.confidence_level = get_nullable(pb, 'confidenceLevel')
    cim.base_model_version = get_nullable(pb, 'baseModelVersion')
    last_conflict = get_nullable(pb, 'lastConflictCheckedAt')
    cim.last_conflict_checked_at = last_conflict.ToDatetime() if last_conflict else None
    cim.user_comments = get_nullable(pb, 'userComments')
    change_set_mrid = get_nullable(pb, 'changeSetMRID')
    if change_set_mrid:
        service.resolve_or_defer_reference(resolver.change_set_stage(cim), change_set_mrid)

    for mrid in pb.dependingStageMRID:
        service.resolve_or_defer_reference(resolver.dependency(cim), mrid)
    # TODO: need to remove this MRID list
    for mrid in pb.dependentOnStageMRID:
        service.resolve_or_defer_reference(resolver.dependency(cim), mrid)
    for ec in pb.equipmentContainerMRIDs:
        cim.add_container(ec)

    network_model_project_component_to_cim(pb.nmpc, cim, service)
    return cim


@bind_to_cim
def annotated_project_dependency_to_cim(pb: PBAnnotatedProjectDependency, service: VariantService) -> AnnotatedProjectDependency:
    """
    Convert the protobuf `PBAnnotatedProjectDependency` into its CIM counterpart.
    """
    cim = AnnotatedProjectDependency(mrid=pb.mrid())
    cim.dependency_type = DependencyKind(pb.dependencyType)
    service.resolve_or_defer_reference(resolver.dependent_on_stage(cim), pb.dependencyDependentOnStageMRID)
    service.resolve_or_defer_reference(resolver.depending_stage(cim), pb.dependencyDependingStageMRID)
    return cim


# ###############################################
# # IEC61970 InfIEC61970 Part303 GenericDataSet #
# ###############################################

def data_set_to_cim(pb: PBDataSet, cim: DataSet) -> DataSet:
    """
    Convert the protobuf `PBDataSet` into its CIM counterpart.
    """
    cim.description = get_nullable(pb, 'description')
    cim.name = get_nullable(pb, 'name')
    return cim


@bind_to_cim
def change_set_to_cim(pb: PBChangeSet, service: VariantService) -> ChangeSet:
    """
    Convert the protobuf `PBChangeSet` into its CIM counterpart.
    """
    cim = ChangeSet(mrid=pb.mrid())
    service.resolve_or_defer_reference(resolver.stage(cim), pb.networkModelProjectStageMRID)

    for mrid in pb.changeSetMemberMRIDs:
        service.resolve_or_defer_reference(resolver.member(cim), mrid)
    data_set_to_cim(pb.dataset, cim)
    return cim


def change_set_member_to_cim(pb: PBChangeSetMember, cim: ChangeSetMember, service: VariantService) -> ChangeSetMember:
    """
    Convert the protobuf `PBChangeSetMember` into its CIM counterpart.
    """
    cim.target_object_mrid = pb.targetObjectMRID
    service.resolve_or_defer_reference(resolver.change_set_member(cim), pb.changeSetMRID, pb.mrid())
    return cim


@bind_to_cim
def object_creation_to_cim(pb: PBObjectCreation, service: VariantService) -> ObjectCreation:
    """
    Convert the protobuf `PBObjectCreation` into its CIM counterpart.
    """
    cim = ObjectCreation()
    change_set_member_to_cim(pb.csm, cim, service)
    return cim


@bind_to_cim
def object_deletion_to_cim(pb: PBObjectDeletion, service: VariantService) -> ObjectDeletion:
    """
    Convert the protobuf `PBObjectDeletion` into its CIM counterpart.
    """
    cim = ObjectDeletion()
    change_set_member_to_cim(pb.csm, cim, service)
    return cim


@bind_to_cim
def object_modification_to_cim(pb: PBObjectModification, service: VariantService) -> ObjectModification:
    """
    Convert the protobuf `PBObjectModification` into its CIM counterpart.
    """
    cim = ObjectModification()
    change_set_member_to_cim(pb.csm, cim, service)
    return cim


#
# NOTE: These `add_from_pb` extensions mirror the JVM `VariantService.addFromPb` extensions — they convert the
# protobuf object and add it to the service (returning `None` if it already existed).
#

def _add_from_pb_network_model_project(pb: PBNetworkModelProject, service: VariantService) -> Optional[NetworkModelProject]:
    cim = network_model_project_to_cim(pb, service)
    return cim if service.try_add(cim) else None


def _add_from_pb_network_model_project_stage(pb: PBNetworkModelProjectStage, service: VariantService) -> Optional[NetworkModelProjectStage]:
    cim = network_model_project_stage_to_cim(pb, service)
    return cim if service.try_add(cim) else None


def _add_from_pb_annotated_project_dependency(pb: PBAnnotatedProjectDependency, service: VariantService) -> Optional[AnnotatedProjectDependency]:
    cim = annotated_project_dependency_to_cim(pb, service)
    return cim if service.try_add(cim) else None


def _add_from_pb_change_set(pb: PBChangeSet, service: VariantService) -> Optional[ChangeSet]:
    cim = change_set_to_cim(pb, service)
    return cim if service.try_add(cim) else None


def _add_from_pb_object_creation(pb: PBObjectCreation, service: VariantService) -> Optional[ObjectCreation]:
    cim = object_creation_to_cim(pb, service)
    return cim if service.try_add(cim) else None


def _add_from_pb_object_deletion(pb: PBObjectDeletion, service: VariantService) -> Optional[ObjectDeletion]:
    cim = object_deletion_to_cim(pb, service)
    return cim if service.try_add(cim) else None


def _add_from_pb_object_modification(pb: PBObjectModification, service: VariantService) -> Optional[ObjectModification]:
    cim = object_modification_to_cim(pb, service)
    return cim if service.try_add(cim) else None
