from zepben.evolve import NetworkService, DiagramService, Diagram, \
    DiagramStyle, BaseVoltage, PositionPoint, Location, Feeder, EnergySource, PowerTransformerInfo


class SimpleBusBranch:

    def __init__(self):
        # Create empty network
        self.network_service: NetworkService = NetworkService()
        self.diagram_service: DiagramService = DiagramService()
        self.diagram: Diagram = Diagram(diagram_style=DiagramStyle.GEOGRAPHIC)
        self.create_network()

    def create_network(self):
        # Create BaseVoltages
        bv_hv: BaseVoltage = BaseVoltage(mrid="20kV", nominal_voltage=20000, name="20kV")
        bv_lv: BaseVoltage = BaseVoltage(mrid="415V", nominal_voltage=3000, name="415V")
        self.network_service.add(bv_hv)
        self.network_service.add(bv_lv)
        # Create Locations for buses
        point1 = PositionPoint(x_position=149.12791965570293, y_position=-35.277592101000934)
        point2 = PositionPoint(x_position=149.12779472660375, y_position=-35.278183862759285)
        loc1 = Location().add_point(point1)
        loc2 = Location().add_point(point2)
        # Create buses
        b1 = self.network_service.create_bus(base_voltage=bv_hv, name="Bus 1", location=loc1)
        b2 = self.network_service.create_bus(base_voltage=bv_lv, name="Bus 2", location=loc1)
        b3 = self.network_service.create_bus(base_voltage=bv_lv, name="Bus 3", location=loc2)
        # Create EnergySource
        energy_source: EnergySource = self.network_service.create_energy_source(bus=b1,
                                                                                voltage_magnitude=1.02 * bv_hv.nominal_voltage,
                                                                                name="Grid Connection", location=loc1)
        # TODO: Replace  createEnergySource with creation of EquivalentInjection
        # Create Feeder
        fdr = Feeder(normal_head_terminal=energy_source.get_terminal_by_sn(1))
        self.network_service.add(fdr)
        # Create EnergyConsumer
        self.network_service.create_energy_consumer(bus=b3, p=100000., q=50000., name="Load", location=loc2)
        # Create Transformer
        self.network_service.create_two_winding_power_transformer(bus1=b1, bus2=b2, name="Trafo", location=loc1,
                                                                  pt_info=PowerTransformerInfo())
        # TODO: Associate the PowerTransformerInfo() to th PowerTransformer instance
        # TODO: Add ptInfo= self.network_service.getAvailablePowerTransformerInfo("0.4 MVA 20/0.4 kV")


SimpleBusBranch()
