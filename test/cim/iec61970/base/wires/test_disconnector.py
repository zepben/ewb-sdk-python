#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.cim.iec61970.base.wires.test_switch import verify_switch_constructor_default, verify_switch_constructor_kwargs, verify_switch_constructor_args, \
    switch_kwargs, switch_args
from zepben.evolve import Disconnector
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_disconnector

disconnector_kwargs = switch_kwargs
disconnector_args = switch_args


def test_disconnector_constructor_default():
    verify_switch_constructor_default(Disconnector())
    verify_switch_constructor_default(create_disconnector())


@given(**disconnector_kwargs)
def test_disconnector_constructor_kwargs(**kwargs):
    verify_switch_constructor_kwargs(Disconnector(**kwargs), **kwargs)


@given(**disconnector_kwargs)
def test_disconnector_creator(**kwargs):
    verify_switch_constructor_kwargs(create_disconnector(**kwargs), **kwargs)


def test_disconnector_constructor_args():
    verify_switch_constructor_args(Disconnector(*disconnector_args))
