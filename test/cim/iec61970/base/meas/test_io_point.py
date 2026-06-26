#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs
from zepben.ewb import IoPoint


def verify_io_point_constructor_default(ip: IoPoint):
    verify_identified_object_constructor_default(ip)


def verify_io_point_constructor_kwargs(ip: IoPoint, **kwargs):
    verify_identified_object_constructor_kwargs(ip, **kwargs)
