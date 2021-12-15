#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.test_common_two_way_connections import set_up_common_equipment_two_way_link_test, check_common_equipment_two_way_link_test
from test.cim.iec61970.base.auxiliaryequipment.test_auxiliary_equipment import auxiliary_equipment_kwargs, verify_auxiliary_equipment_constructor_default, \
    verify_auxiliary_equipment_constructor_kwargs, verify_auxiliary_equipment_constructor_args, auxiliary_equipment_args
from zepben.evolve import FaultIndicator
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.create_auxiliary_equipment_components import create_fault_indicator

fault_indicator_info_kwargs = auxiliary_equipment_kwargs
fault_indicator_info_args = auxiliary_equipment_args


def test_fault_indicator_info_constructor_default():
    verify_auxiliary_equipment_constructor_default(FaultIndicator())
    verify_auxiliary_equipment_constructor_default(create_fault_indicator())


@given(**fault_indicator_info_kwargs)
def test_fault_indicator_info_constructor_kwargs(**kwargs):
    # noinspection PyArgumentList
    verify_auxiliary_equipment_constructor_kwargs(FaultIndicator(**kwargs), **kwargs)


@given(**fault_indicator_info_kwargs)
def test_fault_indicator_info_creator(**kwargs):
    # noinspection PyArgumentList
    verify_auxiliary_equipment_constructor_kwargs(create_fault_indicator(**kwargs), **kwargs)


def test_fault_indicator_info_constructor_args():
    # noinspection PyArgumentList
    verify_auxiliary_equipment_constructor_args(FaultIndicator(*fault_indicator_info_args))


def test_auto_two_way_connections_for_fault_indicator_constructor():

    up, ec, opr, f = set_up_common_equipment_two_way_link_test()
    fi = create_fault_indicator(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f])
    check_common_equipment_two_way_link_test(fi, up, ec, opr, f)


