#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import UsagePoint, EquipmentContainer, OperationalRestriction, Feeder, Equipment, Terminal, ConductingEquipment, PowerElectronicsConnection, \
    PowerElectronicsUnit


def set_up_common_equipment_two_way_link_test():
    up = UsagePoint()
    ec = EquipmentContainer()
    opr = OperationalRestriction()
    f = Feeder()
    return up, ec, opr, f


def check_common_equipment_two_way_link_test(e: Equipment, up: UsagePoint, ec: EquipmentContainer, opr: OperationalRestriction, f: Feeder):
    assert up.get_equipment(e.mrid) == e
    assert ec.get_equipment(e.mrid) == e
    assert opr.get_equipment(e.mrid) == e
    assert f.get_equipment(e.mrid) == e


def set_up_conducting_equipment_two_way_link_test():
    up, ec, opr, f = set_up_common_equipment_two_way_link_test()
    t = Terminal()
    return up, ec, opr, f, t


def check_conducting_equipment_two_way_link_test(ce: ConductingEquipment, up: UsagePoint, ec: EquipmentContainer, opr: OperationalRestriction, f: Feeder,
                                                 t: Terminal):
    check_common_equipment_two_way_link_test(ce, up, ec, opr, f)
    assert t.conducting_equipment == ce


def check_equipment_container_connection(e: Equipment, ec: EquipmentContainer):
    assert e.get_container(ec.mrid) == ec


def set_up_power_electronics_unit_two_way_link_test():
    up, ec, opr, f = set_up_common_equipment_two_way_link_test()
    pec = PowerElectronicsConnection()
    return up, ec, opr, f, pec


def check_power_electronics_unit_two_way_link_test(peu: PowerElectronicsUnit, up: UsagePoint, ec: EquipmentContainer, opr: OperationalRestriction, f: Feeder,
                                                   pec: PowerElectronicsConnection):
    check_common_equipment_two_way_link_test(peu, up, ec, opr, f)
    assert pec.get_unit(peu.mrid) == peu
