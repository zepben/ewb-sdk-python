#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["variant_object_to_pb", "network_model_project_to_pb", "network_model_project_stage_to_pb", "annotated_project_dependency_to_pb",
           "change_set_to_pb", "object_creation_to_pb", "object_deletion_to_pb", "object_modification_to_pb"]

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

from zepben.ewb import datetime_to_timestamp
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.annotated_project_dependency import AnnotatedProjectDependency
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_stage import NetworkModelProjectStage
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set_member import ChangeSetMember
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.data_set import DataSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project import NetworkModelProject
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_component import NetworkModelProjectComponent
from zepben.ewb.services.common.translator.base_cim2proto import bind_to_pb, identified_object_to_pb, set_or_null
from zepben.ewb.services.variant.translator.variant_enum_mappers import _map_dependency_kind
from zepben.ewb.services.variant.variant_service_utils import when_variant_identified_object


def variant_object_to_pb(identified: Identifiable) -> VariantObject:
    """
    Convert the `identified` object to a `VariantObject` representation.
    """
    return when_variant_identified_object(
        identified,
        is_network_model_project=lambda it: VariantObject(networkModelProject=network_model_project_to_pb(it)),
        is_network_model_project_stage=lambda it: VariantObject(networkModelProjectStage=network_model_project_stage_to_pb(it)),
        is_annotated_project_dependency=lambda it: VariantObject(annotatedProjectDependency=annotated_project_dependency_to_pb(it)),
        is_change_set=lambda it: VariantObject(changeSet=change_set_to_pb(it)),
        is_object_creation=lambda it: VariantObject(objectCreation=object_creation_to_pb(it)),
        is_object_deletion=lambda it: VariantObject(objectDeletion=object_deletion_to_pb(it)),
        is_object_modification=lambda it: VariantObject(objectModification=object_modification_to_pb(it)),
    )


# ###################################################################
# # Extensions IEC61970 InfIEC61970 InfPart303 NetworkModelProjects #
# ###################################################################

@bind_to_pb
def network_model_project_to_pb(cim: NetworkModelProject) -> PBNetworkModelProject:
    """
    Convert the `NetworkModelProject` into its protobuf counterpart.
    """
    return PBNetworkModelProject(
        nmpc=network_model_project_component_to_pb(cim),
        childrenMRIDs=[str(child.mrid) for child in cim.children],
        **set_or_null(
            externalStatus=cim.external_status,
            forecastCommissionDate=datetime_to_timestamp(cim.forecast_commission_date),
            externalDriver=cim.external_driver
        )
    )


def network_model_project_component_to_pb(cim: NetworkModelProjectComponent) -> PBNetworkModelProjectComponent:
    """
    Convert the `NetworkModelProjectComponent` into its protobuf counterpart.
    """
    return PBNetworkModelProjectComponent(
        io=identified_object_to_pb(cim),
        parentMRID=str(cim.parent.mrid) if cim.parent else "",
        **set_or_null(
            created=datetime_to_timestamp(cim.created),
            updated=datetime_to_timestamp(cim.updated),
            closed=datetime_to_timestamp(cim.closed)
        )
    )


# ########################################################
# # IEC61970 InfIEC61970 InfPart303 NetworkModelProjects #
# ########################################################

@bind_to_pb
def annotated_project_dependency_to_pb(cim: AnnotatedProjectDependency) -> PBAnnotatedProjectDependency:
    """
    Convert the `AnnotatedProjectDependency` into its protobuf counterpart.
    """
    return PBAnnotatedProjectDependency(
        mRID=str(cim.mrid),
        dependencyType=_map_dependency_kind.to_pb(cim.dependency_type),
        dependencyDependingStageMRID=str(cim.dependency_depending_stage.mrid) if cim.dependency_depending_stage else "",
        dependencyDependentOnStageMRID=str(cim.dependency_dependent_on_stage.mrid) if cim.dependency_dependent_on_stage else ""
    )


@bind_to_pb
def network_model_project_stage_to_pb(cim: NetworkModelProjectStage) -> PBNetworkModelProjectStage:
    """
    Convert the `NetworkModelProjectStage` into its protobuf counterpart.
    """
    return PBNetworkModelProjectStage(
        nmpc=network_model_project_component_to_pb(cim),
        **set_or_null(
            plannedCommissionedDate=datetime_to_timestamp(cim.planned_commissioned_date),
            commissionedDate=datetime_to_timestamp(cim.commissioned_date),
            confidenceLevel=cim.confidence_level,
            baseModelVersion=cim.base_model_version,
            lastConflictCheckedAt=datetime_to_timestamp(cim.last_conflict_checked_at),
            userComments=cim.user_comments,
            changeSetMRID=str(cim.change_set.mrid) if cim.change_set else None
        ),
        dependingStageMRID=[str(dep.mrid) for dep in cim.dependencies],
        equipmentContainerMRIDs=list(cim.equipment_container_mrids)
    )


# ###############################################
# # IEC61970 InfIEC61970 Part303 GenericDataSet #
# ###############################################

def data_set_to_pb(cim: DataSet) -> PBDataSet:
    """
    Convert the `DataSet` into its protobuf counterpart.
    """
    return PBDataSet(
        mRID=str(cim.mrid),
        **set_or_null(
            name=cim.name,
            description=cim.description
        )
    )


@bind_to_pb
def change_set_to_pb(cim: ChangeSet) -> PBChangeSet:
    """
    Convert the `ChangeSet` into its protobuf counterpart.
    """
    return PBChangeSet(
        dataset=data_set_to_pb(cim),
        networkModelProjectStageMRID=str(cim.network_model_project_stage.mrid) if cim.network_model_project_stage else "",
        changeSetMemberMRIDs=[str(member.mrid) for member in cim.members]
    )


def change_set_member_to_pb(cim: ChangeSetMember) -> PBChangeSetMember:
    """
    Convert the `ChangeSetMember` into its protobuf counterpart.
    """
    return PBChangeSetMember(
        changeSetMRID=str(cim.change_set.mrid),
        targetObjectMRID=cim.target_object_mrid
    )


@bind_to_pb
def object_creation_to_pb(cim: ObjectCreation) -> PBObjectCreation:
    """
    Convert the `ObjectCreation` into its protobuf counterpart.
    """
    return PBObjectCreation(csm=change_set_member_to_pb(cim))


@bind_to_pb
def object_deletion_to_pb(cim: ObjectDeletion) -> PBObjectDeletion:
    """
    Convert the `ObjectDeletion` into its protobuf counterpart.
    """
    return PBObjectDeletion(csm=change_set_member_to_pb(cim))


@bind_to_pb
def object_modification_to_pb(cim: ObjectModification) -> PBObjectModification:
    """
    Convert the `ObjectModification` into its protobuf counterpart.
    """
    return PBObjectModification(csm=change_set_member_to_pb(cim))
