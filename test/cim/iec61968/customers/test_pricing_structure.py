#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds

from test.cim import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61968.common.test_document import document_kwargs, verify_document_constructor_default, verify_document_constructor_kwargs, \
    verify_document_constructor_args, document_args
from zepben.evolve import PricingStructure, Tariff
from zepben.evolve.model.cim.iec61968.customers.create_customers_components import create_pricing_structure

pricing_structure_kwargs = {
    **document_kwargs,
    "tariffs": lists(builds(Tariff), max_size=2),
}

pricing_structure_args = [*document_args, [Tariff()]]


def test_pricing_structure_constructor_default():
    ps = PricingStructure()
    ps2 = create_pricing_structure()
    validate_default_pricing_structure(ps)
    validate_default_pricing_structure(ps2)


def validate_default_pricing_structure(ps):
    verify_document_constructor_default(ps)
    assert not list(ps.tariffs)


@given(**pricing_structure_kwargs)
def test_pricing_structure_constructor_kwargs(tariffs, **kwargs):
    args = extract_testing_args(locals())
    ps = PricingStructure(**args, **kwargs)
    validate_pricing_structure_values(ps, **args, **kwargs)


@given(**pricing_structure_kwargs)
def test_pricing_structure_creator(tariffs, **kwargs):
    args = extract_testing_args(locals())
    ps = create_pricing_structure(**args, **kwargs)
    validate_pricing_structure_values(ps, **args, **kwargs)


def validate_pricing_structure_values(ps, tariffs, **kwargs):
    verify_document_constructor_kwargs(ps, **kwargs)
    assert list(ps.tariffs) == tariffs


def test_pricing_structure_constructor_args():
    # noinspection PyArgumentList
    ps = PricingStructure(*pricing_structure_args)

    verify_document_constructor_args(ps)
    assert list(ps.tariffs) == pricing_structure_args[-1]


def test_tariffs_collection():
    # noinspection PyArgumentList
    validate_collection_unordered(PricingStructure,
                                  lambda mrid, _: Tariff(mrid),
                                  PricingStructure.num_tariffs,
                                  PricingStructure.get_tariff,
                                  PricingStructure.tariffs,
                                  PricingStructure.add_tariff,
                                  PricingStructure.remove_tariff,
                                  PricingStructure.clear_tariffs)
