#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import sub_geographical_region_kwargs
from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs
from cim.private_collection_validator import validate_unordered
from zepben.ewb import Substation, generate_id
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion


def test_sub_geographical_region_constructor_default():
    sgr = SubGeographicalRegion(mrid=generate_id())

    verify_identified_object_constructor_default(sgr)
    assert not list(sgr.substations)


@given(**sub_geographical_region_kwargs())
def test_sub_geographical_region_constructor_kwargs(geographical_region, substations, **kwargs):
    sgr = SubGeographicalRegion(
        geographical_region=geographical_region,
        substations=substations,
        **kwargs,
    )

    verify_identified_object_constructor_kwargs(sgr, **kwargs)
    assert sgr.geographical_region == geographical_region
    assert list(sgr.substations) == substations


def test_substations_collection():
    validate_unordered(
        SubGeographicalRegion,
        lambda mrid: Substation(mrid),
        SubGeographicalRegion.substations,
        SubGeographicalRegion.num_substations,
        SubGeographicalRegion.get_substation,
        SubGeographicalRegion.add_substation,
        SubGeographicalRegion.remove_substation,
        SubGeographicalRegion.clear_substations,
    )
