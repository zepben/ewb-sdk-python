#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable

from pytest import raises
from zepben.ewb import Curve, CurveData

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, identified_object_args, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args
from cim.private_collection_validator import validate_unordered_other_1234567890

# todo curve data?
curve_kwargs = identified_object_kwargs
curve_args = identified_object_args


def verify_curve_constructor_default(curve: Curve):
    verify_identified_object_constructor_default(curve)


def verify_curve_constructor_kwargs(curve: Curve, **kwargs):
    verify_identified_object_constructor_kwargs(curve, **kwargs)


def verify_curve_constructor_args(curve: Curve):
    verify_identified_object_constructor_args(curve)


def test_curve_data_collection():
    validate_unordered_other_1234567890(
        Curve,
        lambda it: CurveData(it + 0.1, it + 0.2, it + 0.3, it + 0.4),
        Curve.data,
        Curve.num_data,
        Curve.get_data,
        Curve.add_curve_data,
        Curve.remove_data,
        Curve.clear_data,
        lambda rs: rs.x_value
    )


def test_add_curve_data_by_passing_in_the_values_and_data_is_sorted_by_x_value_in_ascending_order_when_retrieved():
    curve = Curve()

    curve.add_data(4, 3, 2, 1)
    curve.add_data(2, 1, 2, 3)
    curve.add_data(1, 1, 2, 3)
    curve.add_data(3, 1, 2, 3)

    assert [it.x_value for it in curve.data] == [1, 2, 3, 4]


def test_cant_add_duplicate_curve_data():
    curve = Curve()

    curve.add_data(1, 1, 2, 3)
    _validate_duplicate_error(curve, 1, lambda it: it.add_data(1, 1.1, 2.1, 3.1))
    _validate_duplicate_error(curve, 1, lambda it: it.add_curve_data(CurveData(1, 1.2, 2.2, 3.2)))

    curve.add_curve_data(CurveData(2, 1, 2, 3))
    _validate_duplicate_error(curve, 2, lambda it: it.add_data(2, 1.1, 2.1, 3.1))
    _validate_duplicate_error(curve, 2, lambda it: it.add_curve_data(CurveData(2, 1.2, 2.2, 3.2)))


def _validate_duplicate_error(curve: Curve, x: float, add_data: Callable[[Curve], None]):
    with raises(ValueError, match=f"Unable to add datapoint to {curve}. x_value {x} is invalid, as data with same x_value already exist in this Curve."):
        add_data(curve)
