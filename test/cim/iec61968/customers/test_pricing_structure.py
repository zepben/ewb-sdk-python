#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds

from cim.collection_validator import validate_collection_unordered
from cim.iec61968.common.test_document import document_kwargs, verify_document_constructor_default, verify_document_constructor_kwargs, \
    verify_document_constructor_args, document_args
from zepben.evolve import PricingStructure, Tariff

pricing_structure_kwargs = {
    **document_kwargs,
    "tariffs": lists(builds(Tariff), max_size=2),
}

pricing_structure_args = [*document_args, [Tariff()]]


def test_pricing_structure_constructor_default():
    ps = PricingStructure()

    verify_document_constructor_default(ps)
    assert not list(ps.tariffs)


@given(**pricing_structure_kwargs)
def test_pricing_structure_constructor_kwargs(tariffs, **kwargs):
    # noinspection PyArgumentList
    ps = PricingStructure(
        tariffs=tariffs,
        **kwargs
    )

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
