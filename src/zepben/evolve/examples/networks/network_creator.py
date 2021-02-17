from zepben.evolve import NetworkService, Junction, Terminal, PhaseCode, ConductingEquipment, EnergySource, \
    PowerTransformer, BaseVoltage, AcLineSegment, EnergyConsumer, PowerTransformerInfo, PowerTransformerEnd
from zepben.evolve.util import CopyableUUID


def create_ac_line_segment(network_service: NetworkService, bus1: Junction, bus2: Junction,
                           **kwargs) -> AcLineSegment:
    acls = AcLineSegment()
    _create_two_terminal_conducting_equipment(network_service=network_service, ce=acls, bus1=bus1, bus2=bus2, **kwargs)
    return acls


def create_two_winding_power_transformer(network_service: NetworkService, bus1: Junction, bus2: Junction,
                                         pt_info: PowerTransformerInfo, **kwargs) -> PowerTransformer:
    power_transformer = PowerTransformer()
    _create_two_terminal_conducting_equipment(network_service=network_service, ce=power_transformer,
                                              bus1=bus1, bus2=bus2, **kwargs)
    # TODO: power_transformer = PowerTransformer(power_transformer_info = PowerTransformerInfo())
    # TODO: Add _connectBuses(bus1, bus2)
    for i in range(1, 2):
        end = PowerTransformerEnd(power_transformer=power_transformer)
        power_transformer.add_end(end)
        end.terminal = power_transformer.get_terminal_by_sn(i)
    return power_transformer


def create_energy_consumer(network_service: NetworkService, bus: Junction, **kwargs) -> EnergyConsumer:
    ec = EnergyConsumer()
    _create_single_terminal_conducting_equipment(network_service=network_service, ce=ec)
    # TODO: Connect to bus
    return ec


def create_energy_source(network_service: NetworkService, bus: Junction, **kwargs) -> EnergySource:
    es = EnergySource()
    _create_single_terminal_conducting_equipment(network_service=network_service, ce=es)
    # TODO: Connect to bus
    return es


def create_bus(network_service: NetworkService, base_voltage: BaseVoltage, **kwargs) -> Junction:
    bus = Junction(base_voltage=base_voltage)
    _create_single_terminal_conducting_equipment(network_service=network_service, ce=bus, **kwargs)
    # TODO: Figure out how to add Voltage to Buses - Looks like we need to add topologicalNode to support the
    #  relationship to BaseVoltage. Meanwhile using Junction.
    return bus


def _create_two_terminal_conducting_equipment(network_service: NetworkService,
                                              ce: ConductingEquipment, bus1: Junction, bus2: Junction, **kwargs):
    if 'mrid' not in kwargs:
        ce.mrid = str(CopyableUUID())
    network_service.add(ce)
    _create_terminals(ce=ce, num_terms=2, network=network_service, **kwargs)


def _create_single_terminal_conducting_equipment(network_service: NetworkService, ce: ConductingEquipment,
                                                 bus: Junction = None, **kwargs):
    if 'mrid' not in kwargs:
        ce.mrid = str(CopyableUUID())
    network_service.add(ce)
    _create_terminals(ce=ce, network=network_service, **kwargs)


def _create_terminals(network: NetworkService, ce: ConductingEquipment,
                      num_terms: int = 1, phases: PhaseCode = PhaseCode.ABC, **kwargs):
    for i in range(1, num_terms + 1):
        terminal: Terminal = Terminal(mrid=f"{ce.mrid}_t{i}", conducting_equipment=ce, phases=phases, sequence_number=i)
        ce.add_terminal(terminal)
        network.add(terminal)
        terminal.conducting_equipment = ce


# TODO: How to associated PowerTrandformerEndInfo to a PowerTranformerInfo

NetworkService.create_bus = create_bus
NetworkService.create_energy_source = create_energy_source
NetworkService.create_two_winding_power_transformer = create_two_winding_power_transformer
NetworkService.create_ac_line_segment = create_ac_line_segment
NetworkService.create_energy_consumer = create_energy_consumer
