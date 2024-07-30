#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from cim.iec61968.common.test_document import document_kwargs, verify_document_constructor_default, verify_document_constructor_kwargs, \
    verify_document_constructor_args, document_args
from zepben.evolve import Tariff

tariff_kwargs = document_kwargs
tariff_args = document_args


def test_tariff_constructor_default():
    verify_document_constructor_default(Tariff())


@given(**tariff_kwargs)
def test_tariff_constructor_kwargs(**kwargs):
    # noinspection PyArgumentList
    verify_document_constructor_kwargs(Tariff(**kwargs), **kwargs)


def test_tariff_constructor_args():
    # noinspection PyArgumentList
    verify_document_constructor_args(Tariff(*tariff_args))
