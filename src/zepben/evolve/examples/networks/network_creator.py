from zepben.evolve import NetworkService, Junction, Terminal, PhaseCode, ConductingEquipment, EnergySource, \
    PowerTransformer, BaseVoltage, AcLineSegment, EnergyConsumer, PowerTransformerInfo, PowerTransformerEnd
from zepben.evolve.util import CopyableUUID


def create_ac_line_segment(network_service: NetworkService, bus1: Junction, bus2: Junction,
                           **kwargs) -> AcLineSegment:
    acls = AcLineSegment()
    _create_two_terminal_conducting_equipment(network_service=network_service, ce=acls, **kwargs)
    _connect_two_terminal_conducting_equipment(network_service=network_service, ce=acls, bus1=bus1, bus2=bus2)
    return acls


def create_two_winding_power_transformer(network_service: NetworkService, bus1: Junction, bus2: Junction,
                                         pt_info: PowerTransformerInfo, **kwargs) -> PowerTransformer:
    power_transformer = PowerTransformer(asset_info=PowerTransformerInfo())
    _create_two_terminal_conducting_equipment(network_service=network_service, ce=power_transformer, **kwargs)
    _connect_two_terminal_conducting_equipment(network_service=network_service, ce=power_transformer,
                                               bus1=bus1, bus2=bus2)
    # TODO: How to associated PowerTransformerEndInfo to a PowerTransformerInfo
    for i in range(1, 2):
        end = PowerTransformerEnd(power_transformer=power_transformer)
        power_transformer.add_end(end)
        end.terminal = power_transformer.get_terminal_by_sn(i)
    return power_transformer


def create_energy_consumer(net: NetworkService, bus: Junction, **kwargs) -> EnergyConsumer:
    ec = EnergyConsumer()
    _create_single_terminal_conducting_equipment(network_service=net, ce=ec, **kwargs)
    _connect_single_terminal_conducting_equipment(network_service=net, ce=ec, bus=bus)
    return ec


def create_energy_source(net: NetworkService, bus: Junction, **kwargs) -> EnergySource:
    es = EnergySource()
    _create_single_terminal_conducting_equipment(network_service=net, ce=es, bus=bus, **kwargs)
    _connect_single_terminal_conducting_equipment(network_service=net, ce=es, bus=bus)
    return es


def create_bus(network_service: NetworkService, base_voltage: BaseVoltage, **kwargs) -> Junction:
    bus = Junction(base_voltage=base_voltage)
    if 'mrid' not in kwargs:
        bus.mrid = str(CopyableUUID())
    network_service.add(bus)
    _create_terminals(ce=bus, network=network_service, **kwargs)
    # TODO: Figure out how to add Voltage to Buses - Looks like we need to add topologicalNode to support the
    #  relationship to BaseVoltage. Meanwhile using Junction.
    return bus


def _create_two_terminal_conducting_equipment(network_service: NetworkService,
                                              ce: ConductingEquipment, **kwargs):
    if 'mrid' not in kwargs:
        ce.mrid = str(CopyableUUID())
    network_service.add(ce)
    _create_terminals(ce=ce, num_terms=2, network=network_service, **kwargs)


def _connect_two_terminal_conducting_equipment(network_service: NetworkService, ce: ConductingEquipment,
                                               bus1: Junction, bus2: Junction):
    network_service.connect_terminals(bus1.get_terminal_by_sn(1), ce.get_terminal_by_sn(1))
    network_service.connect_terminals(bus2.get_terminal_by_sn(1), ce.get_terminal_by_sn(2))


def _create_single_terminal_conducting_equipment(network_service: NetworkService, ce: ConductingEquipment, **kwargs):
    if 'mrid' not in kwargs:
        ce.mrid = str(CopyableUUID())
    network_service.add(ce)
    _create_terminals(ce=ce, network=network_service)


def _connect_single_terminal_conducting_equipment(network_service: NetworkService, ce: ConductingEquipment,
                                                  bus: Junction):
    network_service.connect_terminals(ce.get_terminal_by_sn(1), bus.get_terminal_by_sn(1))


def _create_terminals(network: NetworkService, ce: ConductingEquipment,
                      num_terms: int = 1, phases: PhaseCode = PhaseCode.ABC, **kwargs):
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
