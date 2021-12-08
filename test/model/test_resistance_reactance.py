#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import floats

from test.cim.extract_testing_args import extract_testing_args
from cim.iec61968.assetinfo.test_transformer_end_info import validate_resistance_reactance
from test.cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import ResistanceReactance
from zepben.evolve.model.create_basic_model_components import create_resistance_reactance

resistance_reactance_kwargs = {
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

# noinspection PyArgumentList
resistance_reactance_args = [1.1, 2.2, 3.3, 4.4]


#
# NOTE: There is no default constructor so no need to test it.
#
# def test_resistance_reactance_constructor_default():


# noinspection PyShadowingBuiltins,PyArgumentList
@given(**resistance_reactance_kwargs)
def test_resistance_reactance_constructor_kwargs(r, x, r0, x0, **kwargs):
    args = extract_testing_args(locals())
    rr = ResistanceReactance(**args, **kwargs)
    validate_resistance_reactance(rr, **args)


# noinspection PyShadowingBuiltins
@given(**resistance_reactance_kwargs)
def test_resistance_reactance_creator(r, x, r0, x0, **kwargs):
    args = extract_testing_args(locals())
    rr = create_resistance_reactance(**args, **kwargs)
    validate_resistance_reactance(rr, **args)


def test_name_constructor_args():
    # noinspection PyArgumentList
    rr = ResistanceReactance(*resistance_reactance_args)

    assert rr.r == resistance_reactance_args[0]
    assert rr.x == resistance_reactance_args[1]
    assert rr.r0 == resistance_reactance_args[2]
    assert rr.x0 == resistance_reactance_args[3]
