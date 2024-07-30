#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds

from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import GeographicalRegion, SubGeographicalRegion

geographical_region_kwargs = {
    **identified_object_kwargs,
    "sub_geographical_regions": lists(builds(SubGeographicalRegion), max_size=2)
}

geographical_region_args = [*identified_object_args, [SubGeographicalRegion()]]


def test_geographical_region_constructor_default():
    gr = GeographicalRegion()

    verify_identified_object_constructor_default(gr)
    assert not list(gr.sub_geographical_regions)


@given(**geographical_region_kwargs)
def test_geographical_region_constructor_kwargs(sub_geographical_regions, **kwargs):
    gr = GeographicalRegion(sub_geographical_regions=sub_geographical_regions, **kwargs)

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
