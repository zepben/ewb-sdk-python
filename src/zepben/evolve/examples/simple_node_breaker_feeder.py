#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import NetworkService, DiagramService, Diagram, DiagramStyle, BaseVoltage, PositionPoint, Location, Feeder, EnergySource, \
    PowerTransformerInfo, DiagramObject, AcLineSegment, ConductingEquipment, Junction, EnergyConsumer, PowerTransformer, DiagramObjectPoint, ConnectivityNode

__all__ = ["SimpleNodeBreakerFeeder"]


class SimpleNodeBreakerFeeder:

    def __init__(self, breaker_is_open=False):
        self.breaker_is_open = breaker_is_open
        self.network_service: NetworkService = NetworkService()
        self.diagram_service: DiagramService = DiagramService()
        self.diagram: Diagram = Diagram(diagram_style=DiagramStyle.GEOGRAPHIC)
        self._create_network_service()
        self._create_diagram_service()

    def _create_network_service(self):
        # Create BaseVoltages
        # noinspection PyArgumentList
        bv_hv: BaseVoltage = BaseVoltage(mrid="20kV", nominal_voltage=20000, name="20kV")
        # noinspection PyArgumentList
        bv_lv: BaseVoltage = BaseVoltage(mrid="415V", nominal_voltage=3000, name="415V")
        self.network_service.add(bv_hv)
        self.network_service.add(bv_lv)
        # Create Locations for buses
        # noinspection PyArgumentList
        point1 = PositionPoint(x_position=149.12791965570293, y_position=-35.277592101000934)
        # noinspection PyArgumentList
        point2 = PositionPoint(x_position=149.12779472660375, y_position=-35.278183862759285)
        loc1 = Location().add_point(point1)
        loc2 = Location().add_point(point2)
        # Create connectivity_nodes
        cn1 = ConnectivityNode(name="cn1")
        cn2 = ConnectivityNode(name="cn2")
        cn3 = ConnectivityNode(name="cn3")
        cn4 = ConnectivityNode(name="cn4")
        # Create EnergySource
        # noinspection PyUnresolvedReferences
        energy_source: EnergySource = self.network_service.create_energy_source(cn=cn1, base_voltage=bv_hv,
                                                                                voltage_magnitude=1.02 * bv_hv.nominal_voltage,
                                                                                name="Grid Connection", location=loc1)
        # TODO: Replace  createEnergySource with creation of EquivalentInjection
        # Create Feeder
        fdr = Feeder(normal_head_terminal=energy_source.get_terminal_by_sn(1))
        self.network_service.add(fdr)
        # Create Transformer
        # noinspection PyUnresolvedReferences
        self.network_service.create_two_winding_power_transformer(cn1=cn1, cn2=cn2, name="Trafo", location=loc1,
                                                                  asset_info=PowerTransformerInfo())
        # TODO: Associate the PowerTransformerInfo() to th PowerTransformer instance
        # TODO: Add ptInfo= self.network_service.getAvailablePowerTransformerInfo("0.4 MVA 20/0.4 kV")
        # Create Breaker
        # noinspection PyUnresolvedReferences
        breaker = self.network_service.create_breaker(cn1=cn2, cn2=cn3, base_voltage=bv_lv)
        breaker.set_open(self.breaker_is_open)
        # Create location for the Line
        line_location = Location().add_point(point1).add_point(point2)
        self.network_service.add(line_location)
        # Create Line
        # noinspection PyUnresolvedReferences
        self.network_service.create_ac_line_segment(cn1=cn3, cn2=cn4, name="Line",
                                                    length=100., base_voltage=bv_lv,
                                                    location=line_location)
        # Create EnergyConsumer
        # noinspection PyUnresolvedReferences
        self.network_service.create_energy_consumer(cn=cn3, p=100000., q=50000., name="Load",
                                                    location=loc2,
                                                    base_voltage=bv_lv)

    def _create_diagram_service(self):
        self.diagram_service.add(self.diagram)
        self._add_diagram_objects()
        # TODO: In ?voltages geo view the acls does not appear.

    def _add_diagram_objects(self):
        # Add DiagramObject for ConductingEquipments
        ce_list = self.network_service.objects(ConductingEquipment)
        for ce in ce_list:
            # diagram_object_mapping = defaultdict(
            #     lambda: DiagramObject(identified_object_mrid=ce.mrid, style="JUNCTION",
            #                           diagram=self.diagram))
            if isinstance(ce, Junction):
                diagram_object = DiagramObject(identified_object_mrid=ce.mrid,
                                               style="JUNCTION",
                                               diagram=self.diagram)
            elif isinstance(ce, EnergySource):
                diagram_object = DiagramObject(identified_object_mrid=ce.mrid,
                                               style="ENERGY_SOURCE",
                                               diagram=self.diagram)
            elif isinstance(ce, EnergyConsumer):
                diagram_object = DiagramObject(identified_object_mrid=ce.mrid,
                                               style="USAGE_POINT",
                                               diagram=self.diagram)
            elif isinstance(ce, PowerTransformer):
                diagram_object = DiagramObject(identified_object_mrid=ce.mrid,
                                               style="DIST_TRANSFORMER",
                                               diagram=self.diagram)

            elif isinstance(ce, AcLineSegment):
                diagram_object = self._add_diagram_objects_to_ac_line_segment(ce)
            else:
                diagram_object = DiagramObject(identified_object_mrid=ce.mrid,
                                               style="JUNCTION",
                                               diagram=self.diagram)
            self.diagram.add_diagram_object(diagram_object)
            self.diagram_service.add(diagram_object)

    def _add_diagram_objects_to_ac_line_segment(self, ac_line_segment: AcLineSegment):
        # Create DiagramObject for AcLineSegments
        diagram_object = DiagramObject(diagram=self.diagram)
        diagram_object.mrid = ac_line_segment.mrid + "-do"
        diagram_object.style = "CONDUCTOR_LV"
        diagram_object.diagram = self.diagram
        for position_point in ac_line_segment.location.points:
            # noinspection PyArgumentList
            diagram_point = DiagramObjectPoint(x_position=position_point.x_position,
                                               y_position=position_point.y_position)
            diagram_object.add_point(diagram_point)
        return diagram_object
