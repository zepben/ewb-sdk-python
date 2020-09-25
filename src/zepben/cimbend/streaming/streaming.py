"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""
from zepben.cimbend import NetworkService, MetricsStore, CustomerService, DiagramService, ConnectivityNode, Terminal, \
    PowerTransformerEnd
from zepben.cimbend.streaming.exceptions import StreamingException
from zepben.protobuf.cp.cp_pb2_grpc import CustomerProducerStub
from zepben.protobuf.cp.cp_requests_pb2 import CreateCustomerServiceRequest, CompleteCustomerServiceRequest
from zepben.protobuf.dp.dp_pb2_grpc import DiagramProducerStub
from zepben.protobuf.dp.dp_requests_pb2 import CreateDiagramServiceRequest, CompleteDiagramServiceRequest
from zepben.protobuf.np.np_pb2_grpc import NetworkProducerStub
from zepben.protobuf.np.np_requests_pb2 import CreateNetworkRequest, CompleteNetworkRequest
from zepben.protobuf.nc.nc_pb2_grpc import NetworkConsumerStub
from zepben.protobuf.nc.nc_responses_pb2 import GetNetworkHierarchyResponse, GetIdentifiedObjectsResponse
from zepben.protobuf.nc.nc_requests_pb2 import GetNetworkHierarchyRequest, GetIdentifiedObjectsRequest
from zepben.protobuf.nc.nc_data_pb2 import IdentifiedObjectGroup
from zepben.cimbend.streaming.network_rpc import rpc_map
from zepben.cimbend.network.translator.network_cim2proto import *
from zepben.cimbend.network.translator.network_proto2cim import NetworkProtoToCim
import random
import math
from zepben.cimbend.common import resolver
from dataclasses import dataclass


from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment as PBAcLineSegment
from zepben.protobuf.cim.iec61968.assets.Asset_pb2 import Asset as PBAsset
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.AuxiliaryEquipment_pb2 import AuxiliaryEquipment as PBAuxiliaryEquipment
from zepben.protobuf.cim.iec61970.base.core.ConductingEquipment_pb2 import ConductingEquipment as PBConductingEquipment
from zepben.protobuf.cim.iec61970.base.wires.Conductor_pb2 import Conductor as PBConductor
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole as  PBPole
from zepben.protobuf.cim.iec61968.assets.Streetlight_pb2 import Streetlight as PBStreetlight
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode as PBConnectivityNode
from zepben.protobuf.cim.iec61968.metering.EndDevice_pb2 import EndDevice as PBEndDevice
from zepben.protobuf.cim.iec61970.base.core.Equipment_pb2 import Equipment as PBEquipment
from zepben.protobuf.cim.iec61970.base.core.EquipmentContainer_pb2 import EquipmentContainer as PBEquipmentContainer
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer as PBEnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumerPhase_pb2 import EnergyConsumerPhase as PBEnergyConsumerPhase
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource as PBEnergySource
from zepben.protobuf.cim.iec61970.base.wires.EnergySourcePhase_pb2 import EnergySourcePhase as PBEnergySourcePhase
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder as PBFeeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion as PBGeographicalRegion
from zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2 import OperationalRestriction as PBOperationalRestriction
from zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2 import PowerSystemResource as PBPowerSystemResource
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer as PBPowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd as PBPowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger as PBRatioTapChanger
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion as PBSubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation as PBSubstation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal as PBTerminal
from zepben.protobuf.cim.iec61970.base.wires.TransformerEnd_pb2 import TransformerEnd as PBTransformerEnd
from zepben.protobuf.cim.iec61968.metering.UsagePoint_pb2 import UsagePoint as PBUsagePoint


__all__ = ["retrieve_network", "send_network", "send_customer", "send_diagram", "FeederStreamResult", "FeederSummary"]


# TODO: Fill in all fields
@dataclass
class FeederSummary:
    acls_count: int
    node_count: int


@dataclass
class FeederStreamResult:
    success: bool
    summary: FeederSummary


MAX_INT: int = math.pow(2, 32) - 1

def get_random_message_id() -> int:
    """
    Provide a random message_id for gRPC communication.
    :return: A random message_id as an int.
    """
    return random.randint(1, MAX_INT)


def get_identified_object(iog: IdentifiedObjectGroup):
    """
    Unwrap an object group and return the enclosed identified object.
    :param object_group: The object group retrieved.
    :return: A :class:`zepben.protobuf.nc.nc_data_pb2.NetworkIdentifiedObject` containing the underlying identified object.
    """
    og = getattr(iog, "objectGroup", {})
    return getattr(og, "identifiedObject", {})


def get_expected_object(iog: IdentifiedObjectGroup, expected_type: str):
    """
    Try to unwrap received identified object group to expected identified object.
    :param iog: The object group retrieved.
    :param expected_type: The expected type of the underlying identified object.
    :return: One of the possible :class:`zepben.protobuf.cim.*` objects in `zepben.protobuf.nc.nc_data_pb2.NetworkIdentifiedObject`
    """
    identified_object = get_identified_object(iog)
    object_type = identified_object.WhichOneof("identifiedObject")
    if expected_type == "conductingEquipment":
        return getattr(identified_object, object_type, None)

    if object_type != expected_type:
        print(f"Object is not of expected type. Expected '{expected_type}' - Actual '{object_type}'")
    return getattr(identified_object, expected_type, None)


def safely_add(network: NetworkProtoToCim, pb) -> None:
    try:
        network.add_from_pb(pb)
    except Exception as e:
        print(f"L126 {e}") # TODO: remove this!
        #raise StreamingException((f"Failed to add [{pb}] to network. Are you using a cimbend ", "version compatible with the server? Underlying error was: {e}"))


async def get_identified_object_group(stub: NetworkConsumerStub, mrid: str) -> IdentifiedObjectGroup:
    """
    Send a request to the connected server to retrieve an identified object group given its mRID.
    :param stub: A network consumer stub.
    :param mrid: The mRID of the desired object.
    :return: The :class:`zepben.protobuf.nc.nc_data_pb2.IdentifiedObjectGroup` object returned by the server.
    """
    message_id = get_random_message_id()
    request = GetIdentifiedObjectsRequest(messageId=message_id, mrids=[mrid])
    response = stub.getIdentifiedObjects(request)
    for obj in response:
        identified_object_group = obj
    return identified_object_group


async def retrieve_dependency(stub: NetworkConsumerStub, network: NetworkProtoToCim, dependency_type: str, dependency_mrid: str) -> None:
    """
    Add a per length sequence impedance to the network.
    :param stub: A network consumer stub.
    :param network: The network to add the equipment to.
    :param dependency_type: The dependency type.
    :param dependency_mrid: The mRID of the ratio tap changer to retrieve.
    """
    try:
        dependency_iog = await get_identified_object_group(stub, dependency_mrid)
        if dependency_iog:
            dependency = get_expected_object(dependency_iog, dependency_type)
            if dependency:
                await add_equipment_dependencies(stub, network, dependency)
                try:
                    safely_add(network, dependency)
                except Exception as e:
                    print(f"L131 {dependency}")
        else:
            print(f"Could not retrieve {dependency_type} {dependency_mrid}")
    except Exception as e:
        pass #print(f"L135 | {dependency_mrid}")


async def add_equipment_dependencies(stub: NetworkConsumerStub, network: NetworkProtoToCim, equipment) -> None:
    """
    Add an equipment to the network.
    :param stub: A network consumer stub.
    :param network: The network to add the equipment to.
    :param equipment: The equipment that may have dependencies.
    """
    mrid_to_type = {
        "locationMRID": "location",
        "serviceLocationMRID": "location",
        "usagePointLocationMRID": "location",
        "terminalMRID": "terminal",
        "terminalMRIDs": "terminal",
        "baseVoltageMRID": "baseVoltage",
        "normalEnergizingSubstationMRID": "substation",
        "perLengthSequenceImpedanceMRID": "perLengthSequenceImpedance",
        "assetInfoMRID": "assetInfo",
        "ratioTapChangerMRID": "ratioTapChanger",
        "conductingEquipmentMRID": "conductingEquipment",
        "connectivityNodeMRID": "connectivityNode",
        "organisationRoleMRIDs": "organisationRole",
        "streetlightMRIDs": "streetlight",
        "poleMRID": "pole",
        "usagePointMRIDs": "usagePoint",
        "equipmentMRIDs": "equipment",
        "equipmentContainerMRIDs": "equipmentContainer",
        "operationalRestrictionMRIDs": "operationalRestriction",
        "normalHeadTerminalMRID": "terminal",
        "energyConsumerPhasesMRIDs": "phase",
        "energyConsumerMRID": "energyConsumer",
        "energySourcePhasesMRIDs": "phase",
        "energySourceMRID": "energySource",
        "powerTransformerEndMRIDs": "powerTransformerEnd",
        "powerTransformerMRID": "powerTransformer"
    }

    for dep_mrid in mrid_to_type:
        mrid = getattr(equipment, dep_mrid, None)
        if mrid:
            if isinstance(mrid, list):
                for _mrid in mrid:
                    await retrieve_dependency(stub, network, mrid_to_type[dep_mrid], _mrid)
            else:
                await retrieve_dependency(stub, network, mrid_to_type[dep_mrid], mrid)


async def add_identified_object(stub: NetworkConsumerStub, network: NetworkProtoToCim, equipment_io) -> None:
    """
    Add an equipment to the network.
    :param stub: A network consumer stub.
    :param network: The network to add the equipment to.
    :param equipment_io: The equipment identified object returned by the server.
    """
    if equipment_io:
        equipment_type = equipment_io.WhichOneof("identifiedObject")
        if equipment_type:
            # TODO: better check of equipment type (cf. oneof) ?
            equipment = getattr(equipment_io, equipment_type, None)
            # TODO: handle dependencies afterwards?
            await add_equipment_dependencies(stub, network, equipment)
            safely_add(network, equipment)


async def retrieve_equipment(stub: NetworkConsumerStub, network: NetworkProtoToCim, equipment_mrid: str) -> None:
    """
    Retrieve equipment using its mRID and add it to the network.
    :param stub: A network consumer stub.
    :param network: The current network.
    :param equipment_mrid: The equipment mRID as a string.
    """
    equipment_iog = await get_identified_object_group(stub, equipment_mrid)
    if equipment_iog:
        await add_identified_object(stub, network, get_identified_object(equipment_iog))
        for owned_io in getattr(equipment_iog, "ownedIdentifiedObject", []):
            await add_identified_object(stub, network, owned_io)
    else:
        print(f"Could not retrieve equipment {equipment_mrid}")


async def retrieve_feeder(stub: NetworkConsumerStub, network: NetworkProtoToCim, feeder_mrid: str) -> None:
    """
    Retrieve feeder using its mRID, add it to the network and retrieve its equipments.
    :param stub: A network consumer stub.
    :param network: The current network.
    :param equipment_mrid: The equipment mRID as a string.
    """
    feeder_iog = await get_identified_object_group(stub, feeder_mrid)
    if feeder_iog:
        feeder = get_expected_object(feeder_iog, "feeder")
        if feeder:
            safely_add(network, feeder)

        for ce_mrid in getattr(feeder, "currentEquipmentMRIDs", []):
            await retrieve_equipment(stub, network, ce_mrid)
    else:
        print(f"Could not retrieve feeder {feeder_mrid}")


async def retrieve_substation(stub: NetworkConsumerStub, network: NetworkProtoToCim, substation_mrid: str) -> None:
    """
    Retrieve substation using its mRID, add it to the network and retrieve its feeders.
    :param stub: A network consumer stub.
    :param network: The current network.
    """
    sub_iog = await get_identified_object_group(stub, substation_mrid)
    if sub_iog:
        sub = get_expected_object(sub_iog, "substation")
        if sub:
            safely_add(network, sub)

        for nef_mrid in getattr(sub, "normalEnergizedFeederMRIDs", []):
            await retrieve_feeder(stub, network, nef_mrid)
        # add loopMRIDs circuitMRIDs normalEnergizedLoopMRIDs ?
    else:
        print(f"Could not retrieve substation {substation_mrid}")


async def retrieve_sub_geographical_region(stub: NetworkConsumerStub, network: NetworkProtoToCim, sub_geographical_region_mrid: str) -> None:
    """
    Retrieve subgeographical region using its mRID, add it to the network and retrieve its substations.
    :param stub: A network consumer stub.
    :param network: The current network.
    """
    sgr_iog = await get_identified_object_group(stub, sub_geographical_region_mrid)
    if sgr_iog:
        sgr = get_expected_object(sgr_iog, "subGeographicalRegion")
        if sgr:
            safely_add(network, sgr)

        for sub_mrid in getattr(sgr, "substationMRIDs", []):
            await retrieve_substation(stub, network, sub_mrid)
    else:
        print(f"Could not retrieve sub geographical region {sub_geographical_region_mrid}")


async def retrieve_geographical_region(stub: NetworkConsumerStub, network: NetworkProtoToCim, geographical_region_mrid: str):
    """
    Retrieve geographical region using its mRID, add it to the network and retrieve its subgeographical regions.
    :param stub: A network consumer stub.
    :param network: The current network.
    """
    gr_iog = await get_identified_object_group(stub, geographical_region_mrid)
    if gr_iog:
        gr = get_expected_object(gr_iog, "geographicalRegion")
        if gr:
            safely_add(network, gr)

        for sgr_mrid in getattr(gr, "subGeographicalRegionMRIDs", []):
            await retrieve_sub_geographical_region(stub, network, sgr_mrid)
    else:
        print(f"Could not retrieve geographical region {geographical_region_mrid}")


async def retrieve_network(channel) -> NetworkService:
    """
    Request network hierarchy and retrieve the network geographical regions.
    :param channel: A gRPC channel to the gRPC server.
    :return: The retrieved `wepben.cimbend.NetworkService` object.
    """
    network = NetworkProtoToCim(NetworkService())
    stub = NetworkConsumerStub(channel)
    message_id = get_random_message_id()
    request = GetNetworkHierarchyRequest(messageId=message_id)
    response = stub.getNetworkHierarchy(request)
    for gr in getattr(response, "geographicalRegions", []):
        gr_mrid = getattr(gr, "mRID", None)
        if gr_mrid:
            await retrieve_geographical_region(stub, network, gr_mrid)

    service = network.service
    print(f"L341 {len(service._unresolved_references)}")
    await empty_unresolved_refs(stub, network)

    return service


async def empty_unresolved_refs(stub, network):
    service = network.service
    #while len(service._unresolved_references) > 0:
    for ref in service.unresolved_references():
        await retrieve_equipment(stub, network, ref)


async def create_network(stub: NetworkProducerStub):
    stub.CreateNetwork(CreateNetworkRequest())


async def complete_network(stub: NetworkProducerStub):
    stub.CompleteNetwork(CompleteNetworkRequest())


class NoSuchRPCException(Exception):
    pass


class ProtoAttributeError(Exception):
    pass


async def send_network(stub: NetworkProducerStub, network_service: NetworkService):
    """
    Send a feeder to the connected server.
    Note that ConnectivityNodes are never sent with this method, a Terminal is sent containing the ConnectivityNode mRID
    which is the only necessary information to rebuild ConnectivityNodes.
    :param ns: The Network containing all equipment in the feeder.
    :return: A :class:`zepben.cimbend.streaming.streaming.FeederStreamResult
    """
    # Terminals and PTE's are handled specifically below
    for obj in network_service.objects():
        try:
            pb = obj.to_pb()
        except Exception as e:
            raise CimTranslationException(f"Failed to translate {obj} to protobuf.") from e

        try:
            rpc = getattr(stub, rpc_map[type(pb)][0])
        except AttributeError as e:
            raise NoSuchRPCException(f"RPC {rpc_map[type(pb)][0]} could not be found in {stub.__class__.__name__}") from e

        try:
            attrname = f"{obj.__class__.__name__[:1].lower()}{obj.__class__.__name__[1:]}"
            req = rpc_map[type(pb)][1]()
            getattr(req, attrname).CopyFrom(pb)
        except AttributeError as e:
            raise ProtoAttributeError() from e

        rpc(req)


async def create_diagram(stub: DiagramProducerStub):
    stub.CreateDiagramService(CreateDiagramServiceRequest())


async def complete_diagram(stub: DiagramProducerStub):
    stub.CompleteDiagramService(CompleteDiagramServiceRequest())


async def send_diagram(stub: DiagramProducerStub, diagram_service: DiagramService):
    pass


async def create_customer(stub: CustomerProducerStub):
    stub.CreateCustomerService(CreateCustomerServiceRequest())


async def complete_customer(stub: CustomerProducerStub):
    stub.CompleteCustomerService(CompleteCustomerServiceRequest())


async def send_customer(stub: CustomerProducerStub, customer_service: CustomerService):
    pass