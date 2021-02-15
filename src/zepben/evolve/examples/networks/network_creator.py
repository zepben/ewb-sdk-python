from zepben.evolve import NetworkService, Junction, Terminal, BaseVoltage, PhaseCode, ConductingEquipment
from zepben.evolve.util import CopyableUUID
import zepben.evolve as evolve


def create_bus(net: NetworkService, bv: BaseVoltage) -> Junction:
    # TODO: Figure out how to add Voltage to Buses - Looks like we need to add topologicalNode to support the
    #  relationship to BaseVoltage. Meanwhile using Junction.
    bus: Junction = Junction()
    bus.base_voltage = bv
    t = Terminal()
    net.add(bus)
    net.add(bv)
    net.add(t)
    t.conducting_equipment = bus
    bus.add_terminal(t)
    return bus


def _creator(class_name, service: NetworkService, **kwargs) -> ConductingEquipment:
    class_ = getattr(evolve, class_name)
    ce = class_()
    if 'mrid' not in kwargs:
        ce.mrid = str(CopyableUUID())
    service.add(ce)
    create_terminals(ce=ce, network=service, **kwargs)
    return ce


def create_terminals(network: NetworkService, ce: ConductingEquipment,
                     num_terms: int = 1, phases: PhaseCode = PhaseCode.ABC):
    for i in range(1, num_terms + 1):
        terminal = Terminal(mrid=f"{ce.mrid}_t{i}", conducting_equipment=ce, phases=phases, sequence_number=i)
        ce.add_terminal(terminal)
        network.add(terminal)


def create_source_for_connecting(network: NetworkService): return _creator(service=network, class_name="EnergySource")


NetworkService.create_bus = create_bus
NetworkService.create_source_for_connecting = create_source_for_connecting
