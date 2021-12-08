#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.cim.iec61968.assetinfo.test_wire_info import wire_info_kwargs, verify_wire_info_constructor_default, \
    verify_wire_info_constructor_kwargs, verify_wire_info_constructor_args, wire_info_args
from zepben.evolve import OverheadWireInfo
from zepben.evolve.model.cim.iec61968.assetinfo.create_asset_info_components import create_overhead_wire_info

overhead_wire_info_kwargs = wire_info_kwargs
overhead_wire_info_args = wire_info_args


def test_overhead_wire_info_constructor_default():
    verify_wire_info_constructor_default(OverheadWireInfo())
    verify_wire_info_constructor_default(create_overhead_wire_info())


@given(**overhead_wire_info_kwargs)
def test_overhead_wire_info_constructor_kwargs(**kwargs):
    # noinspection PyArgumentList
    verify_wire_info_constructor_kwargs(OverheadWireInfo(**kwargs), **kwargs)


@given(**overhead_wire_info_kwargs)
def test_overhead_wire_info_creator(**kwargs):
    # noinspection PyArgumentList
    verify_wire_info_constructor_kwargs(create_overhead_wire_info(**kwargs), **kwargs)


def test_overhead_wire_info_constructor_args():
    # noinspection PyArgumentList
    verify_wire_info_constructor_args(OverheadWireInfo(*overhead_wire_info_args))
