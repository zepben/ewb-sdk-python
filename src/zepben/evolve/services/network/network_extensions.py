#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.wires.connectors import Junction
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer
from zepben.evolve.model.cim.iec61970.base.wires.switch import Breaker
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.evolve.util import CopyableUUID

__all__ = ["create_ac_line_segment", "create_two_winding_power_transformer", "create_energy_consumer",
           "create_energy_source", "create_bus", "create_breaker"]


# !! WARNING !! #
# THIS CODE IS IN ACTIVE DEVELOPMENT, UNSTABLE, AND LIKELY TO HAVE ISSUES. FOR EXPERIMENTATION ONLY.

def create_ac_line_segment(network_service: NetworkService, cn1: ConnectivityNode, cn2: ConnectivityNode,
                           **kwargs) -> AcLineSegment:
    acls = AcLineSegment(**kwargs)
    _create_two_terminal_conducting_equipment(network_service=network_service, ce=acls)
    _connect_two_terminal_conducting_equipment(network_service=network_service, ce=acls, cn1=cn1, cn2=cn2)
    return acls


def create_two_winding_power_transformer(network_service: NetworkService, cn1: ConnectivityNode, cn2: ConnectivityNode,
                                         **kwargs) -> PowerTransformer:
    power_transformer = PowerTransformer(**kwargs)
    _create_two_terminal_conducting_equipment(network_service=network_service, ce=power_transformer, **kwargs)
    _connect_two_terminal_conducting_equipment(network_service=network_service, ce=power_transformer, cn1=cn1, cn2=cn2)
    # TODO: How to associated PowerTransformerEndInfo to a PowerTransformerInfo
    for i in range(1, 2):
        end = PowerTransformerEnd(power_transformer=power_transformer)
        power_transformer.add_end(end)
        end.terminal = power_transformer.get_terminal_by_sn(i)
    return power_transformer


def create_energy_consumer(net: NetworkService, cn: ConnectivityNode, **kwargs) -> EnergyConsumer:
    ec = EnergyConsumer(**kwargs)
    _create_single_terminal_conducting_equipment(network_service=net, ce=ec, **kwargs)
    _connect_single_terminal_conducting_equipment(network_service=net, ce=ec, cn=cn)
    return ec


def create_energy_source(net: NetworkService, cn: ConnectivityNode, **kwargs) -> EnergySource:
    es = EnergySource(**kwargs)
    _create_single_terminal_conducting_equipment(network_service=net, ce=es, cn=cn, **kwargs)
    _connect_single_terminal_conducting_equipment(network_service=net, ce=es, cn=cn)
    return es


def create_breaker(network_service: NetworkService, cn1: ConnectivityNode, cn2: ConnectivityNode, **kwargs) -> Breaker:
    ce = Breaker(**kwargs)
    _create_two_terminal_conducting_equipment(network_service=network_service, ce=ce, **kwargs)
    _connect_two_terminal_conducting_equipment(network_service=network_service, ce=ce, cn1=cn1, cn2=cn2)
    return ce


def create_bus(network_service: NetworkService, **kwargs) -> Junction:
    bus = Junction(**kwargs)
    if 'mrid' not in kwargs:
        bus.mrid = str(CopyableUUID())
    network_service.add(bus)
    _create_terminals(ce=bus, network=network_service)
    # TODO: Figure out how to add Voltage to Buses - Looks like we need to add topologicalNode to support the
    #  relationship to BaseVoltage. Meanwhile using Junction.
    return bus


def _create_two_terminal_conducting_equipment(network_service: NetworkService, ce: ConductingEquipment, **kwargs):
    if 'mrid' not in kwargs:
        ce.mrid = str(CopyableUUID())
    network_service.add(ce)
    _create_terminals(ce=ce, num_terms=2, network=network_service)


def _connect_two_terminal_conducting_equipment(network_service: NetworkService, ce: ConductingEquipment,
                                               cn1: ConnectivityNode, cn2: ConnectivityNode):
    network_service.connect_by_mrid(ce.get_terminal_by_sn(1), cn1.mrid)
    network_service.connect_by_mrid(ce.get_terminal_by_sn(2), cn2.mrid)


def _create_single_terminal_conducting_equipment(network_service: NetworkService, ce: ConductingEquipment, **kwargs):
    if 'mrid' not in kwargs:
        ce.mrid = str(CopyableUUID())
    network_service.add(ce)
    _create_terminals(ce=ce, network=network_service)


def _connect_single_terminal_conducting_equipment(network_service: NetworkService, ce: ConductingEquipment,
                                                  cn: ConnectivityNode):
    network_service.connect_by_mrid(ce.get_terminal_by_sn(1), cn.mrid)


def _create_terminals(network: NetworkService, ce: ConductingEquipment, num_terms: int = 1,
                      phases: PhaseCode = PhaseCode.ABC):
    for i in range(1, num_terms + 1):
        terminal: Terminal = Terminal(mrid=f"{ce.mrid}_t{i}", conducting_equipment=ce, phases=phases, sequence_number=i)
        ce.add_terminal(terminal)
        network.add(terminal)
        terminal.conducting_equipment = ce


NetworkService.create_bus = create_bus
NetworkService.create_energy_source = create_energy_source
NetworkService.create_two_winding_power_transformer = create_two_winding_power_transformer
NetworkService.create_ac_line_segment = create_ac_line_segment
NetworkService.create_energy_consumer = create_energy_consumer
NetworkService.create_breaker = create_breaker
