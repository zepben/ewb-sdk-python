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
from zepben.model import DiagramObject, Location, Terminal, RatioTapChanger, BaseVoltage
from zepben.model.asset_info import CableInfo, OverheadWireInfo, TransformerEndInfo
from zepben.model.connectivity_node import ConnectivityNode
from zepben.model.energy_consumer import EnergyConsumer, EnergyConsumerPhase
from zepben.model.energy_source import EnergySource
from zepben.model.aclinesegment import ACLineSegment
from zepben.model.power_transformer import PowerTransformer, PowerTransformerEnd
from zepben.model.asset_info import WireInfo
from zepben.model.switch import Breaker
from zepben.model.per_length_sequence_impedance import PerLengthSequenceImpedance
from zepben.model.metrics_store import MetricsStore
from zepben.model.metering import UsagePoint, Meter
from zepben.model.customer import Customer
from zepben.cim.iec61970.base.wires.VectorGroup_pb2 import VectorGroup
from typing import List
from pprint import pformat
from pathlib import Path

logger = logging.getLogger(__name__)
TRACED_NETWORK_FILE = str(Path.home().joinpath(Path("traced.json")))


class EquipmentContainer(object):
    """
    A full representation of the power network.
    Contains a map of equipment (string ID's -> Equipment/Nodes/etc)
    And a reverse map of equipment to terminals
    """

    def __init__(self, metrics_store: MetricsStore, name: str = "default"):
        """
        Represents a whole network. At the moment there's a single index on equipment ID's -> all types of equipment,
        as well as an index on energy source ID's -> energy sources.
        TODO: Split resources into a dictionary for each type and provide type based getter methods for each
              type - as well as a getter for when type is unknown.
        :param metrics_store: Storage for meter measurement data associated with this network.
        """
        self.name = name
        self.resources = {}
        self.energy_sources = {}
        self.base_voltages = {}
        self.seq_impedances = {}
        self.asset_infos = {}
        self.usage_points = {}
        self.customers = {}
        self.meters = {}
        self.metrics_store = metrics_store

    def print_network(self):
        logger.info(f"Resources:\n{pformat(self.resources)}")

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
        TODO: This requires everything to have unique ID's! Need to enforce/document this
        It is preferred to use the get_* methods if you know what type you are retrieving.
        :param item:
        :return:
        :raises: NoEquipmentException when item isn't in the EquipmentContainer. This should be caught
                 and re-thrown with more detail.
        """
        if item in self.resources:
            return self.resources[item]
        if item in self.asset_infos:
            return self.asset_infos[item]
        if item in self.seq_impedances:
            return self.seq_impedances[item]
        if item in self.base_voltages:
            return self.base_voltages[item]
        if item in self.usage_points:
            return self.usage_points[item]
        if item in self.meters:
            return self.meters[item]
        raise KeyError(f"{item}")

    def get_meter(self, meter_mrid):
        try:
            return self.meters[meter_mrid]
        except KeyError:
            raise NoMeterException(f"{meter_mrid}")

    def get_base_voltage(self, bv_mrid):
        try:
            return self.base_voltages[bv_mrid]
        except KeyError:
            raise NoBaseVoltageException(f"{bv_mrid}")

    def get_asset_info(self, ai_mrid):
        try:
            return self.asset_infos[ai_mrid]
        except KeyError:
            raise NoAssetInfoException(f"{ai_mrid}")

    def get_plsi(self, plsi_mrid):
        try:
            return self.seq_impedances[plsi_mrid]
        except KeyError:
            raise NoPerLengthSeqImpException(f"{plsi_mrid}")

    def get_usage_point(self, up_mrid):
        try:
            return self.usage_points[up_mrid]
        except KeyError:
            raise NoUsagePointException(f"{up_mrid}")

    def get_customer(self, cust_mrid):
        try:
            return self.customers[cust_mrid]
        except KeyError:
            raise NoCustomerException(f"{cust_mrid}")

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
                t.upstream = upstream
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
                    terminal.upstream = upstream
                    upstream = not upstream
                    for term in conn_node:
                        if term.mrid in traced:
                            continue
                        if term != terminal:
                            if not term.equipment.connected():
                                continue
                            term.upstream = upstream
                            equips_to_trace.append(term.equipment)
                        # Don't trace over a terminal twice to stop us from reversing direction
                        traced.add(term.mrid)

    def _create_common_pb_fields(self, pb):
        """
        Creates common features of ConductingEquipment. No exceptions should be thrown from this function. It
        is more appropriate to return None/Empty if something fails.
        :param pb:
        :return:
        """
        terms = self.create_connectivity_nodes(pb.terminals)
        location = Location.from_pb(pb.location)
        diag_objs = DiagramObject.from_pbs(pb.diagramObjects)
        return terms, location, diag_objs

    def create_connectivity_nodes(self, pb_terminals):
        """
        Extract and create ConnectivityNode's from a set of protobuf Terminals.
        Order of the terminals is preserved and indicates their sequenceNumber
        :param pb_terminals: A list of protobuf Terminal's.
        :return: A set of CIM terminals.
        """
        terms = []
        for terminal in pb_terminals:
            conn_node = self.add_connectivity_node(terminal.connectivityNodeMRID)
            term = Terminal(terminal.mRID, terminal.phases, conn_node, terminal.name, connected=terminal.connected)
            conn_node.add_terminal(term)
            terms.append(term)
        return terms

    def add_connectivity_node(self, mrid):
        if mrid not in self.resources:
            node = ConnectivityNode(mrid)
            self.resources[mrid] = node
            return node
        else:
            return self.resources[mrid]

    def add_pb_base_voltage(self, pb_bv):
        bv = BaseVoltage.from_pb(pb_bv)
        self.base_voltages[bv.mrid] = bv

    def add_pb_per_length_sequence_impedance(self, pb_plsi):
        plsi = PerLengthSequenceImpedance.from_pb(pb_plsi)
        self.seq_impedances[plsi.mrid] = plsi

    def add_pb_asset_info(self, pb_ai):
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
        up = UsagePoint.from_pb(pb_up, self)
        self.usage_points[up.mrid] = up

    def add_pb_customer(self, pb_c):
        customer = Customer.from_pb(pb_c)
        self.customers[customer.mrid] = customer

    def add_pb_meter(self, pb_m):
        meter = Meter.from_pb(pb_m, self)
        self.meters[meter.mrid] = meter

    def add_pb_energy_source(self, pb_es):
        """
        Helper function to add an energy source to the network that has come through as a protobuf message
        :param pb_es:
        :return:
        """
        terms, location, diag_objs = self._create_common_pb_fields(pb_es)
        base_voltage = self.get_base_voltage(pb_es.baseVoltageMRID)

        self.add_energy_source(pb_es.mRID,
                               pb_es.name,
                               pb_es.activePower,
                               pb_es.r,
                               pb_es.x,
                               base_voltage,
                               pb_es.reactivePower,
                               pb_es.voltageAngle,
                               pb_es.voltageMagnitude,
                               pb_es.inService,
                               terms,
                               diag_objs,
                               location)

    def add_energy_source(self, mrid, name: str, active_power: float, r: float, x: float, base_volt: BaseVoltage,
                          reactive_power: float, voltage_angle: float, voltage_magnitude: float,
                          in_service: bool, terminals: List, diag_objs: List[DiagramObject] = None,
                          location: Location = None):
        self.resources[mrid] = EnergySource(mrid, active_power, r, x, base_volt, reactive_power, voltage_angle,
                                            voltage_magnitude, name=name,
                                            in_service=in_service, terminals=terminals, diag_objs=diag_objs,
                                            location=location)
        self.energy_sources[mrid] = self.resources[mrid]

    def add_pb_energy_consumer(self, pb_ec):
        base_voltage = self.get_base_voltage(pb_ec.baseVoltageMRID)
        terms, location, diag_objs = self._create_common_pb_fields(pb_ec)
        ecp = [EnergyConsumerPhase(con_phase.pfixed, con_phase.qfixed, con_phase.phase) for con_phase in pb_ec.energyConsumerPhases]

        self.add_energy_consumer(pb_ec.mRID,
                                 pb_ec.name,
                                 pb_ec.p,
                                 pb_ec.q,
                                 base_voltage,
                                 pb_ec.phaseConnection,
                                 pb_ec.inService,
                                 terms,
                                 ecp,
                                 diag_objs,
                                 location)

    def add_energy_consumer(self, mrid, name: str, p: float, q: float, base_volt: BaseVoltage, phase_shunt_con_kind,
                            in_service: bool,
                            terminals: List, phases: List[EnergyConsumerPhase], diag_objs: List[DiagramObject] = None,
                            location: Location = None):
        self.resources[mrid] = EnergyConsumer(mrid, p, q, phs_shunt_conn_kind=phase_shunt_con_kind,
                                              base_voltage=base_volt, ecp=phases,
                                              name=name, in_service=in_service, terminals=terminals,
                                              diag_objs=diag_objs,
                                              location=location)

    def add_pb_transformer(self, pb_tf):
        terms, location, diag_objs = self._create_common_pb_fields(pb_tf)
        ends = []
        for end in pb_tf.powerTransformerEnds:
            tap_changer = RatioTapChanger(end.ratioTapChanger.highStep, end.ratioTapChanger.lowStep, end.ratioTapChanger.step,
                                          end.ratioTapChanger.stepVoltageIncrement)
            ends.append(PowerTransformerEnd(end.ratedS, end.ratedU, end.r, end.x, end.r0, end.x0, end.connectionKind,
                                            tap_changer=tap_changer))

        self.add_transformer(pb_tf.mRID,
                             pb_tf.name,
                             pb_tf.vectorGroup,
                             pb_tf.inService,
                             terms,
                             ends,
                             diag_objs,
                             location)

    def add_transformer(self, mrid: str, name: str, vector_group: VectorGroup, in_service: bool, terminals: List,
                        transformer_ends: List[PowerTransformerEnd], diag_objs: List[DiagramObject] = None,
                        location: Location = None):
        self.resources[mrid] = PowerTransformer(mrid, vector_group, name=name, in_service=in_service, terminals=terminals,
                                                ends=transformer_ends, diag_objs=diag_objs, location=location)

    def add_pb_aclinesegment(self, pb_acls):
        """
        Add a Protobuf AcLineSegment
        :param pb_acls:
        :raises: a subclass of MissingReferenceException if any reference fields in the message are not already in the network.
        """
        terms, location, diag_objs = self._create_common_pb_fields(pb_acls)
        plsi = self.get_plsi(pb_acls.perLengthSequenceImpedanceMRID)
        base_voltage = self.get_base_voltage(pb_acls.baseVoltageMRID)
        wire_info = self.get_asset_info(pb_acls.assetInfoMRID)

        self.add_aclinesegment(pb_acls.mRID,
                               pb_acls.name,
                               plsi,
                               pb_acls.length,
                               base_voltage,
                               wire_info,
                               pb_acls.inService,
                               terms,
                               diag_objs,
                               location)

    def add_aclinesegment(self, mrid: str, name: str, plsi: PerLengthSequenceImpedance, length: float,
                          base_volt: BaseVoltage, wire_info: WireInfo,
                          in_service: bool, terminals: List, diag_objs: List[DiagramObject] = None,
                          location: Location = None):
        self.resources[mrid] = ACLineSegment(mrid, plsi, length, wire_info, base_voltage=base_volt, name=name,
                                             in_service=in_service, terminals=terminals, diag_objs=diag_objs,
                                             location=location)

    def add_pb_breaker(self, pb_br):
        terms, location, diag_objs = self._create_common_pb_fields(pb_br)
        base_voltage = self.get_base_voltage(pb_br.baseVoltageMRID)

        self.add_breaker(pb_br.mRID,
                         pb_br.name,
                         pb_br.open,
                         base_voltage,
                         pb_br.inService,
                         terms,
                         diag_objs,
                         location)

    def add_breaker(self, mrid: str, name: str, open_: bool, base_volt: BaseVoltage, in_service: bool, terminals: List,
                    diag_objs: List[DiagramObject] = None, location: Location = None):
        self.resources[mrid] = Breaker(mrid, open_, base_voltage=base_volt, name=name, in_service=in_service,
                                       terminals=terminals, diag_objs=diag_objs, location=location)

    def dumpTracing(self):
        with open(TRACED_NETWORK_FILE, "w") as f:
            for e in self.depth_first_trace_and_apply():
                assert len(e.terminals) < 3
                upstream_count = 0
                f.write(str(e) + "\n")
                for term in e.terminals:
                    if term.upstream:
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

    def pickle(self, path=None):
        if path is not None:
            with open(path, 'w') as f:
                pickle.dump(self, f)
        else:
            return pickle.dumps(self)

