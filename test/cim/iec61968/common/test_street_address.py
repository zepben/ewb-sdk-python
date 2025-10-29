#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, text
from zepben.ewb.model.cim.iec61968.common.street_address import StreetAddress
from zepben.ewb.model.cim.iec61968.common.street_detail import StreetDetail
from zepben.ewb.model.cim.iec61968.common.town_detail import TownDetail

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE

street_address_kwargs = {
    "postal_code": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "town_detail": builds(TownDetail),
    "po_box": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "street_detail": builds(StreetDetail)
}

street_address_args = ["a", TownDetail(), "b", StreetDetail()]


def test_street_address_constructor_default():
    sa = StreetAddress()

    assert sa.postal_code is None
    assert not sa.town_detail


@given(**street_address_kwargs)
def test_street_address_constructor_kwargs(postal_code, town_detail, po_box, street_detail, **kwargs):
    assert not kwargs

    sa = StreetAddress(postal_code=postal_code, town_detail=town_detail, po_box=po_box, street_detail=street_detail)

    assert sa.postal_code == postal_code
    assert sa.town_detail == town_detail
    assert sa.po_box == po_box
    assert sa.street_detail == street_detail


from pytest import mark
@mark.skip(reason="Args are deprecated")
def test_street_address_constructor_args():
    sa = StreetAddress(*street_address_args)

    assert street_address_args[-4:] == [
        sa.postal_code,
        sa.town_detail,
        sa.po_box,
        sa.street_detail
    ]
