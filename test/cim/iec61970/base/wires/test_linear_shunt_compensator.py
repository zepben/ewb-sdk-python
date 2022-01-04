#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import floats, data

from test.cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.wires.test_shunt_compensator import verify_shunt_compensator_constructor_default, \
    verify_shunt_compensator_constructor_kwargs, verify_shunt_compensator_constructor_args, shunt_compensator_kwargs, shunt_compensator_args
from test.cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import LinearShuntCompensator
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_linear_shunt_compensator

linear_shunt_compensator_kwargs = {
    **shunt_compensator_kwargs,
    "b0_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "b_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "g0_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "g_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

linear_shunt_compensator_args = [*shunt_compensator_args, 1.1, 2.2, 3.3, 4.4]


def test_linear_shunt_compensator_constructor_default():
    lsc = LinearShuntCompensator()
    lsc2 = create_linear_shunt_compensator()
    verify_default_linear_shunt_compensator_constructor(lsc)
    verify_default_linear_shunt_compensator_constructor(lsc2)


def verify_default_linear_shunt_compensator_constructor(lsc):
    verify_shunt_compensator_constructor_default(lsc)
    assert lsc.b0_per_section is None
    assert lsc.b_per_section is None
    assert lsc.g0_per_section is None
    assert lsc.g_per_section is None


# noinspection PyShadowingNames
@given(data())
def test_linear_shunt_compensator_constructor_kwargs(data):
    verify(
        [LinearShuntCompensator, create_linear_shunt_compensator],
        data, linear_shunt_compensator_kwargs, verify_linear_shunt_compensator_values
    )


def verify_linear_shunt_compensator_values(lsc, b0_per_section, b_per_section, g0_per_section, g_per_section, **kwargs):
    verify_shunt_compensator_constructor_kwargs(lsc, **kwargs)
    assert lsc.b0_per_section == b0_per_section
    assert lsc.b_per_section == b_per_section
    assert lsc.g0_per_section == g0_per_section
    assert lsc.g_per_section == g_per_section


def test_linear_shunt_compensator_constructor_args():
    lsc = LinearShuntCompensator(*linear_shunt_compensator_args)

    verify_shunt_compensator_constructor_args(lsc)
    assert lsc.b0_per_section == linear_shunt_compensator_args[-4]
    assert lsc.b_per_section == linear_shunt_compensator_args[-3]
    assert lsc.g0_per_section == linear_shunt_compensator_args[-2]
    assert lsc.g_per_section == linear_shunt_compensator_args[-1]


def test_auto_two_way_connections_for_linear_shunt_compensator_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    lsc = create_linear_shunt_compensator(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t])
    check_conducting_equipment_two_way_link_test(lsc, up, ec, opr, f, t)
