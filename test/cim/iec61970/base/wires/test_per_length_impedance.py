#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.wires.test_per_length_line_parameter import per_length_line_parameter_kwargs, verify_per_length_line_parameter_constructor_default, \
    verify_per_length_line_parameter_constructor_kwargs, verify_per_length_line_parameter_constructor_args, per_length_line_parameter_args
from zepben.evolve import PerLengthImpedance

per_length_impedance_kwargs = per_length_line_parameter_kwargs
per_length_impedance_args = per_length_line_parameter_args


def verify_per_length_impedance_constructor_default(pli: PerLengthImpedance):
    verify_per_length_line_parameter_constructor_default(pli)


def verify_per_length_impedance_constructor_kwargs(pli: PerLengthImpedance, **kwargs):
    verify_per_length_line_parameter_constructor_kwargs(pli, **kwargs)


def verify_per_length_impedance_constructor_args(pli: PerLengthImpedance):
    verify_per_length_line_parameter_constructor_args(pli)
