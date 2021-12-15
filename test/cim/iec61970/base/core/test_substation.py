#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds

from test.cim.extract_testing_args import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args, equipment_container_args
from zepben.evolve import Substation, Feeder, Loop, Circuit, SubGeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.create_core_components import create_substation

substation_kwargs = {
    **equipment_container_kwargs,
    "sub_geographical_region": builds(SubGeographicalRegion),
    "normal_energized_feeders": lists(builds(Feeder), max_size=2),
    "loops": lists(builds(Loop), max_size=2),
    "energized_loops": lists(builds(Loop), max_size=2),
    "circuits": lists(builds(Circuit), max_size=2)
}

substation_args = [*equipment_container_args, Substation(), [Feeder()], [Loop()], [Loop()], [Circuit()]]


def test_substation_constructor_default():
    ss = Substation()
    ss2 = create_substation()
    validate_default_substation(ss)
    validate_default_substation(ss2)


def validate_default_substation(ss):
    verify_equipment_container_constructor_default(ss)
    assert not ss.sub_geographical_region
    assert not list(ss.feeders)
    assert not list(ss.loops)
    assert not list(ss.energized_loops)
    assert not list(ss.circuits)


@given(**substation_kwargs)
def test_substation_constructor_kwargs(sub_geographical_region, normal_energized_feeders, loops, energized_loops, circuits, **kwargs):
    args = extract_testing_args(locals())
    ss = Substation(**args, **kwargs)
    validate_substation_values(ss, **args, **kwargs)


@given(**substation_kwargs)
def test_substation_creator(sub_geographical_region, normal_energized_feeders, loops, energized_loops, circuits, **kwargs):
    args = extract_testing_args(locals())
    ss = create_substation(**args, **kwargs)
    validate_substation_values(ss, **args, **kwargs)


def validate_substation_values(ss, sub_geographical_region, normal_energized_feeders, loops, energized_loops, circuits, **kwargs):
    verify_equipment_container_constructor_kwargs(ss, **kwargs)
    assert ss.sub_geographical_region == sub_geographical_region
    assert list(ss.feeders) == normal_energized_feeders
    assert list(ss.loops) == loops
    assert list(ss.energized_loops) == energized_loops
    assert list(ss.circuits) == circuits


def test_substation_constructor_args():
    ss = Substation(*substation_args)

    verify_equipment_container_constructor_args(ss)
    assert ss.sub_geographical_region == substation_args[-5]
    assert list(ss.feeders) == substation_args[-4]
    assert list(ss.loops) == substation_args[-3]
    assert list(ss.energized_loops) == substation_args[-2]
    assert list(ss.circuits) == substation_args[-1]


def test_normal_energized_feeders_collection():
    validate_collection_unordered(Substation,
                                  lambda mrid, _: Feeder(mrid),
                                  Substation.num_feeders,
                                  Substation.get_feeder,
                                  Substation.feeders,
                                  Substation.add_feeder,
                                  Substation.remove_feeder,
                                  Substation.clear_feeders)


def test_loops_collection():
    validate_collection_unordered(Substation,
                                  lambda mrid, _: Loop(mrid),
                                  Substation.num_loops,
                                  Substation.get_loop,
                                  Substation.loops,
                                  Substation.add_loop,
                                  Substation.remove_loop,
                                  Substation.clear_loops)


def test_energized_loops_collection():
    validate_collection_unordered(Substation,
                                  lambda mrid, _: Loop(mrid),
                                  Substation.num_energized_loops,
                                  Substation.get_energized_loop,
                                  Substation.energized_loops,
                                  Substation.add_energized_loop,
                                  Substation.remove_energized_loop,
                                  Substation.clear_energized_loops)


def test_circuits_collection():
    validate_collection_unordered(Substation,
                                  lambda mrid, _: Circuit(mrid),
                                  Substation.num_circuits,
                                  Substation.get_circuit,
                                  Substation.circuits,
                                  Substation.add_circuit,
                                  Substation.remove_circuit,
                                  Substation.clear_circuits)


def test_auto_two_way_connections_for_substation_constructor():
    sgr = SubGeographicalRegion()
    nef = Feeder()
    loop = Loop()
    el = Loop()
    c = Circuit()
    p1 = create_substation(sub_geographical_region=sgr)
    p2 = create_substation(normal_energized_feeders=[nef])
    p3 = create_substation(loops=[loop])
    p4 = create_substation(energized_loops=[el])
    p5 = create_substation(circuits=[c])

    assert sgr.get_substation(p1.mrid) == p1
    assert nef.normal_energizing_substation == p2
    assert loop.get_substation(p3.mrid) == p3
    assert el.get_energizing_substation(p4.mrid) == p4
    assert c.get_end_substation(p5.mrid) == p5
