#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import datetime

from hypothesis.strategies import builds, datetimes, none

from cim.iec61968.common.test_document import document_kwargs, verify_document_constructor_default, \
    verify_document_constructor_kwargs, verify_document_constructor_args, document_args
from zepben.ewb.model.cim.iec61968.common.agreement import Agreement
from zepben.ewb.model.cim.iec61970.base.domain.date_time_interval import DateTimeInterval


MIN_MAX = datetime.datetime(2020, 1, 1)

agreement_kwargs = {
    **document_kwargs,
    'validity_interval': builds(DateTimeInterval, start=datetimes(max_value=MIN_MAX) , end=none()),
}

agreement_args = [*document_args, builds(DateTimeInterval, start=datetimes(max_value=MIN_MAX), end=none())]


def verify_agreement_constructor_default(a: Agreement):
    verify_document_constructor_default(a)


def verify_agreement_constructor_kwargs(a: Agreement, validity_interval, **kwargs):
    assert a.validity_interval == validity_interval
    verify_document_constructor_kwargs(a, **kwargs)


def verify_agreement_constructor_args(a: Agreement):
    verify_document_constructor_args(a)
    assert agreement_args[-1:] == [
        a.validity_interval
    ]
