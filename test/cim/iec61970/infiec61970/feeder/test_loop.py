#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists

from cim import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, verify_identified_object_constructor_kwargs, \
    verify_identified_object_constructor_args, identified_object_kwargs, identified_object_args
from zepben.evolve import Loop, Circuit, Substation
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.create_feeder_components import create_loop

loop_kwargs = {
    **identified_object_kwargs,
    "circuits": lists(builds(Circuit)),
    "substations": lists(builds(Substation)),
    "energizing_substations": lists(builds(Substation))
}

loop_args = [*identified_object_args, [Circuit()], [Substation()], [Substation()]]


def test_loop_constructor_default():
    loop = Loop()
    loop2 = create_loop()
    validate_default_loop_constructor(loop)
    validate_default_loop_constructor(loop2)


def validate_default_loop_constructor(loop):
    verify_identified_object_constructor_default(loop)
    assert not list(loop.circuits)
    assert not list(loop.substations)
    assert not list(loop.energizing_substations)


@given(**loop_kwargs)
def test_loop_constructor_kwargs(circuits, substations, energizing_substations, **kwargs):
    args = extract_testing_args(locals())
    loop = Loop(**args, **kwargs)
    validate_loop_constructor_values(loop, **args, **kwargs)


@given(**loop_kwargs)
def test_loop_creator(circuits, substations, energizing_substations, **kwargs):
    args = extract_testing_args(locals())
    loop = create_loop(**args, **kwargs)
    validate_loop_constructor_values(loop, **args, **kwargs)


def validate_loop_constructor_values(loop, circuits, substations, energizing_substations, **kwargs):
    verify_identified_object_constructor_kwargs(loop, **kwargs)
    assert list(loop.circuits) == circuits
    assert list(loop.substations) == substations
    assert list(loop.energizing_substations) == energizing_substations


def test_loop_constructor_args():
    loop = Loop(*loop_args)

    verify_identified_object_constructor_args(loop)
    assert list(loop.circuits) == loop_args[-3]
    assert list(loop.substations) == loop_args[-2]
    assert list(loop.energizing_substations) == loop_args[-1]


def test_circuits_collection():
    validate_collection_unordered(Loop,
                                  lambda mrid, _: Circuit(mrid),
                                  Loop.num_circuits,
                                  Loop.get_circuit,
                                  Loop.circuits,
                                  Loop.add_circuit,
                                  Loop.remove_circuit,
                                  Loop.clear_circuits)


def test_substations_collection():
    validate_collection_unordered(Loop,
                                  lambda mrid, _: Substation(mrid),
                                  Loop.num_substations,
                                  Loop.get_substation,
                                  Loop.substations,
                                  Loop.add_substation,
                                  Loop.remove_substation,
                                  Loop.clear_substations)


def test_energizing_substations_collection():
    validate_collection_unordered(Loop,
                                  lambda mrid, _: Substation(mrid),
                                  Loop.num_energizing_substations,
                                  Loop.get_energizing_substation,
                                  Loop.energizing_substations,
                                  Loop.add_energizing_substation,
                                  Loop.remove_energizing_substation,
                                  Loop.clear_energizing_substations)
