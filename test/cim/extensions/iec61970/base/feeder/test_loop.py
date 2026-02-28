#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists

from util import mrid_strategy
from zepben.ewb import Loop, Circuit, Substation, generate_id

from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, verify_identified_object_constructor_kwargs, \
    verify_identified_object_constructor_args, identified_object_kwargs, identified_object_args
from cim.private_collection_validator import validate_unordered

loop_kwargs = {
    **identified_object_kwargs,
    "circuits": lists(builds(Circuit, mrid=mrid_strategy)),
    "substations": lists(builds(Substation, mrid=mrid_strategy)),
    "energizing_substations": lists(builds(Substation, mrid=mrid_strategy))
}

loop_args = [*identified_object_args, [Circuit(mrid=generate_id())], [Substation(mrid=generate_id())], [Substation(mrid=generate_id())]]


def test_loop_constructor_default():
    loop = Loop(mrid=generate_id())

    verify_identified_object_constructor_default(loop)
    assert not list(loop.circuits)
    assert not list(loop.substations)
    assert not list(loop.energizing_substations)


@given(**loop_kwargs)
def test_loop_constructor_kwargs(circuits, substations, energizing_substations, **kwargs):
    loop = Loop(
        circuits=circuits,
        substations=substations,
        energizing_substations=energizing_substations,
        **kwargs
    )

    verify_identified_object_constructor_kwargs(loop, **kwargs)
    assert list(loop.circuits) == circuits
    assert list(loop.substations) == substations
    assert list(loop.energizing_substations) == energizing_substations


def test_loop_constructor_args():
    loop = Loop(*loop_args)

    verify_identified_object_constructor_args(loop)
    assert loop_args[-3:] == [
        list(loop.circuits),
        list(loop.substations),
        list(loop.energizing_substations)
    ]


def test_circuits_collection():
    validate_unordered(
        Loop,
        lambda mrid: Circuit(mrid),
        Loop.circuits,
        Loop.num_circuits,
        Loop.get_circuit,
        Loop.add_circuit,
        Loop.remove_circuit,
        Loop.clear_circuits
    )


def test_substations_collection():
    validate_unordered(
        Loop,
        lambda mrid: Substation(mrid),
        Loop.substations,
        Loop.num_substations,
        Loop.get_substation,
        Loop.add_substation,
        Loop.remove_substation,
        Loop.clear_substations
    )


def test_energizing_substations_collection():
    validate_unordered(
        Loop,
        lambda mrid: Substation(mrid),
        Loop.energizing_substations,
        Loop.num_energizing_substations,
        Loop.get_energizing_substation,
        Loop.add_energizing_substation,
        Loop.remove_energizing_substation,
        Loop.clear_energizing_substations
    )
