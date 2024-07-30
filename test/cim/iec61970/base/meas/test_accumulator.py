#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.meas.test_measurement import measurement_kwargs, verify_measurement_constructor_default, \
    verify_measurement_constructor_kwargs, verify_measurement_constructor_args, measurement_args
from zepben.evolve import Accumulator

accumulator_kwargs = measurement_kwargs
accumulator_args = measurement_args


def test_accumulator_constructor_default():
    verify_measurement_constructor_default(Accumulator())


@given(**accumulator_kwargs)
def test_accumulator_constructor_kwargs(**kwargs):
    # noinspection PyArgumentList
    verify_measurement_constructor_kwargs(Accumulator(**kwargs), **kwargs)


def test_accumulator_constructor_args():
    # noinspection PyArgumentList
    verify_measurement_constructor_args(Accumulator(*accumulator_args))
