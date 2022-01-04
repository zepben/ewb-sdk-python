#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import floats, data

from test.cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, \
    check_conducting_equipment_two_way_link_test
from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.equivalents.test_equivalent_equipment import equivalent_equipment_kwargs, verify_equivalent_equipment_constructor_default, \
    verify_equivalent_equipment_constructor_kwargs, verify_equivalent_equipment_constructor_args, equivalent_equipment_args
from test.cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import EquivalentBranch
from zepben.evolve.model.cim.iec61970.base.equivalents.create_equivalents_components import create_equivalent_branch

equivalent_branch_kwargs = {
    **equivalent_equipment_kwargs,
    "negative_r12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "negative_r21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "negative_x12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "negative_x21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "positive_r12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "positive_r21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "positive_x12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "positive_x21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "zero_r12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "zero_r21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "zero_x12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "zero_x21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
}

equivalent_branch_args = [*equivalent_equipment_args, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.01, 11.11, 12.21, 13.31, 14.41, 15.51, 16.61]


def test_equivalent_branch_constructor_default():
    eb = EquivalentBranch()
    eb2 = create_equivalent_branch()

    verify_default_equivalent_branch(eb)
    verify_default_equivalent_branch(eb2)


def verify_default_equivalent_branch(eb):
    verify_equivalent_equipment_constructor_default(eb)
    assert not eb.negative_r12
    assert not eb.negative_r21
    assert not eb.negative_x12
    assert not eb.negative_x21
    assert not eb.positive_r12
    assert not eb.positive_r21
    assert not eb.positive_x12
    assert not eb.positive_x21
    assert not eb.r
    assert not eb.r21
    assert not eb.x
    assert not eb.x21
    assert not eb.zero_r12
    assert not eb.zero_r21
    assert not eb.zero_x12
    assert not eb.zero_x21


# noinspection PyShadowingNames
@given(data())
def test_equivalent_branch_constructor_kwargs(data):
    verify(
        [EquivalentBranch, create_equivalent_branch],
        data, equivalent_branch_kwargs, verify_equivalent_branch_values
    )


def verify_equivalent_branch_values(eb, negative_r12, negative_r21, negative_x12, negative_x21, positive_r12, positive_r21, positive_x12, positive_x21, r,
                                    r21, x, x21, zero_r12, zero_r21, zero_x12, zero_x21, **kwargs):
    verify_equivalent_equipment_constructor_kwargs(eb, **kwargs)
    assert eb.negative_r12 == negative_r12
    assert eb.negative_r21 == negative_r21
    assert eb.negative_x12 == negative_x12
    assert eb.negative_x21 == negative_x21
    assert eb.positive_r12 == positive_r12
    assert eb.positive_r21 == positive_r21
    assert eb.positive_x12 == positive_x12
    assert eb.positive_x21 == positive_x21
    assert eb.r == r
    assert eb.r21 == r21
    assert eb.x == x
    assert eb.x21 == x21
    assert eb.zero_r12 == zero_r12
    assert eb.zero_r21 == zero_r21
    assert eb.zero_x12 == zero_x12
    assert eb.zero_x21 == zero_x21


def test_equivalent_branch_constructor_args():
    eb = EquivalentBranch(*equivalent_branch_args)

    verify_equivalent_equipment_constructor_args(eb)
    assert eb.negative_r12 == equivalent_branch_args[-16]
    assert eb.negative_r21 == equivalent_branch_args[-15]
    assert eb.negative_x12 == equivalent_branch_args[-14]
    assert eb.negative_x21 == equivalent_branch_args[-13]
    assert eb.positive_r12 == equivalent_branch_args[-12]
    assert eb.positive_r21 == equivalent_branch_args[-11]
    assert eb.positive_x12 == equivalent_branch_args[-10]
    assert eb.positive_x21 == equivalent_branch_args[-9]
    assert eb.r == equivalent_branch_args[-8]
    assert eb.r21 == equivalent_branch_args[-7]
    assert eb.x == equivalent_branch_args[-6]
    assert eb.x21 == equivalent_branch_args[-5]
    assert eb.zero_r12 == equivalent_branch_args[-4]
    assert eb.zero_r21 == equivalent_branch_args[-3]
    assert eb.zero_x12 == equivalent_branch_args[-2]
    assert eb.zero_x21 == equivalent_branch_args[-1]


def test_auto_two_way_connections_for_pole_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    eb = create_equivalent_branch(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t])
    check_conducting_equipment_two_way_link_test(eb, up, ec, opr, f, t)
