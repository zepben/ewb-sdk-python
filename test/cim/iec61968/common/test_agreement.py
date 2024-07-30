#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61968.common.test_document import document_kwargs, verify_document_constructor_default, \
    verify_document_constructor_kwargs, verify_document_constructor_args, document_args
from zepben.evolve import Agreement

agreement_kwargs = document_kwargs
agreement_args = document_args


def verify_agreement_constructor_default(a: Agreement):
    verify_document_constructor_default(a)


def verify_agreement_constructor_kwargs(a: Agreement, **kwargs):
    verify_document_constructor_kwargs(a, **kwargs)


def verify_agreement_constructor_args(a: Agreement):
    verify_document_constructor_args(a)
