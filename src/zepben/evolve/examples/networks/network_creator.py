from zepben.evolve import NetworkService, Junction, Terminal, BaseVoltage


def create_bus(net: NetworkService, bv: BaseVoltage):
    # TODO: Figure out how to add Voltage to Buses - Looks like we need to add topologicalNode to support the
    #  relationship to BaseVoltage. Meanwhile using Junction.
    bus = Junction(base_voltage=bv)
    t = Terminal()
    net.add(bus)
    net.add(bv)
    net.add(t)
    t.conducting_equipment = bus
    bus.add_terminal(t)
    return bus


NetworkService.create_bus = create_bus
