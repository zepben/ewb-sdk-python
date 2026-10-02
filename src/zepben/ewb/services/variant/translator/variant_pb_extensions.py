#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# NOTE: Mirrors the JVM `VariantPbExtensions.kt` — these `mrid()` extensions are monkey-patched onto the
# protobuf message classes so the proto2cim translator can read a stable mRID from any variant object,
# including the nested `ChangeSetMember` (whose mRID is computed from `changeSetMRID` + `targetObjectMRID`).

from zepben.protobuf.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.NetworkModelProject_pb2 import NetworkModelProject as PBNetworkModelProject
from zepben.protobuf.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.NetworkModelProjectComponent_pb2 import NetworkModelProjectComponent as PBNetworkModelProjectComponent
from zepben.protobuf.cim.iec61970.infiec61970.infpart303.networkmodelprojects.AnnotatedProjectDependency_pb2 import AnnotatedProjectDependency as PBAnnotatedProjectDependency
from zepben.protobuf.cim.iec61970.infiec61970.infpart303.networkmodelprojects.NetworkModelProjectStage_pb2 import NetworkModelProjectStage as PBNetworkModelProjectStage
from zepben.protobuf.cim.iec61970.infiec61970.part303.genericdataset.ChangeSet_pb2 import ChangeSet as PBChangeSet
from zepben.protobuf.cim.iec61970.infiec61970.part303.genericdataset.ChangeSetMember_pb2 import ChangeSetMember as PBChangeSetMember


PBNetworkModelProject.mrid = lambda self: self.nmpc.io.mRID
PBNetworkModelProjectStage.mrid = lambda self: self.nmpc.io.mRID
PBNetworkModelProjectComponent.mrid = lambda self: self.io.mRID
PBChangeSetMember.mrid = lambda self: f"{self.changeSetMRID}_{self.targetObjectMRID}"
PBChangeSet.mrid = lambda self: self.dataset.mRID
PBAnnotatedProjectDependency.mrid = lambda self: self.mRID
