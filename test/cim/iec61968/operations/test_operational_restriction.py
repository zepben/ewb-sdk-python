#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds

from util import mrid_strategy
from zepben.ewb import OperationalRestriction, Equipment, generate_id

from cim.iec61968.common.test_document import document_kwargs, verify_document_constructor_default, verify_document_constructor_kwargs, \
    verify_document_constructor_args, document_args
from cim.private_collection_validator import validate_unordered

operational_restriction_kwargs = {
    **document_kwargs,
    "equipment": lists(builds(Equipment, mrid=mrid_strategy), max_size=2),
}

operational_restriction_args = [*document_args, [Equipment(mrid=generate_id())]]


def test_operational_restriction_constructor_default():
    or_ = OperationalRestriction(mrid=generate_id())

    verify_document_constructor_default(or_)
    assert not list(or_.equipment)


@given(**operational_restriction_kwargs)
def test_operational_restriction_constructor_kwargs(equipment, **kwargs):
    or_ = OperationalRestriction(
        equipment=equipment,
        **kwargs
    )

    verify_document_constructor_kwargs(or_, **kwargs)
    assert list(or_.equipment) == equipment


def test_operational_restriction_constructor_args():
    or_ = OperationalRestriction(*operational_restriction_args)

    verify_document_constructor_args(or_)
    assert operational_restriction_args[-1:] == [
        list(or_.equipment)
    ]


def test_equipment_collection():
    validate_unordered(
        OperationalRestriction,
        lambda mrid: Equipment(mrid),
        OperationalRestriction.equipment,
        OperationalRestriction.num_equipment,
        OperationalRestriction.get_equipment,
        OperationalRestriction.add_equipment,
        OperationalRestriction.remove_equipment,
        OperationalRestriction.clear_equipment
    )
