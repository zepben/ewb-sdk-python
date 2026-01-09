#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds

from cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args, equipment_container_args
from cim.private_collection_validator import validate_unordered
from util import mrid_strategy
from zepben.ewb import Substation, Feeder, Loop, Circuit, generate_id
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion

substation_kwargs = {
    **equipment_container_kwargs,
    "sub_geographical_region": builds(SubGeographicalRegion, mrid=mrid_strategy),
    "normal_energized_feeders": lists(builds(Feeder, mrid=mrid_strategy), max_size=2),
    "loops": lists(builds(Loop, mrid=mrid_strategy), max_size=2),
    "energized_loops": lists(builds(Loop, mrid=mrid_strategy), max_size=2),
    "circuits": lists(builds(Circuit, mrid=mrid_strategy), max_size=2)
}

substation_args = [
    *equipment_container_args,
    Substation(mrid=generate_id()),
    [Feeder(mrid=generate_id())],
    [Loop(mrid=generate_id())],
    [Loop(mrid=generate_id())],
    [Circuit(mrid=generate_id())]
]


def test_substation_constructor_default():
    cn = Substation(mrid=generate_id())

    verify_equipment_container_constructor_default(cn)
    assert not cn.sub_geographical_region
    assert not list(cn.feeders)
    assert not list(cn.loops)
    assert not list(cn.energized_loops)
    assert not list(cn.circuits)


@given(**substation_kwargs)
def test_substation_constructor_kwargs(sub_geographical_region, normal_energized_feeders, loops, energized_loops, circuits, **kwargs):
    cn = Substation(sub_geographical_region=sub_geographical_region,
                    normal_energized_feeders=normal_energized_feeders,
                    loops=loops,
                    energized_loops=energized_loops,
                    circuits=circuits,
                    **kwargs)

    verify_equipment_container_constructor_kwargs(cn, **kwargs)
    assert cn.sub_geographical_region == sub_geographical_region
    assert list(cn.feeders) == normal_energized_feeders
    assert list(cn.loops) == loops
    assert list(cn.energized_loops) == energized_loops
    assert list(cn.circuits) == circuits


def test_substation_constructor_args():
    cn = Substation(*substation_args)

    verify_equipment_container_constructor_args(cn)
    assert substation_args[-5:] == [
        cn.sub_geographical_region,
        list(cn.feeders),
        list(cn.loops),
        list(cn.energized_loops),
        list(cn.circuits)
    ]


def test_normal_energized_feeders_collection():
    validate_unordered(
        Substation,
        lambda mrid: Feeder(mrid),
        Substation.feeders,
        Substation.num_feeders,
        Substation.get_feeder,
        Substation.add_feeder,
        Substation.remove_feeder,
        Substation.clear_feeders
    )


def test_loops_collection():
    validate_unordered(
        Substation,
        lambda mrid: Loop(mrid),
        Substation.loops,
        Substation.num_loops,
        Substation.get_loop,
        Substation.add_loop,
        Substation.remove_loop,
        Substation.clear_loops
    )


def test_energized_loops_collection():
    validate_unordered(
        Substation,
        lambda mrid: Loop(mrid),
        Substation.energized_loops,
        Substation.num_energized_loops,
        Substation.get_energized_loop,
        Substation.add_energized_loop,
        Substation.remove_energized_loop,
        Substation.clear_energized_loops
    )


def test_circuits_collection():
    validate_unordered(
        Substation,
        lambda mrid: Circuit(mrid),
        Substation.circuits,
        Substation.num_circuits,
        Substation.get_circuit,
        Substation.add_circuit,
        Substation.remove_circuit,
        Substation.clear_circuits
    )
