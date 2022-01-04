#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import sampled_from

from test.cim.common_testing_functions import extract_testing_args
from zepben.evolve import SinglePhaseKind, NominalPhasePath
from zepben.evolve.model.create_basic_model_components import create_nominal_phase_path

nominal_phase_path_kwargs = {
    "from_phase": sampled_from(SinglePhaseKind),
    "to_phase": sampled_from(SinglePhaseKind)
}

# noinspection PyArgumentList
nominal_phase_path_args = [SinglePhaseKind.C, SinglePhaseKind.N]


#
# NOTE: There is no default constructor so no need to test it.
#
# def test_nominal_phase_path_constructor_default():


# noinspection PyShadowingBuiltins,PyArgumentList
@given(**nominal_phase_path_kwargs)
def test_nominal_phase_path_constructor_kwargs(from_phase, to_phase, **kwargs):
    args = extract_testing_args(locals())
    npp = NominalPhasePath(**args, **kwargs)
    validate_nominal_phase_path_values(npp, **args)


# noinspection PyShadowingBuiltins
@given(**nominal_phase_path_kwargs)
def test_nominal_phase_path_creator(from_phase, to_phase, **kwargs):
    args = extract_testing_args(locals())
    npp = create_nominal_phase_path(**args, **kwargs)
    validate_nominal_phase_path_values(npp, **args)


def validate_nominal_phase_path_values(npp, from_phase, to_phase):
    assert npp.from_phase == from_phase
    assert npp.to_phase == to_phase


def test_name_constructor_args():
    # noinspection PyArgumentList
    npp = NominalPhasePath(*nominal_phase_path_args)

    assert npp.from_phase == nominal_phase_path_args[0]
    assert npp.to_phase == nominal_phase_path_args[1]
