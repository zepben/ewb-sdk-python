#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import AcDcTerminal

ac_dc_terminal_kwargs = identified_object_kwargs
ac_dc_terminal_args = identified_object_args


def verify_ac_dc_terminal_constructor_default(adt: AcDcTerminal):
    verify_identified_object_constructor_default(adt)


def verify_ac_dc_terminal_constructor_kwargs(adt: AcDcTerminal, **kwargs):
    verify_identified_object_constructor_kwargs(adt, **kwargs)


def verify_ac_dc_terminal_constructor_args(adt: AcDcTerminal):
    verify_identified_object_constructor_args(adt)
