#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from typing import TypeVar, Type, Optional

from hypothesis import assume

from zepben.evolve import MetadataCollection, NetworkService, DiagramService, CustomerService, MeasurementService, NameType, Organisation, DataSource, \
    IdentifiedObject, EnergyConsumerPhase, EnergyConsumer, EnergySourcePhase, EnergySource, BaseService, PowerTransformerInfo, TransformerEndInfo, \
    TransformerTankInfo, Asset, Pole, Streetlight, OrganisationRole, Customer, CustomerAgreement, PricingStructure, EndDevice, UsagePoint, \
    OperationalRestriction, AuxiliaryEquipment, ConductingEquipment, ConnectivityNode, Equipment, EquipmentContainer, Feeder, GeographicalRegion, Name, \
    PowerSystemResource, SubGeographicalRegion, Substation, Terminal, Diagram, DiagramObject, Control, Measurement, RemoteControl, RemoteSource, \
    PowerElectronicsUnit, AcLineSegment, Conductor, PowerElectronicsConnection, PowerElectronicsConnectionPhase, PowerTransformer, PowerTransformerEnd, \
    RatioTapChanger, ShuntCompensator, TransformerEnd, TransformerStarImpedance, Circuit, Loop, StreetAddress, LvFeeder, ProtectedSwitch, \
    CurrentTransformer, PotentialTransformer, Breaker, RegulatingCondEq, RegulatingControl, ProtectionRelayFunction, Sensor, ProtectionRelayScheme, \
    ProtectionRelaySystem, Fuse

T = TypeVar("T", bound=IdentifiedObject)


class Services(object):
    metadata_collection: MetadataCollection
    network_service: NetworkService
    diagram_service: DiagramService
    customer_service: CustomerService
    measurement_service: MeasurementService

    def __init__(self):
        self.metadata_collection = MetadataCollection()
        self.network_service = NetworkService()
        self.diagram_service = DiagramService()
        self.customer_service = CustomerService()
        self.measurement_service = MeasurementService()


def assume_non_blank_street_address_details(address: Optional[StreetAddress]):
    assume(not address or (not address.town_detail.all_fields_null_or_empty() and not address.street_detail.all_fields_empty()))


class SchemaNetworks:

    @staticmethod
    def create_name_test_services() -> Services:
        services = Services()
        # noinspection PyArgumentList
        name_type = NameType(name="type1")
        name_type.description = "type description"

        org = Organisation(mrid="org1")
        org.add_name(name_type.get_or_add_name("name1", org))
        services.network_service.add(org)

        services.network_service.add_name_type(name_type)

        # noinspection PyArgumentList
        name_type = NameType(name="type1")
        name_type.description = "type description"

        org = Organisation(mrid="org1")
        org.add_name(name_type.get_or_add_name("name1", org))
        services.customer_service.add(org)

        services.customer_service.add_name_type(name_type)

        # noinspection PyArgumentList
        name_type = NameType(name="type1")
        name_type.description = "type description"

        services.diagram_service.add_name_type(name_type)

        return services

    @staticmethod
    def create_data_source_test_services() -> Services:
        services = Services()
        # noinspection PyArgumentList
        services.metadata_collection.add(DataSource("source1", "v1", datetime(1970, 1, 1)))
        # noinspection PyArgumentList
        services.metadata_collection.add(DataSource("source2", "v2", datetime.now()))

        return services

    def customer_services_of(self, factory: Type[T], filled: T) -> Services:
        services = Services()
        services.customer_service.add(factory("empty"))
        self._add_with_references(filled, services.customer_service)

        # Copy items to other services that get auto loaded there.
        for org in services.customer_service.objects(Organisation):
            services.network_service.add(org)

        for name_type in services.customer_service.name_types:
            # noinspection PyArgumentList
            nt = NameType(name=name_type.name)
            nt.description = name_type.description

            for name in filter(lambda it: it.identified_object is Organisation, name_type.names):
                nt.get_or_add_name(name.name, name.identified_object)

            services.network_service.add_name_type(nt)

            # noinspection PyArgumentList
            nt = NameType(name=name_type.name)
            nt.description = name_type.description
            services.diagram_service.add_name_type(nt)

        return services

    def diagram_services_of(self, factory: Type[T], filled: T) -> Services:
        services = Services()
        services.diagram_service.add(factory("empty"))
        self._add_with_references(filled, services.diagram_service)

        # Copy items to other services that get auto loaded there.
        for name_type in services.diagram_service.name_types:
            # noinspection PyArgumentList
            nt = NameType(name=name_type.name)
            nt.description = name_type.description
            services.customer_service.add_name_type(nt)

            # noinspection PyArgumentList
            nt = NameType(name=name_type.name)
            nt.description = name_type.description
            services.network_service.add_name_type(nt)

        return services

    def network_services_of(self, factory: Type[T], filled: T) -> Services:
        services = Services()
        services.network_service.add(self._fill_required(services.network_service, factory("empty")))

        filled.mrid = "filled"
        self._add_with_references(filled, services.network_service)

        # Not yet supported
        # traces.set_phases().run(services.network_service)

        # Copy items to other services that get auto loaded there.
        for org in services.network_service.objects(Organisation):
            services.customer_service.add(org)

        for name_type in services.network_service.name_types:
            # noinspection PyArgumentList
            nt = NameType(name=name_type.name)
            nt.description = name_type.description

            for name in filter(lambda it: it.identified_object is Organisation, name_type.names):
                nt.get_or_add_name(name.name, name.identified_object)

            services.customer_service.add_name_type(nt)

            # noinspection PyArgumentList
            nt = NameType(name=name_type.name)
            nt.description = name_type.description
            services.diagram_service.add_name_type(nt)

        return services

    @staticmethod
    def _fill_required(service: NetworkService, io: T) -> T:
        if isinstance(io, EnergyConsumerPhase):
            ec = EnergyConsumer()
            ec.add_phase(io)
            service.add(ec)
            io.energy_consumer = ec
        elif isinstance(io, EnergySourcePhase):
            es = EnergySource()
            es.add_phase(io)
            service.add(es)
            io.energy_source = es

        return io

    @staticmethod
    def _add_with_references(filled: T, service: BaseService):
        service.add(filled)

        #######################
        # IEC61968 ASSET INFO #
        #######################

        if isinstance(filled, PowerTransformerInfo):
            for it in filled.transformer_tank_infos:
                it.power_transformer_info = filled
                service.add(it)

        if isinstance(filled, TransformerEndInfo):
            filled.transformer_tank_info.add_transformer_end_info(filled)
            service.add(filled.transformer_tank_info)
            filled.transformer_star_impedance.transformer_end_info = filled
            service.add(filled.transformer_star_impedance)
            service.add(filled.energised_end_no_load_tests)
            service.add(filled.energised_end_short_circuit_tests)
            service.add(filled.grounded_end_short_circuit_tests)
            service.add(filled.open_end_open_circuit_tests)
            service.add(filled.energised_end_open_circuit_tests)

        if isinstance(filled, TransformerTankInfo):
            filled.power_transformer_info.add_transformer_tank_info(filled)
            service.add(filled.power_transformer_info)
            for it in filled.transformer_end_infos:
                it.transformer_tank_info = filled
                service.add(it)

        ###################
        # IEC61968 ASSETS #
        ###################

        if isinstance(filled, Asset):
            service.add(filled.location)
            for it in filled.organisation_roles:
                service.add(it)

        if isinstance(filled, Pole):
            for it in filled.streetlights:
                it.pole = filled
                service.add(it)

        if isinstance(filled, Streetlight):
            filled.pole.add_streetlight(filled)
            service.add(filled.pole)

        ###################
        # IEC61968 COMMON #
        ###################

        if isinstance(filled, OrganisationRole):
            service.add(filled.organisation)

        ######################
        # IEC61968 CUSTOMERS #
        ######################

        if isinstance(filled, Customer):
            for it in filled.agreements:
                it.customer = filled
                service.add(it)

        if isinstance(filled, CustomerAgreement):
            filled.customer.add_agreement(filled)
            service.add(filled.customer)
            for it in filled.pricing_structures:
                service.add(it)

        if isinstance(filled, PricingStructure):
            for it in filled.tariffs:
                service.add(it)

        #####################
        # IEC61968 METERING #
        #####################

        if isinstance(filled, EndDevice):
            for it in filled.usage_points:
                it.add_end_device(filled)
                service.add(it)
            service.add(filled.service_location)

        if isinstance(filled, UsagePoint):
            service.add(filled.usage_point_location)
            for it in filled.equipment:
                it.add_usage_point(filled)
                service.add(it)
            for it in filled.end_devices:
                it.add_usage_point(filled)
                service.add(it)

        #######################
        # IEC61968 OPERATIONS #
        #######################

        if isinstance(filled, OperationalRestriction):
            for it in filled.equipment:
                it.add_operational_restriction(filled)
                service.add(it)

        #####################################
        # IEC61970 BASE AUXILIARY EQUIPMENT #
        #####################################

        if isinstance(filled, AuxiliaryEquipment):
            service.add(filled.terminal)

        if isinstance(filled, CurrentTransformer):
            service.add(filled.asset_info)

        if isinstance(filled, PotentialTransformer):
            service.add(filled.asset_info)

        ######################
        # IEC61970 BASE CORE #
        ######################

        if isinstance(filled, ConductingEquipment):
            service.add(filled.base_voltage)
            for it in filled.terminals:
                service.add(it)

        if isinstance(filled, ConnectivityNode):
            for it in filled.terminals:
                it.connectivity_node = filled
                service.add(it)

        if isinstance(filled, Equipment):
            for it in filled.containers:
                it.add_equipment(filled)
                service.add(it)
            for it in filled.usage_points:
                it.add_equipment(filled)
                service.add(it)
            for it in filled.operational_restrictions:
                it.add_equipment(filled)
                service.add(it)

        if isinstance(filled, EquipmentContainer):
            for it in filled.equipment:
                it.add_container(filled)
                service.add(it)

        if isinstance(filled, Feeder):
            service.add(filled.normal_head_terminal)
            filled.normal_energizing_substation.add_feeder(filled)
            service.add(filled.normal_energizing_substation)
            for it in filled.normal_energized_lv_feeders:
                it.add_normal_energizing_feeder(filled)
                service.add(it)

        if isinstance(filled, GeographicalRegion):
            for it in filled.sub_geographical_regions:
                it.geographical_region = filled
                service.add(it)

        if isinstance(filled, Name):
            filled.identified_object.add_name(filled)
            service.add(filled.identified_object)
            service.add_name_type(filled.type)

        if isinstance(filled, PowerSystemResource):
            service.add(filled.location)

        if isinstance(filled, SubGeographicalRegion):
            filled.geographical_region.add_sub_geographical_region(filled)
            service.add(filled.geographical_region)
            for it in filled.substations:
                it.sub_geographical_region = filled
                service.add(it)

        if isinstance(filled, Substation):
            filled.sub_geographical_region.add_substation(filled)
            service.add(filled.sub_geographical_region)
            for it in filled.feeders:
                it.normal_energizing_substation = filled
                service.add(it)
            for it in filled.loops:
                it.add_substation(filled)
                service.add(it)
            for it in filled.energized_loops:
                it.add_energizing_substation(filled)
                service.add(it)
            for it in filled.circuits:
                it.add_end_substation(filled)
                service.add(it)

        if isinstance(filled, Terminal):
            filled.conducting_equipment.add_terminal(filled)
            service.add(filled.conducting_equipment)
            if filled.connectivity_node:
                filled.connectivity_node.add_terminal(filled)
                service.add(filled.connectivity_node)

        ################################
        # IEC61970 BASE DIAGRAM LAYOUT #
        ################################

        if isinstance(filled, Diagram):
            for it in filled.diagram_objects:
                it.diagram = filled
                service.add(it)

        if isinstance(filled, DiagramObject):
            filled.diagram.add_diagram_object(filled)
            service.add(filled.diagram)

        ######################
        # IEC61970 BASE MEAS #
        ######################

        if isinstance(filled, Control):
            filled.remote_control.control = filled
            service.add(filled.remote_control)

        if isinstance(filled, Measurement):
            filled.remote_source.measurement = filled
            service.add(filled.remote_source)

        ############################
        # IEC61970 Base Protection #
        ############################
        if isinstance(filled, ProtectionRelayFunction):
            for it in filled.protected_switches:
                it.add_relay_function(filled)
                service.add(it)
            for it in filled.sensors:
                it.add_relay_function(filled)
                service.add(it)
            for it in filled.schemes:
                it.add_function(filled)
                service.add(it)
            service.add(filled.relay_info)

        if isinstance(filled, Sensor):
            for it in filled.relay_functions:
                it.add_sensor(filled)
                service.add(it)

        if isinstance(filled, ProtectionRelayScheme):
            if filled.system is not None:
                filled.system.add_scheme(filled)
                service.add(filled.system)
            for it in filled.functions:
                it.add_scheme(filled)
                service.add(it)

        if isinstance(filled, ProtectionRelaySystem):
            for it in filled.schemes:
                it.system = filled
                service.add(it)

        #######################
        # IEC61970 BASE SCADA #
        #######################

        if isinstance(filled, RemoteControl):
            filled.control.remote_control = filled
            service.add(filled.control)

        if isinstance(filled, RemoteSource):
            filled.measurement.remote_source = filled
            service.add(filled.measurement)

        #############################################
        # IEC61970 BASE WIRES GENERATION PRODUCTION #
        #############################################

        if isinstance(filled, PowerElectronicsUnit):
            filled.power_electronics_connection.add_unit(filled)
            service.add(filled.power_electronics_connection)

        #######################
        # IEC61970 BASE WIRES #
        #######################

        if isinstance(filled, AcLineSegment):
            service.add(filled.per_length_sequence_impedance)

        if isinstance(filled, Conductor):
            service.add(filled.asset_info)

        if isinstance(filled, EnergyConsumer):
            for it in filled.phases:
                it.energy_consumer = filled
                service.add(it)

        if isinstance(filled, EnergyConsumerPhase):
            filled.energy_consumer.add_phase(filled)
            service.add(filled.energy_consumer)

        if isinstance(filled, EnergySource):
            for it in filled.phases:
                it.energy_source = filled
                service.add(it)

        if isinstance(filled, EnergySourcePhase):
            filled.energy_source.add_phase(filled)
            service.add(filled.energy_source)

        if isinstance(filled, Fuse):
            service.add(filled.function)

        if isinstance(filled, PowerElectronicsConnection):
            for it in filled.units:
                it.power_electronics_connection = filled
                service.add(it)
            for it in filled.phases:
                it.power_electronics_connection = filled
                service.add(it)

        if isinstance(filled, RegulatingCondEq):
            filled.regulating_control.add_regulating_cond_eq(filled)
            service.add(filled.regulating_control)

        if isinstance(filled, RegulatingControl):
            service.add(filled.terminal)
            for it in filled.regulating_conducting_equipment:
                it.regulating_control = filled
                service.add(it)

        if isinstance(filled, PowerElectronicsConnectionPhase):
            filled.power_electronics_connection.add_phase(filled)
            service.add(filled.power_electronics_connection)

        if isinstance(filled, PowerTransformer):
            service.add(filled.asset_info)
            for it in filled.ends:
                it.power_transformer = filled
                service.add(it)

        if isinstance(filled, PowerTransformerEnd):
            filled.power_transformer.add_end(filled)
            service.add(filled.power_transformer)

        if isinstance(filled, ProtectedSwitch):
            for it in filled.relay_functions:
                it.add_protected_switch(filled)
                service.add(it)

        if isinstance(filled, RatioTapChanger):
            filled.transformer_end.ratio_tap_changer = filled
            service.add(filled.transformer_end)
            service.add(filled.tap_changer_control)

        if isinstance(filled, ShuntCompensator):
            service.add(filled.asset_info)

        if isinstance(filled, TransformerEnd):
            service.add(filled.terminal)
            service.add(filled.base_voltage)
            filled.ratio_tap_changer.transformer_end = filled
            service.add(filled.ratio_tap_changer)
            service.add(filled.star_impedance)

        if isinstance(filled, TransformerStarImpedance):
            filled.transformer_end_info.transformer_star_impedance = filled
            service.add(filled.transformer_end_info)

        #########################
        # IEC61970 INF IEC61970 #
        #########################

        if isinstance(filled, Circuit):
            filled.loop.add_circuit(filled)
            service.add(filled.loop)
            for it in filled.end_terminals:
                service.add(it)
            for it in filled.end_substations:
                it.add_circuit(filled)  # could also be add_energized_loop
                service.add(it)

        if isinstance(filled, Loop):
            for it in filled.circuits:
                it.loop = filled
                service.add(it)
            for it in filled.substations:
                it.add_loop(filled)
                service.add(it)
            for it in filled.energizing_substations:
                it.add_energized_loop(filled)
                service.add(it)

        if isinstance(filled, LvFeeder):
            service.add(filled.normal_head_terminal)
            for it in filled.normal_energizing_feeders:
                it.add_normal_energized_lv_feeder(filled)
                service.add(it)

        for io in service.objects():
            for name in io.names:
                service.add_name_type(name.type)
                service.get_name_type(name.type.name).get_or_add_name(name.name, io)
