#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.wires.generation.production.test_power_electronics_unit import power_electronics_unit_kwargs, \
    verify_power_electronics_unit_constructor_default, verify_power_electronics_unit_constructor_kwargs, verify_power_electronics_unit_constructor_args, \
    power_electronics_unit_args
from zepben.evolve import PhotoVoltaicUnit

photo_voltaic_unit_kwargs = power_electronics_unit_kwargs
photo_voltaic_unit_args = power_electronics_unit_args


def test_photo_voltaic_unit_constructor_default():
    verify_power_electronics_unit_constructor_default(PhotoVoltaicUnit())


@given(**photo_voltaic_unit_kwargs)
def test_photo_voltaic_unit_constructor_kwargs(**kwargs):
    verify_power_electronics_unit_constructor_kwargs(PhotoVoltaicUnit(**kwargs), **kwargs)


def test_photo_voltaic_unit_constructor_args():
    verify_power_electronics_unit_constructor_args(PhotoVoltaicUnit(*photo_voltaic_unit_args))
