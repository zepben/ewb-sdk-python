from zepben.evolve import NetworkService, Junction, Terminal

class NetworkService(NetworkService):
    def createBus(self, bv):
        # TODO: Figure out how to add Voltage to Buses - Looks like we need to add topologicalNode to support the relationship to BaseVoltage. Meanwhile using Junction.
        bus = Junction()
        t  = Terminal()
        self.add(bus)
        self.add(bv)
        self.add(t)
        t.conducting_equipment = bus
        bus.add_terminal(t)
        return bus
