#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats

from cim.iec61970.base.equivalents.test_equivalent_equipment import equivalent_equipment_kwargs, verify_equivalent_equipment_constructor_default, \
    verify_equivalent_equipment_constructor_kwargs, verify_equivalent_equipment_constructor_args, equivalent_equipment_args
from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import EquivalentBranch

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
    t = EquivalentBranch()

    verify_equivalent_equipment_constructor_default(t)
    assert not t.negative_r12
    assert not t.negative_r21
    assert not t.negative_x12
    assert not t.negative_x21
    assert not t.positive_r12
    assert not t.positive_r21
    assert not t.positive_x12
    assert not t.positive_x21
    assert not t.r
    assert not t.r21
    assert not t.x
    assert not t.x21
    assert not t.zero_r12
    assert not t.zero_r21
    assert not t.zero_x12
    assert not t.zero_x21


@given(**equivalent_branch_kwargs)
def test_equivalent_branch_constructor_kwargs(negative_r12, negative_r21, negative_x12, negative_x21, positive_r12, positive_r21, positive_x12, positive_x21, r, r21, x,
                                              x21, zero_r12, zero_r21, zero_x12, zero_x21, **kwargs):
    t = EquivalentBranch(
        negative_r12=negative_r12,
        negative_r21=negative_r21,
        negative_x12=negative_x12,
        negative_x21=negative_x21,
        positive_r12=positive_r12,
        positive_r21=positive_r21,
        positive_x12=positive_x12,
        positive_x21=positive_x21,
        r=r,
        r21=r21,
        x=x,
        x21=x21,
        zero_r12=zero_r12,
        zero_r21=zero_r21,
        zero_x12=zero_x12,
        zero_x21=zero_x21,
        **kwargs
    )

    verify_equivalent_equipment_constructor_kwargs(t, **kwargs)
    assert t.negative_r12 == negative_r12
    assert t.negative_r21 == negative_r21
    assert t.negative_x12 == negative_x12
    assert t.negative_x21 == negative_x21
    assert t.positive_r12 == positive_r12
    assert t.positive_r21 == positive_r21
    assert t.positive_x12 == positive_x12
    assert t.positive_x21 == positive_x21
    assert t.r == r
    assert t.r21 == r21
    assert t.x == x
    assert t.x21 == x21
    assert t.zero_r12 == zero_r12
    assert t.zero_r21 == zero_r21
    assert t.zero_x12 == zero_x12
    assert t.zero_x21 == zero_x21


def test_equivalent_branch_constructor_args():
    t = EquivalentBranch(*equivalent_branch_args)

    verify_equivalent_equipment_constructor_args(t)
    assert t.negative_r12 == equivalent_branch_args[-16]
    assert t.negative_r21 == equivalent_branch_args[-15]
    assert t.negative_x12 == equivalent_branch_args[-14]
    assert t.negative_x21 == equivalent_branch_args[-13]
    assert t.positive_r12 == equivalent_branch_args[-12]
    assert t.positive_r21 == equivalent_branch_args[-11]
    assert t.positive_x12 == equivalent_branch_args[-10]
    assert t.positive_x21 == equivalent_branch_args[-9]
    assert t.r == equivalent_branch_args[-8]
    assert t.r21 == equivalent_branch_args[-7]
    assert t.x == equivalent_branch_args[-6]
    assert t.x21 == equivalent_branch_args[-5]
    assert t.zero_r12 == equivalent_branch_args[-4]
    assert t.zero_r21 == equivalent_branch_args[-3]
    assert t.zero_x12 == equivalent_branch_args[-2]
    assert t.zero_x21 == equivalent_branch_args[-1]
