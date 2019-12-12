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
import pickle
from zepben.model.exceptions import *
from zepben.model.terminal import Terminal
from zepben.model.base_voltage import BaseVoltage
from zepben.model.asset_info import CableInfo, OverheadWireInfo, TransformerEndInfo
from zepben.model.connectivity_node import ConnectivityNode
from zepben.model.energy_consumer import EnergyConsumer
from zepben.model.energy_source import EnergySource
from zepben.model.aclinesegment import ACLineSegment
from zepben.model.power_transformer import PowerTransformer
from zepben.model.switch import Breaker
from zepben.model.per_length_sequence_impedance import PerLengthSequenceImpedance
from zepben.model.metrics_store import MetricsStore
from zepben.model.metering import UsagePoint, Meter
from zepben.model.customer import Customer
from zepben.model.decorators import create_registrar
from typing import List
from pathlib import Path

logger = logging.getLogger(__name__)
TRACED_NETWORK_FILE = str(Path.home().joinpath(Path("traced.json")))


class EquipmentContainer(object):
    """
    A full representation of the power network.
    Contains a map of equipment (string ID's -> Equipment/Nodes/etc)
    **All** `IdentifiedObject's` submitted to this EquipmentContainer **MUST** have unique mRID's!
    """

    # A decorator simply used for registering EquipmentContainer getter functions.
    # If you create a new equipment map in __init__, you should create a corresponding getter function and
    # decorate it with @getter
    getter = create_registrar()

    def __init__(self, metrics_store: MetricsStore, name: str = "default"):
        """
        Represents a whole network. At the moment there's a single index on equipment ID's -> all types of equipment,
        as well as an index on energy source ID's -> energy sources.
        TODO: Split resources into a dictionary for each type and provide type based getter methods for each
              type - as well as a getter for when type is unknown.
        :param metrics_store: Storage for meter measurement data associated with this network.
        """
        self.name = name
        # TODO: merge these into gets... stop using resources
        self.asset_infos = {}
        self.base_voltages = {}
        self.breakers = {}
        self.connectivity_nodes = {}
        self.customers = {}
        self.energy_sources = {}
        self.energy_consumers = {}
        self.lines = {}
        self.meters = {}
        self.seq_impedances = {}
        self.transformers = {}
        self.usage_points = {}
        self.metrics_store = metrics_store

    def __iter__(self):
        """
        This performs a depth-first iteration of the network, stopping
        at any open switches or out-of-service equipment.
        :return:
        """
        return self

    def __next__(self):
        for e in self.depth_first_trace_and_apply():
            yield e

        raise StopIteration()

    def __getitem__(self, item):
        """
        Gets an mRID from the EquipmentContainer, checking all mappings.
        It is preferred to use the get_* methods if you know what type you are retrieving.
        :param item:
        :return:
        :raises: KeyError when `item` isn't in the EquipmentContainer.
        """
        for m in EquipmentContainer.getter.all.values():
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
    def get_breaker(self, br_mrid):
        try:
            return self.breakers[br_mrid]
        except KeyError:
            raise NoBreakerException(f"{br_mrid}")

    @getter
    def get_aclinesegment(self, acls_mrid):
        try:
            return self.lines[acls_mrid]
        except KeyError:
            raise NoACLineSegmentException(f"{acls_mrid}")

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
    def get_energyconsumer(self, ec_mrid):
        try:
            return self.energy_consumers[ec_mrid]
        except KeyError:
            raise NoEnergyConsumerException(f"{ec_mrid}")

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

    def depth_first_trace_and_apply(self, term_fn=None):
        """
        term_fn will be applied to each terminal prior to being returned
        """
        equips_to_trace = []
        traced = set()
        for source in self.energy_sources.values():
            # All sources have no upstream terminals
            yield source
            for t in source.terminals:
                traced.add(t.mrid)
            equips_to_trace.append(source)
            while equips_to_trace:
                try:
                    equip = equips_to_trace.pop()
                except IndexError:  # No more equipment
                    break
                # Explore all connectivity nodes for this equipments terminals,
                # and set upstream on each terminal.
                for terminal in equip.terminals:
                    conn_node = terminal.connectivity_node
                    for term in conn_node:
                        if term.mrid in traced:
                            continue
                        if term != terminal:
                            if not term.equipment.connected():
                                continue
                            equips_to_trace.append(term.equipment)
                            yield term.equipment
                        # Don't trace over a terminal twice to stop us from reversing direction
                        traced.add(term.mrid)

    def trace_and_set_directions(self):
        equips_to_trace = []
        traced = set()
        for source in self.energy_sources.values():
            # All sources have no upstream terminals
            upstream = False
            for t in source.terminals:
                t.direction = upstream
                traced.add(t.mrid)
            equips_to_trace.append(source)
            while equips_to_trace:
                upstream = not upstream
                try:
                    equip = equips_to_trace.pop()
                except IndexError:  # No more equipment
                    break
                # Explore all connectivity nodes for this equipments terminals,
                # and set upstream on each terminal.
                for terminal in equip.terminals:
                    conn_node = terminal.connectivity_node
                    terminal.direction = upstream
                    upstream = not upstream
                    for term in conn_node:
                        if term.mrid in traced:
                            continue
                        if term != terminal:
                            if not term.equipment.connected():
                                continue
                            term.direction = upstream
                            equips_to_trace.append(term.equipment)
                        # Don't trace over a terminal twice to stop us from reversing direction
                        traced.add(term.mrid)

    def create_connectivity_nodes(self, pb_terminals):
        """
        Extract and create ConnectivityNode's from a set of protobuf Terminals.
        Order of the terminals is preserved and indicates their sequenceNumber
        :param pb_terminals: A list of protobuf :class:`zepben.cim.iec61970.core.Terminal`'s
        :return: A set of CIM terminals.
        """
        terms = []
        for terminal in pb_terminals:
            conn_node = self.add_connectivitynode(terminal.connectivityNodeMRID)
            term = Terminal(terminal.mRID, terminal.phases, conn_node, terminal.name, connected=terminal.connected)
            conn_node.add_terminal(term)
            terms.append(term)
        return terms

    def add_connectivitynode(self, mrid):
        """
        Add a connectivity node to the network.
        :param mrid: mRID of the ConnectivityNode
        :return: A new ConnectivityNode with `mrid` if it doesn't already exist, otherwise the existing
                 ConnectivityNode represented by `mrid`
        """
        if mrid not in self.connectivity_nodes:
            node = ConnectivityNode(mrid)
            self.connectivity_nodes[mrid] = node
            return node
        else:
            return self.connectivity_nodes[mrid]

    def add_pb_base_voltage(self, pb_bv):
        """
        Add a Protobuf BaseVoltage
        :param pb_bv: :class:`zepben.cim.iec61970.base.core.BaseVoltage`
        """
        bv = BaseVoltage.from_pb(pb_bv)
        self.base_voltages[bv.mrid] = bv

    def add_pb_per_length_sequence_impedance(self, pb_plsi):
        """
        Add a Protobuf PerLengthSequenceImpedance
        :param pb_plsi: :class:`zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance`
        """
        plsi = PerLengthSequenceImpedance.from_pb(pb_plsi)
        self.seq_impedances[plsi.mrid] = plsi

    def add_pb_asset_info(self, pb_ai):
        """
        Add a Protobuf AssetInfo
        :param pb_ai: :class:`zepben.cim.iec61968.assetinfo.AssetInfo`
        :raises: NoEquipmentException if no field in the oneof was set.
        """
        if pb_ai.HasField("cableInfo"):
            cable_info = CableInfo.from_pb(pb_ai.cableInfo)
            self.asset_infos[cable_info.mrid] = cable_info
        elif pb_ai.HasField("overheadWireInfo"):
            overhead_wire_info = OverheadWireInfo.from_pb(pb_ai.overheadWireInfo)
            self.asset_infos[overhead_wire_info.mrid] = overhead_wire_info
        elif pb_ai.HasField("transformerEndInfo"):
            transformer_end_info = TransformerEndInfo.from_pb(pb_ai.transformerEndInfo)
            self.asset_infos[transformer_end_info.mrid] = transformer_end_info
        else:
            raise NoEquipmentException("assetInfo was empty")

    def add_pb_usage_point(self, pb_up):
        """
        Add a Protobuf UsagePoint
        :param pb_up: :class:`zepben.cim.iec61968.metering.UsagePoint`
        """
        up = UsagePoint.from_pb(pb_up, self)
        self.usage_points[up.mrid] = up

    def add_pb_customer(self, pb_c):
        """
        Add a Protobuf Customer
        :param pb_c: :class:`zepben.cim.iec61968.customers.Customer`
        """
        customer = Customer.from_pb(pb_c)
        self.customers[customer.mrid] = customer

    def add_pb_meter(self, pb_m):
        """
        Add a Protobuf Meter
        :param pb_m: :class:`zepben.cim.iec61968.metering.Meter`
        :raises: a subclass of MissingReferenceException if any reference fields in the message are not already in the
                 network See :func:`Meter.from_pb`
        """
        self.meters[pb_m.mRID] = Meter.from_pb(pb_m, self)

    def add_pb_energy_source(self, pb_es):
        """
        Add an energy source to the network that has come through as a protobuf message
        :param pb_es: :class:`zepben.cim.iec61970.base.wires.EnergySource`
        :raises: a subclass of MissingReferenceException if any reference fields in the message are not already in the
                 network. See :func:`EnergySource.from_pb`
        """
        self.energy_sources[pb_es.mRID] = EnergySource.from_pb(pb_es, self)

    def add_pb_energy_consumer(self, pb_ec):
        """
        Add a Protobuf EnergyConsumer
        :param pb_ec: :class:`zepben.cim.iec61970.base.wires.EnergyConsumer`
        :raises: a subclass of MissingReferenceException if any reference fields in the message are not already in the
                 network. See :func:`EnergyConsumer.from_pb`
        """
        self.energy_consumers[pb_ec.mRID] = EnergyConsumer.from_pb(pb_ec, self)

    def add_pb_transformer(self, pb_tf):
        """
        Add a Protobuf PowerTransformer
        :param pb_tf: :class:`zepben.cim.iec61970.base.wires.PowerTransformer`
        :raises: a subclass of MissingReferenceException if any reference fields in the message are not already in the
                 network. See :func:`PowerTransformer.from_pb`
        """
        self.transformers[pb_tf.mRID] = PowerTransformer.from_pb(pb_tf, self)

    def add_pb_aclinesegment(self, pb_acls):
        """
        Add a Protobuf AcLineSegment
        :param pb_acls: :class:`zepben.cim.iec61970.base.wires.AcLineSegment`
        :raises: a subclass of MissingReferenceException if any reference fields in the message are not already in the
                 network. See :func:`ACLineSegment.from_pb`
        """
        self.lines[pb_acls.mRID] = ACLineSegment.from_pb(pb_acls, self)

    def add_pb_breaker(self, pb_br):
        """
        Add a Protobuf Breaker
        :param pb_br: :class:`zepben.cim.iec61970.base.wires.Breaker`
        :raises: a subclass of MissingReferenceException if any reference fields in the message are not already in the
                 network. See :func:`Breaker.from_pb`
        """
        self.breakers[pb_br.mRID] = Breaker.from_pb(pb_br, self)

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

