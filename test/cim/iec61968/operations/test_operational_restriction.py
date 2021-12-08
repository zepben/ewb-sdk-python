#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds

from test.cim.extract_testing_args import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61968.common.test_document import document_kwargs, verify_document_constructor_default, verify_document_constructor_kwargs, \
    verify_document_constructor_args, document_args
from zepben.evolve import OperationalRestriction, Equipment
from zepben.evolve.model.cim.iec61968.operations.create_operational_restriction_components import create_operational_restriction

operational_restriction_kwargs = {
    **document_kwargs,
    "equipment": lists(builds(Equipment), max_size=2),
}

operational_restriction_args = [*document_args, [Equipment()]]


def test_operational_restriction_constructor_default():
    or_ = OperationalRestriction()
    or_2 = create_operational_restriction()
    validate_default_operational_restriction(or_)
    validate_default_operational_restriction(or_2)


def validate_default_operational_restriction(or_):
    verify_document_constructor_default(or_)
    assert not list(or_.equipment)


@given(**operational_restriction_kwargs)
def test_operational_restriction_constructor_kwargs(equipment, **kwargs):
    args = extract_testing_args(locals())
    or_ = OperationalRestriction(**args, **kwargs)
    validate_operational_restriction_values(or_, **args, **kwargs)


@given(**operational_restriction_kwargs)
def test_operational_restriction_creator(equipment, **kwargs):
    args = extract_testing_args(locals())
    or_ = create_operational_restriction(**args, **kwargs)
    validate_operational_restriction_values(or_, **args, **kwargs)


def validate_operational_restriction_values(or_, equipment, **kwargs):
    verify_document_constructor_kwargs(or_, **kwargs)
    assert list(or_.equipment) == equipment


def test_operational_restriction_constructor_args():
    # noinspection PyArgumentList
    or_ = OperationalRestriction(*operational_restriction_args)

    verify_document_constructor_args(or_)
    assert list(or_.equipment) == operational_restriction_args[-1]


def test_equipment_collection():
    # noinspection PyArgumentList
    validate_collection_unordered(OperationalRestriction,
                                  lambda mrid, _: Equipment(mrid),
                                  OperationalRestriction.num_equipment,
                                  OperationalRestriction.get_equipment,
                                  OperationalRestriction.equipment,
                                  OperationalRestriction.add_equipment,
                                  OperationalRestriction.remove_equipment,
                                  OperationalRestriction.clear_equipment)
