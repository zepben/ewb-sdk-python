#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import PerLengthLineParameter

per_length_line_parameter_kwargs = identified_object_kwargs
per_length_line_parameter_args = identified_object_args


def verify_per_length_line_parameter_constructor_default(pllp: PerLengthLineParameter):
    verify_identified_object_constructor_default(pllp)


def verify_per_length_line_parameter_constructor_kwargs(pllp: PerLengthLineParameter, **kwargs):
    verify_identified_object_constructor_kwargs(pllp, **kwargs)


def verify_per_length_line_parameter_constructor_args(pllp: PerLengthLineParameter):
    verify_identified_object_constructor_args(pllp)
