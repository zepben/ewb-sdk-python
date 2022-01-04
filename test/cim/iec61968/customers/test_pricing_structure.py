#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds, data

from test.cim.common_testing_functions import verify
from test.cim.collection_verifier import verify_collection_unordered
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
    verify_default_pricing_structure(ps)
    verify_default_pricing_structure(ps2)


def verify_default_pricing_structure(ps):
    verify_document_constructor_default(ps)
    assert not list(ps.tariffs)


# noinspection PyShadowingNames
@given(data())
def test_pricing_structure_constructor_kwargs(data):
    verify(
        [PricingStructure, create_pricing_structure],
        data, pricing_structure_kwargs, verify_pricing_structure_values
    )


def verify_pricing_structure_values(ps, tariffs, **kwargs):
    verify_document_constructor_kwargs(ps, **kwargs)
    assert list(ps.tariffs) == tariffs


def test_pricing_structure_constructor_args():
    # noinspection PyArgumentList
    ps = PricingStructure(*pricing_structure_args)

    verify_document_constructor_args(ps)
    assert list(ps.tariffs) == pricing_structure_args[-1]


def test_tariffs_collection():
    # noinspection PyArgumentList
    verify_collection_unordered(PricingStructure,
                                lambda mrid, _: Tariff(mrid),
                                PricingStructure.num_tariffs,
                                PricingStructure.get_tariff,
                                PricingStructure.tariffs,
                                PricingStructure.add_tariff,
                                PricingStructure.remove_tariff,
                                PricingStructure.clear_tariffs)
