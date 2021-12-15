#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds

from test.cim.extract_testing_args import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import SubGeographicalRegion, Substation, GeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.create_core_components import create_sub_geographical_region

sub_geographical_region_kwargs = {
    **identified_object_kwargs,
    "geographical_region": builds(GeographicalRegion),
    "substations": lists(builds(Substation), max_size=2)
}

sub_geographical_region_args = [*identified_object_args, GeographicalRegion(), [Substation()]]


def test_sub_geographical_region_constructor_default():
    sgr = SubGeographicalRegion()
    sgr2 = create_sub_geographical_region()
    validate_default_sub_geographical_region(sgr)
    validate_default_sub_geographical_region(sgr2)


def validate_default_sub_geographical_region(sgr):
    verify_identified_object_constructor_default(sgr)
    assert not list(sgr.substations)


@given(**sub_geographical_region_kwargs)
def test_sub_geographical_region_constructor_kwargs(geographical_region, substations, **kwargs):
    args = extract_testing_args(locals())
    sgr = SubGeographicalRegion(**args, **kwargs)
    validate_sub_geographical_region_values(sgr, **args, **kwargs)


@given(**sub_geographical_region_kwargs)
def test_sub_geographical_region_constructor_kwargs(geographical_region, substations, **kwargs):
    args = extract_testing_args(locals())
    sgr = create_sub_geographical_region(**args, **kwargs)
    validate_sub_geographical_region_values(sgr, **args, **kwargs)


def validate_sub_geographical_region_values(sgr, geographical_region, substations, **kwargs):
    verify_identified_object_constructor_kwargs(sgr, **kwargs)
    assert sgr.geographical_region == geographical_region
    assert list(sgr.substations) == substations


def test_sub_geographical_region_constructor_args():
    sgr = SubGeographicalRegion(*sub_geographical_region_args)

    verify_identified_object_constructor_args(sgr)
    assert sgr.geographical_region == sub_geographical_region_args[-2]
    assert list(sgr.substations) == sub_geographical_region_args[-1]


def test_substations_collection():
    validate_collection_unordered(SubGeographicalRegion,
                                  lambda mrid, _: Substation(mrid),
                                  SubGeographicalRegion.num_substations,
                                  SubGeographicalRegion.get_substation,
                                  SubGeographicalRegion.substations,
                                  SubGeographicalRegion.add_substation,
                                  SubGeographicalRegion.remove_substation,
                                  SubGeographicalRegion.clear_substations)


def test_auto_two_way_connections_for_sub_geographical_region_constructor():
    gr = GeographicalRegion()
    s = Substation()
    p = create_sub_geographical_region(geographical_region=gr, substations=[s])

    assert gr.get_sub_geographical_region(p.mrid) == p
    assert s.sub_geographical_region == p

