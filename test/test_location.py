#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve import PositionPoint, TownDetail


def test_create_positionpoints():
    x = PositionPoint(1.0, 2.0)
    assert x.longitude == 1.0
    assert x.latitude == 2.0
    y = PositionPoint(x_position=1.0, y_position=2.0)
    z = PositionPoint(1.0, y_position=2.0)
    assert x == y == z
    with pytest.raises(TypeError):
        x = PositionPoint()
    with pytest.raises(TypeError):
        x = PositionPoint(1.0)
    with pytest.raises(TypeError):
        x = PositionPoint(y_position=2.0)
    with pytest.raises(ValueError, match="Longitude is out of range. Expected -180 to 180, got -181.0."):
        x = PositionPoint(-181.0, 0)
    with pytest.raises(ValueError, match="Longitude is out of range. Expected -180 to 180, got 181.0."):
        x = PositionPoint(181.0, 0)
    with pytest.raises(ValueError, match="Latitude is out of range. Expected -90 to 90, got -91.0."):
        x = PositionPoint(0, -91.0)
    with pytest.raises(ValueError, match="Latitude is out of range. Expected -90 to 90, got 91.0."):
        x = PositionPoint(0, 91.0)


def test_create_towndetail():
    td = TownDetail("name", "state")
    assert td.name == "name"
    assert td.state_or_province == "state"
    td.state_or_province = "state2"
    td.name = "name2"
    assert td.name == "name2"
    assert td.state_or_province == "state2"
    td = TownDetail(state_or_province="state")
    assert td.name == ""
    assert td.state_or_province == "state"

