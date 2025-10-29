#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds
from zepben.ewb import Substation
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion
from zepben.ewb.model.cim.iec61970.base.core.geographical_region import GeographicalRegion

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.private_collection_validator import validate_unordered_1234567890

sub_geographical_region_kwargs = {
    **identified_object_kwargs,
    "geographical_region": builds(GeographicalRegion),
    "substations": lists(builds(Substation), max_size=2)
}

sub_geographical_region_args = [*identified_object_args, GeographicalRegion(), [Substation()]]


def test_sub_geographical_region_constructor_default():
    sgr = SubGeographicalRegion()

    verify_identified_object_constructor_default(sgr)
    assert not list(sgr.substations)


@given(**sub_geographical_region_kwargs)
def test_sub_geographical_region_constructor_kwargs(geographical_region, substations, **kwargs):
    sgr = SubGeographicalRegion(geographical_region=geographical_region,
                                substations=substations,
                                **kwargs)

    verify_identified_object_constructor_kwargs(sgr, **kwargs)
    assert sgr.geographical_region == geographical_region
    assert list(sgr.substations) == substations


from pytest import mark
@mark.skip(reason="Args are deprecated")
def test_sub_geographical_region_constructor_args():
    sgr = SubGeographicalRegion(*sub_geographical_region_args)

    verify_identified_object_constructor_args(sgr)
    assert sub_geographical_region_args[-2:] == [
        sgr.geographical_region,
        list(sgr.substations)
    ]


def test_substations_collection():
    validate_unordered_1234567890(
        SubGeographicalRegion,
        lambda mrid: Substation(mrid),
        SubGeographicalRegion.substations,
        SubGeographicalRegion.num_substations,
        SubGeographicalRegion.get_substation,
        SubGeographicalRegion.add_substation,
        SubGeographicalRegion.remove_substation,
        SubGeographicalRegion.clear_substations
    )
