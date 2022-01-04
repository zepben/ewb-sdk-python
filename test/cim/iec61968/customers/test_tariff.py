#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import data

from test.cim.common_testing_functions import verify
from test.cim.iec61968.common.test_document import document_kwargs, verify_document_constructor_default, verify_document_constructor_kwargs, \
    verify_document_constructor_args, document_args
from zepben.evolve import Tariff
from zepben.evolve.model.cim.iec61968.customers.create_customers_components import create_tariff

tariff_kwargs = document_kwargs
tariff_args = document_args


def test_tariff_constructor_default():
    verify_document_constructor_default(Tariff())
    verify_document_constructor_default(create_tariff())


# noinspection PyShadowingNames
@given(data())
def test_tariff_constructor_kwargs(data):
    verify(
        [Tariff, create_tariff],
        data, tariff_kwargs, verify_document_constructor_kwargs
    )


def test_tariff_constructor_args():
    # noinspection PyArgumentList
    verify_document_constructor_args(Tariff(*tariff_args))
