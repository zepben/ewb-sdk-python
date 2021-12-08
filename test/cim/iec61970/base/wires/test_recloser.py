#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.cim.iec61970.base.wires.test_protected_switch import verify_protected_switch_constructor_default, \
    verify_protected_switch_constructor_kwargs, verify_protected_switch_constructor_args, protected_switch_kwargs, protected_switch_args
from zepben.evolve import Recloser
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_recloser

recloser_kwargs = protected_switch_kwargs
recloser_args = protected_switch_args


def test_recloser_constructor_default():
    verify_protected_switch_constructor_default(Recloser())
    verify_protected_switch_constructor_default(create_recloser())


@given(**recloser_kwargs)
def test_recloser_constructor_kwargs(**kwargs):
    verify_protected_switch_constructor_kwargs(Recloser(**kwargs), **kwargs)


@given(**recloser_kwargs)
def test_recloser_creator(**kwargs):
    verify_protected_switch_constructor_kwargs(create_recloser(**kwargs), **kwargs)


def test_recloser_constructor_args():
    verify_protected_switch_constructor_args(Recloser(*recloser_args))
