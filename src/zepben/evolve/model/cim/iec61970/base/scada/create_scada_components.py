#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *


def create_remote_control(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, control: Control = None) -> RemoteControl:
    """
    RemoteControl(RemotePoint(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    RemotePoint:
    RemoteControl: control
    """
    return RemoteControl(**locals())


def create_remote_source(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, measurement: Measurement = None) -> RemoteSource:
    """
    RemoteSource(RemotePoint(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    RemotePoint:
    RemoteSource: measurement
    """
    return RemoteSource(**locals())
