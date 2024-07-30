#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pytest import raises
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, lists, floats, integers

from cim.iec61970.base.core.test_conducting_equipment import verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_kwargs, conducting_equipment_args
from cim.cim_creators import FLOAT_MIN, FLOAT_MAX, MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER

from zepben.evolve import SeriesCompensator

series_compensator_kwargs = {
    **conducting_equipment_kwargs,
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "varistor_rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "varistor_voltage_threshold": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
}

series_compensator_args = [*conducting_equipment_args, 1.1, 2.2, 3.3, 4.4, 5, 6]


def test_series_compensator_constructor_default():
    sc = SeriesCompensator()

    verify_conducting_equipment_constructor_default(sc)
    assert sc.r is None
    assert sc.r0 is None
    assert sc.x is None
    assert sc.x0 is None
    assert sc.varistor_rated_current is None
    assert sc.varistor_voltage_threshold is None


@given(**series_compensator_kwargs)
def test_series_compensator_constructor_kwargs(r, r0, x, x0, varistor_rated_current, varistor_voltage_threshold, **kwargs):
    sc = SeriesCompensator(r=r,
                           r0=r0,
                           x=x,
                           x0=x0,
                           varistor_rated_current=varistor_rated_current,
                           varistor_voltage_threshold=varistor_voltage_threshold,
                           **kwargs)

    verify_conducting_equipment_constructor_kwargs(sc, **kwargs)
    assert sc.r == r
    assert sc.r0 == r0
    assert sc.x == x
    assert sc.x0 == x0
    assert sc.varistor_rated_current == varistor_rated_current
    assert sc.varistor_voltage_threshold == varistor_voltage_threshold


def test_series_compensator_constructor_args():
    sc = SeriesCompensator(*series_compensator_args)

    verify_conducting_equipment_constructor_args(sc)
    assert sc.r == series_compensator_args[-6]
    assert sc.r0 == series_compensator_args[-5]
    assert sc.x == series_compensator_args[-4]
    assert sc.x0 == series_compensator_args[-3]
    assert sc.varistor_rated_current == series_compensator_args[-2]
    assert sc.varistor_voltage_threshold == series_compensator_args[-1]


def test_varistor_present_flag():
    sc = SeriesCompensator(varistor_rated_current=None, varistor_voltage_threshold=None)

    assert sc.varistor_present() is False

    sc.varistor_rated_current = 1
    assert sc.varistor_present() is True
    sc.varistor_rated_current = None
    assert sc.varistor_present() is False

    sc.varistor_voltage_threshold = 1
    assert sc.varistor_present() is True
    sc.varistor_voltage_threshold = None
    assert sc.varistor_present() is False

    sc.varistor_voltage_threshold = 1
    sc.varistor_rated_current = 1
    assert sc.varistor_present() is True

    sc.varistor_voltage_threshold = None
    sc.varistor_rated_current = None
    assert sc.varistor_present() is False
