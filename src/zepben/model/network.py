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
from zepben.model.equipment import NoEquipmentException
from zepben.model import DiagramObjectPoints, PositionPoints, Terminal, RatioTapChanger
from zepben.model.connectivity_node import ConnectivityNode
from zepben.model.energy_consumer import EnergyConsumer, EnergyConsumerPhase
from zepben.model.energy_source import EnergySource
from zepben.model.aclinesegment import ACLineSegment
from zepben.model.power_transformer import PowerTransformer, PowerTransformerEnd
from zepben.model.switch import Breaker
from zepben.model.metrics_store import MetricsStore
from typing import List
from pprint import pformat
from pathlib import Path

logger = logging.getLogger(__name__)
TRACED_NETWORK_FILE = str(Path.home().joinpath(Path("traced.json")))


class NetworkQueryError(Exception):
    pass


def pos_points_from_pb(points):
    """
    Transform a list of protobuf position points to cimbiotic PositionPoints
    :param points:
    :return:
    """
    pos_points = []
    for point in points:
        pos_points.append(PositionPoints(point.xPosition, point.yPosition, point.sequenceNumber))
    return pos_points


class EquipmentContainer(object):
    """
    A full representation of the power network.
    Contains a map of equipment (string ID's -> Equipment/Nodes/etc)
    And a reverse map of equipment to terminals
    """

    def __init__(self, metrics_store: MetricsStore):
        """
        Represents a whole network. At the moment there's a single index on equipment ID's -> all types of equipment,
        as well as an index on energy source ID's -> energy sources.
        TODO: Split resources into a dictionary for each type and provide type based getter methods for each
              type - as well as a getter for when type is unknown.
        :param metrics_store: Storage for meter measurement data associated with this network.
        """
        self.resources = {}
        self.equipment_to_terminals = {}
        self.terminal_to_equipment = {}
        self.equipment_to_diagram_points = {}
        self.energy_sources = {}
        self.metrics_store = metrics_store

    def print_network(self):
        logger.info(f"Resources:\n{pformat(self.resources)}")
        logger.info(f"Unassociated terminals:\n{pformat(self.equipment_to_terminals)}")
        logger.info(f"Unassociated points:\n{pformat(self.equipment_to_diagram_points)}")

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

    def get_equipment(self, mrid):
        try:
            equip = self.resources[mrid]
            # Reconcile terminals with equipment - This should only occur once per equipment after it is created in the network
            if not equip.terminals:
                terms = self.equipment_to_terminals.get(equip.mrid, None)
                if terms:
                    equip.terminals = terms
                    for term in terms:
                        self.terminal_to_equipment[term.mrid] = equip
                    # No need to store the terminal separately anymore - it's been associated with its equipment, so we can delete the reference
                    del self.equipment_to_terminals[equip.mrid]
            if not equip.diagram_points:
                diag_points = self.equipment_to_diagram_points.get(equip.mrid, None)
                if diag_points:
                    equip.set_diagram_points(diag_points)
                    del self.equipment_to_diagram_points[equip.mrid]
        except KeyError as k:
            raise NoEquipmentException(f"No equipment with ID {mrid} found")

        return equip

    def create_connectivity_nodes(self, pb_terminals):
        """
        Extract and create ConnectivityNode's from a set of protobuf Terminals.
        :param pb_terminals: A list of protobuf Terminal's.
        :return: A set of CIM terminals.
        """
        terms = set()
        for terminal in pb_terminals:
            conn_node = self.add_connectivity_node(terminal.connectivityNode)
            term = Terminal(terminal.mRID, terminal.phases, conn_node, terminal.sequenceNumber, terminal.name, connected=terminal.connected)
            conn_node.add_terminal(term)
            terms.add(term)
        return terms

    def add_connectivity_node(self, mrid):
        if mrid not in self.resources:
            node = ConnectivityNode(mrid)
            self.resources[mrid] = node
            return node
        else:
            return self.resources[mrid]

    def _add_terms_to_map(self, terminals, equipment):
        for term in terminals:
            equip = self.terminal_to_equipment.get(term.mrid, None)
            if equip is None:
                self.terminal_to_equipment[term.mrid] = equipment
            elif equip.mrid == equipment.mrid:
                logger.debug(f"Terminal {term.mrid} was already mapped to {equip.__class__.__name__} {equip.mrid}")
            else:
                raise Exception(
                    f"Terminal {term.mrid} is already connected to {equip.mrid}. Cannot have a terminal with multiple connections.")

    def add_pb_energy_source(self, pb_es):
        """
        Helper function to add an energy source to the network that has come through as a protobuf message
        :param pb_es:
        :return:
        """
        terms = self.create_connectivity_nodes(pb_es.terminals)
        pos_points = pos_points_from_pb(pb_es.posPoints)
        self.add_energy_source(pb_es.mRID,
                               pb_es.name,
                               pb_es.activePower,
                               pb_es.r,
                               pb_es.x,
                               pb_es.nominalVoltage,
                               pb_es.reactivePower,
                               pb_es.voltageAngle,
                               pb_es.voltageMagnitude,
                               pb_es.inService,
                               terms,
                               pb_es.diagramPoints.xPosition,
                               pb_es.diagramPoints.yPosition,
                               pos_points)

    def add_energy_source(self, mrid, name: str, active_power: float, r: float, x: float, nominal_voltage: float,
                          reactive_power: float, voltage_angle: float, voltage_magnitude: float,
                          in_service: bool, terminals: set, x_pos: float = None, y_pos: float = None,
                          pos_points: List[PositionPoints] = None):
        diag_points = DiagramObjectPoints(x_pos, y_pos) if x_pos is not None and y_pos is not None else None
        self.resources[mrid] = EnergySource(mrid, active_power, r, x, nominal_voltage, reactive_power, voltage_angle,
                                            voltage_magnitude, name=name,
                                            in_service=in_service, terminals=terminals, diag_point=diag_points,
                                            pos_points=pos_points)
        self._add_terms_to_map(terminals, self.resources[mrid])
        self.energy_sources[mrid] = self.resources[mrid]

    def add_pb_energy_consumer(self, pb_ec):
        terms = self.create_connectivity_nodes(pb_ec.terminals)
        ecp = []
        for con_phase in pb_ec.energyConsumerPhase:
            ecp.append(EnergyConsumerPhase(con_phase.pfixed, con_phase.qfixed, con_phase.phase))

        pos_points = pos_points_from_pb(pb_ec.posPoints)
        self.add_energy_consumer(pb_ec.mRID,
                                 pb_ec.name,
                                 pb_ec.p,
                                 pb_ec.q,
                                 pb_ec.nominalVoltage,
                                 pb_ec.connectionKind,
                                 pb_ec.inService,
                                 terms,
                                 ecp,
                                 pb_ec.diagramPoints.xPosition,
                                 pb_ec.diagramPoints.yPosition,
                                 pos_points)

    def add_energy_consumer(self, mrid, name: str, p: float, q: float, nominal_voltage: float, phase_shunt_con_kind,
                            in_service: bool,
                            terminals: set, phases: List[EnergyConsumerPhase], x_pos: float = None, y_pos: float = None,
                            pos_points: List[PositionPoints] = None):
        diag_points = DiagramObjectPoints(x_pos, y_pos) if x_pos is not None and y_pos is not None else None
        self.resources[mrid] = EnergyConsumer(mrid, p, q, phs_shunt_conn_kind=phase_shunt_con_kind,
                                              nom_volts=nominal_voltage, ecp=phases,
                                              name=name, in_service=in_service, terminals=terminals,
                                              diag_point=diag_points,
                                              pos_points=pos_points)
        self._add_terms_to_map(terminals, self.resources[mrid])

    def add_pb_transformer(self, pb_tf):
        terms = self.create_connectivity_nodes(pb_tf.terminals)
        ends = []
        for end in pb_tf.ends:
            tap_changer = RatioTapChanger(end.tapChanger.highStep, end.tapChanger.lowStep, end.tapChanger.step,
                                          end.tapChanger.stepVoltageIncrement)
            r = end.r
            x = end.x
            r0 = end.r0
            x0 = end.x0
            if "r" not in end.mask.paths:
                r = None
            if "x" not in end.mask.paths:
                x = None
            if "r0" not in end.mask.paths:
                r0 = None
            if "x0" not in end.mask.paths:
                x0 = None
            ends.append(PowerTransformerEnd(end.ratedS, end.ratedU, r, x, r0, x0, end.connectionKind,
                                            end_number=end.endNumber, tap_changer=tap_changer))
        pos_points = pos_points_from_pb(pb_tf.posPoints)
        self.add_transformer(pb_tf.mRID,
                             pb_tf.name,
                             pb_tf.vectorGroup,
                             pb_tf.inService,
                             terms,
                             ends,
                             pb_tf.diagramPoints.xPosition,
                             pb_tf.diagramPoints.yPosition,
                             pos_points)

    def add_transformer(self, mrid: str, name: str, vector_group: float, in_service: bool, terminals: set,
                        transformer_ends: List[PowerTransformerEnd], x_pos: float = None, y_pos: float = None,
                        pos_points: List[PositionPoints] = None):
        diag_points = DiagramObjectPoints(x_pos, y_pos) if x_pos is not None and y_pos is not None else None
        self.resources[mrid] = PowerTransformer(mrid, vector_group, name=name, in_service=in_service,
                                                terminals=terminals,
                                                diag_point=diag_points, pos_points=pos_points)
        for end in transformer_ends:
            self.resources[mrid].add_end(end)
        self._add_terms_to_map(terminals, self.resources[mrid])

    def add_pb_aclinesegment(self, pb_acls):
        terms = self.create_connectivity_nodes(pb_acls.terminals)
        pos_points = pos_points_from_pb(pb_acls.posPoints)
        self.add_aclinesegment(pb_acls.mRID,
                               pb_acls.name,
                               pb_acls.r,
                               pb_acls.x,
                               pb_acls.r0,
                               pb_acls.x0,
                               pb_acls.length,
                               pb_acls.nominalVoltage,
                               pb_acls.ratedCurrent,
                               pb_acls.inService,
                               terms,
                               pb_acls.diagramPoints.xPosition,
                               pb_acls.diagramPoints.yPosition,
                               pos_points)

    def add_aclinesegment(self, mrid: str, name: str, r: float, x: float, r0: float, x0: float, length: float,
                          nominal_voltage: float, rated_current: float,
                          in_service: bool, terminals: set, x_pos: float = None, y_pos: float = None,
                          pos_points: List[PositionPoints] = None):
        diag_points = DiagramObjectPoints(x_pos, y_pos) if x_pos is not None and y_pos is not None else None
        self.resources[mrid] = ACLineSegment(mrid, r, x, r0, x0, length, rated_current, nom_volts=nominal_voltage, name=name,
                                             in_service=in_service, terminals=terminals, diag_point=diag_points,
                                             pos_points=pos_points)
        self._add_terms_to_map(terminals, self.resources[mrid])

    def add_pb_breaker(self, pb_br):
        terms = self.create_connectivity_nodes(pb_br.terminals)
        pos_points = pos_points_from_pb(pb_br.posPoints)
        self.add_breaker(pb_br.mRID,
                         pb_br.name,
                         pb_br.open,
                         pb_br.nominalVoltage,
                         pb_br.inService,
                         terms,
                         pb_br.diagramPoints.xPosition,
                         pb_br.diagramPoints.yPosition,
                         pos_points)

    def add_breaker(self, mrid: str, name: str, open_: bool, nominal_voltage: float, in_service: bool, terminals: set,
                    x_pos: float = None, y_pos: float = None, pos_points: List[PositionPoints] = None):
        diag_points = DiagramObjectPoints(x_pos, y_pos) if x_pos is not None and y_pos is not None else None
        self.resources[mrid] = Breaker(mrid, open_, nom_volts=nominal_voltage, name=name, in_service=in_service,
                                       terminals=terminals, diag_point=diag_points, pos_points=pos_points)
        self._add_terms_to_map(terminals, self.resources[mrid])

    def add_diagram_object_point(self, connected_mrid: str, x_pos: float, y_pos: float):
        equip = self.resources.get(connected_mrid, None)
        diag_point = DiagramObjectPoints(x_pos, y_pos)
        # If the equipment doesn't already exist, we save the point separately in our equip -> point map to look up later
        if equip is None:
            self.equipment_to_diagram_points[connected_mrid] = diag_point
        else:
            # Otherwise add the reference directly to the connected equip
            equip.set_diagram_points(diag_point)

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

