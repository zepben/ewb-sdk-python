#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from _pytest.python_api import raises

from zepben.evolve import RelaySetting, UnitSymbol


def test_relay_setting_value_must_be_real():
    with raises(ValueError, match=r"RelaySetting.value must be a real number. Provided: None"):
        RelaySetting(unit_symbol=UnitSymbol.METRES, value=None)
    with raises(ValueError, match=r"RelaySetting.value must be a real number. Provided: nan"):
        RelaySetting(unit_symbol=UnitSymbol.METRES, value=float('nan'), name="threshold name")
    with raises(TypeError, match=r"must be real number, not str"):
        RelaySetting(unit_symbol=UnitSymbol.METRES, value='string', name="threshold name")

    rs = RelaySetting(unit_symbol=UnitSymbol.METRES, value=0.0, name="threshold name")
    assert rs.value == 0.0
    rs = RelaySetting(unit_symbol=UnitSymbol.METRES, value=1, name="threshold name")
    assert rs.value == 1
