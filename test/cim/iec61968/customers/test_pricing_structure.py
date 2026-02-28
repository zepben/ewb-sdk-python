#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds, text

from cim.cim_creators import ALPHANUM
from util import mrid_strategy
from zepben.ewb import PricingStructure, Tariff, generate_id

from cim.iec61968.common.test_document import document_kwargs, verify_document_constructor_default, verify_document_constructor_kwargs, \
    verify_document_constructor_args, document_args
from cim.private_collection_validator import validate_unordered

pricing_structure_kwargs = {
    **document_kwargs,
    "tariffs": lists(builds(Tariff, mrid=mrid_strategy), max_size=2),
    "code": text(alphabet=ALPHANUM),
}

pricing_structure_args = [*document_args, [Tariff(mrid=generate_id())], "asd"]


def test_pricing_structure_constructor_default():
    ps = PricingStructure(mrid=generate_id())

    verify_document_constructor_default(ps)
    assert not list(ps.tariffs)
    assert ps.code is None


@given(**pricing_structure_kwargs)
def test_pricing_structure_constructor_kwargs(tariffs, code, **kwargs):
    ps = PricingStructure(
        tariffs=tariffs,
        code=code,
        **kwargs
    )

    verify_document_constructor_kwargs(ps, **kwargs)
    assert list(ps.tariffs) == tariffs
    assert ps.code == code


def test_pricing_structure_constructor_args():
    ps = PricingStructure(*pricing_structure_args)

    verify_document_constructor_args(ps)
    assert pricing_structure_args[-2:] == [
               list(ps.tariffs),
                ps.code
           ]


def test_tariffs_collection():
    validate_unordered(
        PricingStructure,
        lambda mrid: Tariff(mrid),
        PricingStructure.tariffs,
        PricingStructure.num_tariffs,
        PricingStructure.get_tariff,
        PricingStructure.add_tariff,
        PricingStructure.remove_tariff,
        PricingStructure.clear_tariffs
    )
