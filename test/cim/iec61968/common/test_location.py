#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds

from cim.collection_validator import validate_collection_ordered
from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.cim_creators import create_position_point
from zepben.evolve import Location, PositionPoint, StreetAddress

location_kwargs = {
    **identified_object_kwargs,
    "main_address": builds(StreetAddress),
    "position_points": lists(create_position_point(), max_size=2),
}

# noinspection PyArgumentList
location_args = [*identified_object_args, StreetAddress(), [PositionPoint(1.1, 2.2)]]


def test_location_constructor_default():
    loc = Location()

    verify_identified_object_constructor_default(loc)
    assert not loc.main_address
    assert not list(loc.points)


@given(**location_kwargs)
def test_location_constructor_kwargs(main_address, position_points, **kwargs):
    loc = Location(main_address=main_address, position_points=position_points, **kwargs)

    verify_identified_object_constructor_kwargs(loc, **kwargs)
    assert loc.main_address == main_address
    assert list(loc.points) == position_points


def test_location_constructor_args():
    loc = Location(*location_args)

    verify_identified_object_constructor_args(loc)
    assert loc.main_address == location_args[-2]
    assert list(loc.points) == location_args[-1]


def test_points_collection():
    # noinspection PyArgumentList
    validate_collection_ordered(Location,
                                lambda i, _: PositionPoint(i, i),
                                Location.num_points,
                                Location.get_point,
                                Location.points,
                                Location.add_point,
                                Location.insert_point,
                                Location.remove_point,
                                Location.clear_points)
