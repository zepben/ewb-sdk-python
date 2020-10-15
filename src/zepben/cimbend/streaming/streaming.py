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
from zepben.cimbend import NetworkService, CustomerService, DiagramService
from zepben.cimbend.streaming.exceptions import StreamingException
from zepben.protobuf.cp.cp_pb2_grpc import CustomerProducerStub
from zepben.protobuf.cp.cp_requests_pb2 import CreateCustomerServiceRequest, CompleteCustomerServiceRequest
from zepben.protobuf.dp.dp_pb2_grpc import DiagramProducerStub
from zepben.protobuf.dp.dp_requests_pb2 import CreateDiagramServiceRequest, CompleteDiagramServiceRequest
from zepben.protobuf.np.np_pb2_grpc import NetworkProducerStub
from zepben.protobuf.np.np_requests_pb2 import CreateNetworkRequest, CompleteNetworkRequest
from zepben.protobuf.nc.nc_pb2_grpc import NetworkConsumerStub
from zepben.protobuf.nc.nc_requests_pb2 import GetNetworkHierarchyRequest, GetIdentifiedObjectsRequest
from zepben.protobuf.nc.nc_data_pb2 import IdentifiedObjectGroup
from zepben.cimbend.streaming.network_rpc import rpc_map
from zepben.cimbend.network.translator.network_cim2proto import *
from zepben.cimbend.network.translator.network_proto2cim import NetworkProtoToCim
import random
import math
from dataclasses import dataclass

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
        raise StreamingException(f"Failed to add [{pb}] to network. Are you using a cimbend version compatible with the server? Underlying error was: {e}")


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
        for owned_io in getattr(equipment_iog, 'ownedIdentifiedObject', []):
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

        for nef_mrid in set(getattr(sub, "normalEnergizedFeederMRIDs", [])):
            await retrieve_feeder(stub, network, nef_mrid)
        # add loopMRIDs circuitMRIDs normalEnergizedLoopMRIDs ?
    else:
        print(f"Could not retrieve substation {substation_mrid}")


async def retrieve_sub_geographical_region(stub: NetworkConsumerStub, network: NetworkProtoToCim,
                                           sub_geographical_region_mrid: str) -> None:
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


async def retrieve_geographical_region(stub: NetworkConsumerStub, network: NetworkProtoToCim,
                                       geographical_region_mrid: str):
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
    proto2cim = NetworkProtoToCim(NetworkService())
    stub = NetworkConsumerStub(channel)
    message_id = get_random_message_id()
    request = GetNetworkHierarchyRequest(messageId=message_id)
    response = stub.getNetworkHierarchy(request)
    for gr in getattr(response, "geographicalRegions", []):
        gr_mrid = getattr(gr, "mRID", None)
        if gr_mrid:
            await retrieve_geographical_region(stub, proto2cim, gr_mrid)

    await empty_unresolved_refs(stub, proto2cim)

    return proto2cim.service


async def empty_unresolved_refs(stub, proto2cim):
    service = proto2cim.service
    while service.has_unresolved_references():
        for mrid in service.unresolved_mrids():
            await retrieve_equipment(stub, proto2cim, mrid)


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
            raise NoSuchRPCException(
                f"RPC {rpc_map[type(pb)][0]} could not be found in {stub.__class__.__name__}") from e

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
