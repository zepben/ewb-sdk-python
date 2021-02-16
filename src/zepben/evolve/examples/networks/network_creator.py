from zepben.evolve import NetworkService, Junction, Terminal, PhaseCode, ConductingEquipment, EnergySource
from zepben.evolve.util import CopyableUUID


def create_energy_source(network_service: NetworkService, bus: Junction, **kwargs) -> EnergySource:
    es = EnergySource()
    _create_conducting_equipment(network_service=network_service, ce=es)
    return es


def create_bus(network_service: NetworkService, **kwargs) -> Junction:
    bus = Junction()
    _create_conducting_equipment(network_service=network_service, ce=bus, **kwargs)
    # TODO: Figure out how to add Voltage to Buses - Looks like we need to add topologicalNode to support the
    #  relationship to BaseVoltage. Meanwhile using Junction.
    return bus


def _create_conducting_equipment(network_service: NetworkService, ce: ConductingEquipment, bus: Junction = None,
                                 **kwargs):
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


NetworkService.create_bus = create_bus
NetworkService.create_energy_source = create_energy_source
