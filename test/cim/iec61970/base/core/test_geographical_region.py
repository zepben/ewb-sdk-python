#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds

from test.cim import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import GeographicalRegion, SubGeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.create_core_components import create_geographical_region

geographical_region_kwargs = {
    **identified_object_kwargs,
    "sub_geographical_regions": lists(builds(SubGeographicalRegion), max_size=2)
}

geographical_region_args = [*identified_object_args, [SubGeographicalRegion()]]


def test_geographical_region_constructor_default():
    gr = GeographicalRegion()
    gr2 = create_geographical_region()
    validate_default_geographical_region(gr)
    validate_default_geographical_region(gr2)


def validate_default_geographical_region(gr):
    verify_identified_object_constructor_default(gr)
    assert not list(gr.sub_geographical_regions)


@given(**geographical_region_kwargs)
def test_geographical_region_constructor_kwargs(sub_geographical_regions, **kwargs):
    args = extract_testing_args(locals())
    gr = GeographicalRegion(**args, **kwargs)
    validate_geographical_region_values(gr, **args, **kwargs)


@given(**geographical_region_kwargs)
def test_geographical_region_creator(sub_geographical_regions, **kwargs):
    args = extract_testing_args(locals())
    gr = create_geographical_region(**args, **kwargs)
    validate_geographical_region_values(gr, **args, **kwargs)


def validate_geographical_region_values(gr, sub_geographical_regions, **kwargs):
    verify_identified_object_constructor_kwargs(gr, **kwargs)
    assert list(gr.sub_geographical_regions) == sub_geographical_regions


def test_geographical_region_constructor_args():
    gr = GeographicalRegion(*geographical_region_args)

    verify_identified_object_constructor_args(gr)
    assert list(gr.sub_geographical_regions) == geographical_region_args[-1]


def test_sub_geographical_regions_collection():
    validate_collection_unordered(GeographicalRegion,
                                  lambda mrid, _: SubGeographicalRegion(mrid),
                                  GeographicalRegion.num_sub_geographical_regions,
                                  GeographicalRegion.get_sub_geographical_region,
                                  GeographicalRegion.sub_geographical_regions,
                                  GeographicalRegion.add_sub_geographical_region,
                                  GeographicalRegion.remove_sub_geographical_region,
                                  GeographicalRegion.clear_sub_geographical_regions)
