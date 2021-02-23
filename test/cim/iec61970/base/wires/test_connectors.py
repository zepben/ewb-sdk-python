#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.cim.constructor_validation import verify_connector_constructor, cn_kwargs, cn_args, verify_cn_args
from zepben.evolve import BusbarSection


bbs_kwargs = cn_kwargs
bbs_args = cn_args


@given(**bbs_kwargs)
def test_busbarsection_constructor_kwargs(**kwargs):
    verify_connector_constructor(BusbarSection, **kwargs)
    bbs = BusbarSection()
    assert bbs.mrid
    bbs = BusbarSection(mrid="test")
    assert bbs.mrid == "test"
    bbs = BusbarSection("test2")
    assert bbs.mrid == "test2"


def test_busbarsection_constructor_args():
    bbs = BusbarSection(*bbs_args)
    verify_cn_args(bbs)
