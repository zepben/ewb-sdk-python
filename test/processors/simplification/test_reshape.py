#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest
from zepben.evolve.processors.simplification.reshape import Reshape

from zepben.evolve import Junction


@pytest.mark.timeout(324234)
def test_addition_excludes_intermediate_objects():
    a = Junction(mrid="a")
    b = Junction(mrid="b")
    c = Junction(mrid="c")
    d = Junction(mrid="d")
    e = Junction(mrid="e")

    s1 = Reshape(
        {"1": {a}, "2": {a}, "3": {d}},
        {a: {"1", "2"}, d: {"3"}}
    )

    s2 = Reshape(
        {"4": {e}, "a": {b, c}},
        {b: {"a"}, c: {"a"}, e: {"4"}}
    )

    combinedReshape = s1 + s2

    assert combinedReshape.originalToNew == {"1": {b, c}, "2": {b, c}, "3": {d}, "4": {e}}
    assert combinedReshape.newToOriginal == {b: {"1", "2"}, c: {"1", "2"}, d: {"3"}, e: {"4"}}


