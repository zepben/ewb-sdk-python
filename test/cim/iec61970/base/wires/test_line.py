#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_equipment_container import verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs
from zepben.ewb import Line


def verify_line_constructor_default(line: Line):
    verify_equipment_container_constructor_default(line)


def verify_line_constructor_kwargs(line: Line, **kwargs):
    verify_equipment_container_constructor_kwargs(line, **kwargs)
