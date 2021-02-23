#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import uuids, text, lists, booleans, builds, sampled_from, integers

from test.cim_creators import ALPHANUM, TEXT_MAX_SIZE, location, sampled_asset_info, sampled_equipment, document, sampled_equipment_container, \
    equipmentcontainer, identifiedobject, acdcterminal, basevoltage, powersystemresource, MAX_32_BIT_INTEGER, MIN_32_BIT_INTEGER
from zepben.evolve import IdentifiedObject, PowerSystemResource, Location, CableInfo, Equipment, UsagePoint, OperationalRestriction, Feeder, Site, \
    ConductingEquipment, BaseVoltage, Terminal, RegulatingCondEq, PowerElectronicsConnection, PowerElectronicsUnit, PhaseCode, Substation

# NOTE:
# verify...constructor calls are used for verifying the constructor for a superclass works as intended at least with no args or with a set of args.
# verify...args calls verify a given set of positional arguments to the constructor for a specific type.
# there is a lot of overlap here, but calling both maximises the constructor combinations we check and should catch any breaking changes to
# constructors.

io_kwargs = {"mrid": uuids(version=4).map(lambda x: str(x)), "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
             "description": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)}

io_args = ("test_mrid", "test_name", "test_description")


psr_kwargs = {**io_kwargs, "location": builds(Location, **identifiedobject()), "asset_info": sampled_asset_info()}

psr_args = (*io_args, Location("test_location"), CableInfo("test_assetinfo"))


equip_kwargs = {**psr_kwargs, "in_service": booleans(), "normally_in_service": booleans(),
                "usage_points": lists(builds(UsagePoint, **identifiedobject()), max_size=1),
                "equipment_containers": lists(sampled_equipment_container(), max_size=1),
                "operational_restrictions": lists(builds(OperationalRestriction, **identifiedobject()), max_size=1),
                "current_feeders": lists(builds(Feeder, **identifiedobject()), max_size=1)}

equip_args = (*psr_args, False, False, [UsagePoint("test_up")], [Site("test_site")], [OperationalRestriction("test_or")], [Feeder("test_feeder")])


ce_kwargs = {**equip_kwargs,
             "base_voltage": builds(BaseVoltage, **identifiedobject()),
             "terminals":
                 lists(builds(Terminal, phases=sampled_from(PhaseCode), sequence_number=integers(min_value=1, max_value=100)), max_size=1)
             }

ce_args = (*equip_args, BaseVoltage("test_bv"), [Terminal("test_terminal")])


rce_kwargs = {**ce_kwargs, "control_enabled": booleans()}

rce_args = (*ce_args, False)


cn_kwargs = {**ce_kwargs}

cn_args = ce_args


peu_kwargs = {**equip_kwargs, "power_electronics_connection": builds(PowerElectronicsConnection),
              "max_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
              "min_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
              }

peu_args = (*equip_args, PowerElectronicsConnection("test_pec"), -100, 200)


def verify_identifed_object_constructor(clazz, mrid, name, description, **kwargs):
    io: IdentifiedObject = clazz()
    assert io.mrid

    io = clazz(mrid="test")
    assert io.mrid == "test"

    io = clazz(mrid, name, description)
    assert io.mrid == mrid
    assert io.name == name
    assert io.description == description

    io = clazz(name="test_name", description="test_description")
    assert io.mrid
    assert io.name == "test_name"
    assert io.description == "test_description"


def verify_power_system_resource_constructor(clazz, location, asset_info, **kwargs):
    psr: PowerSystemResource = clazz()
    assert psr.location is None
    assert psr.asset_info is None
    psr = clazz(location=location, asset_info=asset_info)
    assert psr.location.mrid == location.mrid
    assert psr.asset_info.mrid == asset_info.mrid

    verify_identifed_object_constructor(clazz, **kwargs)


def verify_equipment_constructor(clazz, in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders,
                                 **kwargs):
    eq: Equipment = clazz()
    assert eq.in_service
    assert eq.normally_in_service
    assert eq._usage_points is None
    assert eq._equipment_containers is None
    assert eq._operational_restrictions is None
    assert eq._current_feeders is None

    eq1: Equipment = clazz(in_service=in_service, normally_in_service=normally_in_service, usage_points=usage_points, equipment_containers=equipment_containers,
                           operational_restrictions=operational_restrictions, current_feeders=current_feeders)
    assert [up for up in eq1.usage_points] == usage_points and eq1.num_usage_points() == len(usage_points)
    assert [ec for ec in eq1.equipment_containers] == equipment_containers and eq1.num_equipment_containers() == len(equipment_containers)
    assert [o for o in eq1.operational_restrictions] == operational_restrictions and eq1.num_restrictions() == len(operational_restrictions)
    assert [f for f in eq1.current_feeders] == current_feeders and eq1.num_current_feeders() == len(current_feeders)
    assert eq1.num_normal_feeders() == len([x for x in equipment_containers if isinstance(x, Feeder)])
    assert eq1.num_substations() == len([x for x in equipment_containers if isinstance(x, Substation)])
    assert eq1.num_sites() == len([x for x in equipment_containers if isinstance(x, Site)])

    verify_power_system_resource_constructor(clazz, **kwargs)


def verify_conducting_equipment_constructor(clazz, base_voltage, terminals, **kwargs):
    ce: ConductingEquipment = clazz()
    assert ce.base_voltage is None
    assert ce._terminals == []
    ce: ConductingEquipment = clazz(base_voltage=base_voltage, terminals=terminals)
    assert ce.base_voltage == base_voltage
    assert [t for t in ce.terminals] == terminals

    verify_equipment_constructor(clazz, **kwargs)


def verify_regulating_cond_eq_constructor(clazz, control_enabled, **kwargs):
    rce: RegulatingCondEq = clazz()
    assert rce.control_enabled
    rce = clazz(control_enabled=control_enabled)
    assert rce.control_enabled == control_enabled

    verify_conducting_equipment_constructor(clazz, **kwargs)


def verify_connector_constructor(clazz, **kwargs):
    verify_conducting_equipment_constructor(clazz, **kwargs)


def verify_power_electronics_unit_constructor(clazz, power_electronics_connection, max_p, min_p, **kwargs):
    peu = clazz(power_electronics_connection=power_electronics_connection, max_p=max_p, min_p=min_p)
    assert peu.power_electronics_connection == power_electronics_connection
    assert peu.max_p == max_p
    assert peu.min_p == min_p
    verify_equipment_constructor(clazz=PowerElectronicsUnit, **kwargs)


def verify_io_args(io):
    assert io.mrid
    assert io.name == "test_name"
    assert io.description == "test_description"


def verify_psr_args(psr):
    assert psr.location.mrid == "test_location"
    assert psr.asset_info.mrid == "test_assetinfo"
    verify_io_args(psr)


def verify_equip_args(eq):
    assert not eq.in_service
    assert not eq.normally_in_service
    assert eq._usage_points[0].mrid == "test_up" and eq.num_usage_points() == 1
    assert eq._equipment_containers[0].mrid == "test_site" and eq.num_equipment_containers() == 1 and eq.num_sites() == 1
    assert eq._operational_restrictions[0].mrid == "test_or" and eq.num_restrictions() == 1
    assert eq._current_feeders[0].mrid == "test_feeder" and eq.num_current_feeders() == 1
    assert eq.num_normal_feeders() == 0
    assert eq.num_substations() == 0
    verify_psr_args(eq)


def verify_ce_args(ce):
    assert ce.base_voltage.mrid == "test_bv"
    assert ce._terminals[0].mrid == "test_terminal"
    verify_equip_args(ce)


def verify_rce_args(rce):
    assert not rce.control_enabled
    verify_ce_args(rce)


def verify_cn_args(cn):
    verify_ce_args(cn)


def verify_peu_args(peu):
    assert peu.power_electronics_connection == peu_args[-3]
    assert peu.max_p == -100
    assert peu.min_p == 200
    verify_equip_args(peu)
