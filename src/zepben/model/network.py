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


import logging
import inspect
from uuid import uuid4

from zepben.model.common import Location
from zepben.model.diagram_layout import DiagramObject
from zepben.model.equipment import PowerSystemResource
from zepben.model.exceptions import *
from zepben.model.base_voltage import BaseVoltage
from zepben.model.asset_info import AssetInfo
from zepben.model.connectivity_node import ConnectivityNode
from zepben.model.connectors import Junction
from zepben.model.energy_consumer import EnergyConsumer
from zepben.model.energy_source import EnergySource
from zepben.model.aclinesegment import ACLineSegment
from zepben.model.power_transformer import PowerTransformer
from zepben.model.switch import Breaker
from zepben.model.per_length_sequence_impedance import PerLengthSequenceImpedance
from zepben.model.metrics_store import MetricsStore
from zepben.model.metering import UsagePoint, Meter
from zepben.model.customer import Customer
from zepben.model.decorators import create_registrar, map_type
from zepben.cim.iec61970 import EnergySource as PBEnergySource, EnergyConsumer as PBEnergyConsumer, Breaker as PBBreaker, \
    PowerTransformer as PBPowerTransformer, AcLineSegment as PBAcLineSegment, BaseVoltage as PBBaseVoltage, \
    PerLengthSequenceImpedance as PBPerLengthSequenceImpedance, Junction as PBJunction
from zepben.cim.iec61968 import AssetInfo as PBAssetInfo, Customer as PBCustomer, Meter as PBMeter, UsagePoint as PBUsagePoint
from zepben.model.tracing.phasing import SetPhases
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)
TRACED_NETWORK_FILE = str(Path.home().joinpath(Path("traced.json")))


class ConnectivityNodeContainer(PowerSystemResource):
    """
    This class is currently unused in our CIM profile, but may be extended in the future
    """
    def __init__(self, mrid: str, name: str = "", diag_objs: List[DiagramObject] = None, location: Location = None):
        super().__init__(mrid=mrid, name=name, diag_objs=diag_objs, location=location)


class EquipmentContainer(ConnectivityNodeContainer):
    """
    A full representation of the power network.
    Contains a map of equipment (string ID's -> Equipment/Nodes/etc)
    **All** `IdentifiedObject's` submitted to this EquipmentContainer **MUST** have unique mRID's!
    """

    # A decorator simply used for registering EquipmentContainer getter functions.
    # If you create a new equipment map in __init__, you should create a corresponding getter function and
    # decorate it with @getter
    getter = create_registrar()

    # A decorator used to specify which types are stored in each map. For every map there should be a
    # corresponding `@property` declaration that is decorated with `type_map(class, [pb_class, gRPC_create_func])`,
    # where `class` indicates the CIM type stored in that map, `pb_class` optionally indicates `class`'s corresponding
    # Protobuf class, and `gRPC_create_func` indicates `pb_class`'s corresponding gRPC function for streaming.
    # Utilised in the `add` method, but also in the streaming library.
    type_map = map_type()

    def __init__(self, metrics_store: MetricsStore = None, name: str = "default", mrid=None,
                 diag_objs: List[DiagramObject] = None, location: Location = None):
        """
        Represents a whole network. At the moment there's a single index on equipment ID's -> all types of equipment,
        as well as an index on energy source ID's -> energy sources.
        :param metrics_store: Storage for meter measurement data associated with this network.
        """
        super().__init__(mrid=mrid if mrid is not None else uuid4(), name=name, diag_objs=diag_objs, location=location)
        self._asset_infos = {}
        self._base_voltages = {}
        self._breakers = {}
        self._connectivity_nodes = {}
        self._customers = {}
        self._energy_sources = {}
        self._energy_consumers = {}
        self._junctions = {}
        self._lines = {}
        self._meters = {}
        self._seq_impedances = {}
        self._transformers = {}
        self._usage_points = {}
        self.metrics_store = metrics_store

    @type_map(BaseVoltage, PBBaseVoltage, 'createBaseVoltage')
    @property
    def base_voltages(self):
        return self._base_voltages

    @type_map(AssetInfo, PBAssetInfo, 'createAssetInfo')
    @property
    def asset_infos(self):
        return self._asset_infos

    @type_map(EnergySource, PBEnergySource, 'createEnergySource')
    @property
    def energy_sources(self):
        return self._energy_sources

    @type_map(EnergyConsumer, PBEnergyConsumer, 'createEnergyConsumer')
    @property
    def energy_consumers(self):
        return self._energy_consumers

    @type_map(Breaker, PBBreaker, 'createBreaker')
    @property
    def breakers(self):
        return self._breakers

    @type_map(ConnectivityNode)
    @property
    def connectivity_nodes(self):
        return self._connectivity_nodes

    @type_map(Customer, PBCustomer, 'createCustomer')
    @property
    def customers(self):
        return self._customers

    @type_map(PerLengthSequenceImpedance, PBPerLengthSequenceImpedance, 'createPerLengthSequenceImpedance')
    @property
    def seq_impedances(self):
        return self._seq_impedances

    @type_map(ACLineSegment, PBAcLineSegment, 'createAcLineSegment')
    @property
    def lines(self):
        return self._lines

    @type_map(Junction, PBJunction, 'createJunction')
    @property
    def junctions(self):
        return self._junctions

    @type_map(Meter, PBMeter, 'createMeter')
    @property
    def meters(self):
        return self._meters

    @type_map(PowerTransformer, PBPowerTransformer, 'createPowerTransformer')
    @property
    def transformers(self):
        return self._transformers

    @type_map(UsagePoint, PBUsagePoint, 'createUsagePoint')
    @property
    def usage_points(self):
        return self._usage_points

    def __iter__(self):
        """
        This performs a depth-first iteration of the network, stopping
        at any open switches or out-of-service equipment.
        :return:
        """
        return self

    def __next__(self):
        raise NotImplementedError()

    def __getitem__(self, item):
        """
        Gets an mRID from the EquipmentContainer, checking all mappings.
        It is preferred to use the get_* methods if you know what type you are retrieving.
        :param item:
        :return:
        :raises: KeyError when `item` isn't in the EquipmentContainer.
        """
        for m in self.getter.all.values():
            try:
                return m(self, item)
            except MissingReferenceException:
                continue
        else:
            raise KeyError(f"{item}")

    def keys(self):
        """
        This is probably a terrible idea. Should make this unnecessary. Do not use
        :return:
        """
        k = set(self.meters.keys()).union(self.base_voltages.keys(), self.connectivity_nodes.keys(),
                                          self.energy_consumers.keys(), self.energy_sources.keys(),
                                          self.transformers.keys(), self.breakers.keys(), self.lines.keys(),
                                          self.customers.keys(), self.usage_points.keys(), self.seq_impedances.keys(),
                                          self.asset_infos.keys())
        return k

    def get_primary_sources(self):
        """
        Get the primary source for this network. All directions are applied relative to this EnergySource
        :return: The primary EnergySource
        """
        return [source for source in self.energy_sources.values() if source.has_phases()]

    @getter
    def get_connectivity_node(self, cn_mrid):
        try:
            return self.connectivity_nodes[cn_mrid]
        except KeyError:
            raise NoConnectivityNodeException(f"{cn_mrid}")

    @getter
    def get_aclinesegment(self, acls_mrid):
        try:
            return self.lines[acls_mrid]
        except KeyError:
            raise NoACLineSegmentException(f"{acls_mrid}")

    @getter
    def get_junction(self, j_mrid):
        try:
            return self.junctions[j_mrid]
        except KeyError:
            raise NoJunctionException(f"{j_mrid}")

    @getter
    def get_energyconsumer(self, ec_mrid):
        try:
            return self.energy_consumers[ec_mrid]
        except KeyError:
            raise NoEnergyConsumerException(f"{ec_mrid}")

    @getter
    def get_breaker(self, br_mrid):
        try:
            return self.breakers[br_mrid]
        except KeyError:
            raise NoBreakerException(f"{br_mrid}")

    @getter
    def get_transformer(self, tf_mrid):
        try:
            return self.transformers[tf_mrid]
        except KeyError:
            raise NoTransformerException(f"{tf_mrid}")

    @getter
    def get_energysource(self, es_mrid):
        try:
            return self.energy_sources[es_mrid]
        except KeyError:
            raise NoEnergySourceException(f"{es_mrid}")

    @getter
    def get_meter(self, meter_mrid):
        try:
            return self.meters[meter_mrid]
        except KeyError:
            raise NoMeterException(f"{meter_mrid}")

    @getter
    def get_base_voltage(self, bv_mrid):
        try:
            return self.base_voltages[bv_mrid]
        except KeyError:
            raise NoBaseVoltageException(f"{bv_mrid}")

    @getter
    def get_asset_info(self, ai_mrid):
        try:
            return self.asset_infos[ai_mrid]
        except KeyError:
            raise NoAssetInfoException(f"{ai_mrid}")

    @getter
    def get_plsi(self, plsi_mrid):
        try:
            return self.seq_impedances[plsi_mrid]
        except KeyError:
            raise NoPerLengthSeqImpException(f"{plsi_mrid}")

    @getter
    def get_usage_point(self, up_mrid):
        try:
            return self.usage_points[up_mrid]
        except KeyError:
            raise NoUsagePointException(f"{up_mrid}")

    @getter
    def get_customer(self, cust_mrid):
        try:
            return self.customers[cust_mrid]
        except KeyError:
            raise NoCustomerException(f"{cust_mrid}")

    def iter_connectivitynodes(self):
        for node in self.connectivity_nodes.values():
            yield node

    def iter_lines(self):
        for line in self.lines.values():
            yield line

    def iter_transformers(self):
        for trafo in self.transformers.values():
            yield trafo

    def iter_breakers(self):
        for breaker in self.breakers.values():
            yield breaker

    def iter_meters(self):
        for meter in self.meters.values():
            yield meter

    def iter_assetinfos(self):
        for ai in self.asset_infos.values():
            yield ai

    def iter_perlengthseqimpedances(self):
        for si in self.seq_impedances.values():
            yield si

    def iter_usagepoints(self):
        for up in self.usage_points.values():
            yield up

    def iter_customers(self):
        for c in self.customers.values():
            yield c

    def iter_energysources(self):
        for es in self.energy_sources.values():
            yield es

    def iter_energyconsumers(self):
        for ec in self.energy_consumers.values():
            yield ec

    def iter_basevoltages(self):
        for bv in self.base_voltages.values():
            yield bv

    def add_connectivitynode(self, mrid: str):
        """
        Add a connectivity node to the network.
        :param mrid: mRID of the ConnectivityNode
        :return: A new ConnectivityNode with `mrid` if it doesn't already exist, otherwise the existing
                 ConnectivityNode represented by `mrid`
        """
        if mrid not in self.connectivity_nodes:
            self.connectivity_nodes[mrid] = ConnectivityNode(mrid)
            return self.connectivity_nodes[mrid]
        else:
            return self.connectivity_nodes[mrid]

    def add(self, obj):
        """
        Adds object to its corresponding map in the network. Utilises the type_map decorator to identify the
        corresponding map. Supports protobuf types, which must also be specified with the type_map decorator.
        :param obj: The object to add. Must extend IdentifiedObject and have a corresponding map field in the network.
        :raises: :class:`zepben.model.exceptions.NetworkException` if there is no corresponding type_map for the
                 provided type.
                 A subclass of :class:`zepben.model.exceptions.MissingReferenceException` if any dependencies are not
                 already in the network. See the types corresponding `from_pb` for specifics.
        """
        try:
            # General case, obj is a CIM class with a mapping or a protobuf class.
            map_ = self.type_map.all[type(obj)].fget(self)
            cls = self.type_map.pb_to_cim[type(obj)]
        except (AttributeError, KeyError):
            # Case where obj is a subclass of a class that has a mapping (e.g obj = CableInfo, map is asset_infos)
            for clazz in inspect.getmro(type(obj)):
                try:
                    map_ = self.type_map.all[clazz].fget(self)
                    break
                except KeyError:
                    pass
            else:
                raise NetworkException((f"Type {type(obj)} did not have a corresponding map in the network and thus could"
                                        f"not be added. You've either passed a non-CIM type or forgot to decorate the"
                                        f"maps property with the correct types."))

        try:
            # If mrid exists we assume we have a CIM class and add it to its map.
            map_[obj.mrid] = obj

        except AttributeError:
            # Otherwise it's a protobuf class.
            # Need to pass in keyword args - at the moment the only possibility is the network.
            # This will throw any exception the corresponding `from_pb` throws
            try:
                o = cls.from_pb(obj, network=self)
            except MissingReferenceException as mre:
                mre.referrer = obj  # To add referrer details to error message.
                raise mre
            map_[o.mrid] = o

    async def set_phases(self):
        set_phases = SetPhases()
        await set_phases.run(self)

    def _dumpTracing(self):
        with open(TRACED_NETWORK_FILE, "w") as f:
            for e in self.depth_first_trace_and_apply():
                assert len(e.terminals) < 3
                upstream_count = 0
                f.write(str(e) + "\n")
                for term in e.terminals:
                    if term.direction:
                        upstream_count += 1
                    f.write("\t" + str(term) + "\n")
                try:
                    if isinstance(e, EnergySource):
                        assert upstream_count == 0, "energy source had more than 0 upstreams"
                    else:
                        assert upstream_count == 1, "Need at least 1 upstream terminal"
                except AssertionError as a:
                    logger.error(a)
                    logger.error(str(e))
                    for term in e.terminals:
                        logger.error(str(term))
                f.write("\n\n")

    # TODO: implement?
    @staticmethod
    def from_pb(pb_gr):
        raise NotImplementedError()

    def to_pb(self):
        raise NotImplementedError()
