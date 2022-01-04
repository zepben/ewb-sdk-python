#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from cim.common_testing_functions import verify
from test.cim.iec61968.assetinfo.test_wire_info import wire_info_kwargs, verify_wire_info_constructor_default, \
    verify_wire_info_constructor_kwargs, verify_wire_info_constructor_args, wire_info_args
from zepben.evolve import CableInfo
from zepben.evolve.model.cim.iec61968.assetinfo.create_asset_info_components import create_cable_info

cable_info_kwargs = wire_info_kwargs
cable_info_args = wire_info_args


def test_cable_info_constructor_default():
    verify_wire_info_constructor_default(CableInfo())
    verify_wire_info_constructor_default(create_cable_info())


# noinspection PyShadowingNames
@given(data())
def test_cable_info_constructor_kwargs(data):
    verify(
        [CableInfo, create_cable_info],
        data, cable_info_kwargs, verify_wire_info_constructor_kwargs
    )


def test_cable_info_constructor_args():
    # noinspection PyArgumentList
    verify_wire_info_constructor_args(CableInfo(*cable_info_args))
