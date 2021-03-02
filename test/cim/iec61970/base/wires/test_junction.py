#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/
from hypothesis import given

from test.cim.constructor_validation import verify_connector_constructor, cn_kwargs, cn_args, verify_cn_args
from zepben.evolve import Junction


jnc_kwargs = cn_kwargs
jnc_args = cn_args


@given(**jnc_kwargs)
def test_junction_constructor_kwargs(**kwargs):
    verify_connector_constructor(Junction, **kwargs)
    jnc = Junction()
    assert jnc.mrid
    jnc = Junction(mrid="test")
    assert jnc.mrid == "test"
    jnc = Junction("test2")
    assert jnc.mrid == "test2"


def test_junction_constructor_args():
    jnc = Junction(*jnc_args)
    verify_cn_args(jnc)




