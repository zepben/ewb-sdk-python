#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime

import pytest

from zepben.ewb.model.cim.iec61970.base.domain.date_time_interval import DateTimeInterval

datetime_interval_kwargs = {
    'start': datetime(2000, 1, 1),
    'end': datetime(2005, 1, 1),
}


def test_datetime_interval_constructor_default():
    with pytest.raises(ValueError, match="You must provide a start or end time."):
        # noinspection PyUnusedLocal
        dti = DateTimeInterval()  # noqa: F841

    a = DateTimeInterval(start=datetime(2020, 1, 1))
    b = DateTimeInterval(end=datetime(2020, 1, 1))
    assert a.end is None
    assert b.start is None


def test_datetime_interval_constructor_kwargs():
    dti = DateTimeInterval(**datetime_interval_kwargs)

    assert dti.start == datetime_interval_kwargs['start']
    assert dti.end == datetime_interval_kwargs['end']


def test_must_have_a_valid_start_or_end():
    with pytest.raises(ValueError, match="The start time must be before the end time."):
        DateTimeInterval(start=datetime(2020, 12, 1), end=datetime(2020, 1, 1))
