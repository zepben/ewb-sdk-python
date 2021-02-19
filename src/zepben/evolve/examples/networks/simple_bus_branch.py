from collections import defaultdict

from zepben.evolve import NetworkService, DiagramService, Diagram, \
    DiagramStyle, BaseVoltage, PositionPoint, Location, Feeder, EnergySource, PowerTransformerInfo, DiagramObject, \
    AcLineSegment, DiagramObjectStyle, IdentifiedObject, ConductingEquipment, Junction, EnergyConsumer, PowerTransformer


class SimpleBusBranch:

    def __init__(self):
        # Create empty network
        self.network_service: NetworkService = NetworkService()
        self.diagram_service: DiagramService = DiagramService()
        self.diagram: Diagram = Diagram(diagram_style=DiagramStyle.GEOGRAPHIC)
        self.create_network()
        self._add_diagram()

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
        # Create location for the Line
        line_location = Location().add_point(point1).add_point(point2)
        self.network_service.add(line_location)
        # Create Line
        self.network_service.create_ac_line_segment(bus1=b1, bus2=b2, name="Line", location=line_location,
                                                    length=100., base_voltage=bv_lv)

    def _add_diagram(self):
        self.diagram_service.add(self.diagram)
        self._add_diagram_objects()
        # TODO: In ?voltages geo view the acls does not appear.

    def _add_diagram_objects(self):
        # Add DiagramObject for ConductingEquipments
        ce_list = self.network_service.objects(ConductingEquipment)
        for ce in ce_list:
            diagram_object_mapping = defaultdict(
                lambda: DiagramObject(identified_object_mrid=ce.mrid, style=DiagramObjectStyle.JUNCTION,
                                      diagram=self.diagram))
            diagram_object_mapping[Junction] = DiagramObject(identified_object_mrid=ce.mrid,
                                                             style=DiagramObjectStyle.JUNCTION,
                                                             diagram=self.diagram)
            diagram_object_mapping[EnergySource] = DiagramObject(identified_object_mrid=ce.mrid,
                                                                 style=DiagramObjectStyle.ENERGY_SOURCE,
                                                                 diagram=self.diagram)
            diagram_object_mapping[EnergyConsumer] = DiagramObject(identified_object_mrid=ce.mrid,
                                                                   style=DiagramObjectStyle.USAGE_POINT,
                                                                   diagram=self.diagram)
            diagram_object_mapping[PowerTransformer] = DiagramObject(identified_object_mrid=ce.mrid,
                                                                     style=DiagramObjectStyle.DIST_TRANSFORMER,
                                                                     diagram=self.diagram)
            # diagram_object_mapping[AcLineSegment] = self._add_diagram_objects_to_ac_line_segment(ce)
            diagram_object: DiagramObject = diagram_object_mapping[type(ce)]
            self.diagram.add_object(diagram_object)
            self.diagram_service.add(diagram_object)

    def _add_diagram_objects_to_ac_line_segment(self, ac_line_segment: AcLineSegment):
        # Create DiagramObject for AcLineSegments
        # diagram_object = DiagramObject(mrid = ac_line_segment.mrid + "-do",
        # = acLineSegment.mRID; style = DiagramObjectStyle.CONDUCTOR_LV; diagram = diagram}
        diagram_object = DiagramObject()
        diagram_object.mrid = ac_line_segment.mrid + "-do"
        diagram_object.style = DiagramObjectStyle.CONDUCTOR_LV
        # diagram_object.diagram =
        # point1 = ac_line_segment.location.get_point(0)
        # point2 = ac_line_segment.location.get_point(1)
        # diagram_object.addPoint(DiagramObjectPoint(xPosition = point1.xPosition, yPosition = point1.yPosition))
        # diagramObject.addPoint(DiagramObjectPoint(xPosition = point2.xPosition, yPosition = point2.yPosition))
        return diagram_object


SimpleBusBranch()
