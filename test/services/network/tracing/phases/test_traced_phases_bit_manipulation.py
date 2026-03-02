#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb import SinglePhaseKind
from zepben.ewb.services.network.tracing.phases.traced_phases_bit_manipulation import TracedPhasesBitManipulation


def test_get():
    assert TracedPhasesBitManipulation().get(0x0001, SinglePhaseKind.A) == SinglePhaseKind.A
    assert TracedPhasesBitManipulation().get(0x0002, SinglePhaseKind.A) == SinglePhaseKind.B
    assert TracedPhasesBitManipulation().get(0x0004, SinglePhaseKind.A) == SinglePhaseKind.C
    assert TracedPhasesBitManipulation().get(0x0008, SinglePhaseKind.A) == SinglePhaseKind.N

    assert TracedPhasesBitManipulation().get(0x0010, SinglePhaseKind.B) == SinglePhaseKind.A
    assert TracedPhasesBitManipulation().get(0x0020, SinglePhaseKind.B) == SinglePhaseKind.B
    assert TracedPhasesBitManipulation().get(0x0040, SinglePhaseKind.B) == SinglePhaseKind.C
    assert TracedPhasesBitManipulation().get(0x0080, SinglePhaseKind.B) == SinglePhaseKind.N

    assert TracedPhasesBitManipulation().get(0x0100, SinglePhaseKind.C) == SinglePhaseKind.A
    assert TracedPhasesBitManipulation().get(0x0200, SinglePhaseKind.C) == SinglePhaseKind.B
    assert TracedPhasesBitManipulation().get(0x0400, SinglePhaseKind.C) == SinglePhaseKind.C
    assert TracedPhasesBitManipulation().get(0x0800, SinglePhaseKind.C) == SinglePhaseKind.N

    assert TracedPhasesBitManipulation().get(0x1000, SinglePhaseKind.N) == SinglePhaseKind.A
    assert TracedPhasesBitManipulation().get(0x2000, SinglePhaseKind.N) == SinglePhaseKind.B
    assert TracedPhasesBitManipulation().get(0x4000, SinglePhaseKind.N) == SinglePhaseKind.C
    assert TracedPhasesBitManipulation().get(0x8000, SinglePhaseKind.N) == SinglePhaseKind.N


def test_set():
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.A, SinglePhaseKind.A) == 0x0001
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.A, SinglePhaseKind.B) == 0x0002
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.A, SinglePhaseKind.C) == 0x0004
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.A, SinglePhaseKind.N) == 0x0008
    assert TracedPhasesBitManipulation().set(0xFFFF, SinglePhaseKind.A, SinglePhaseKind.NONE) == 0xFFF0

    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.B, SinglePhaseKind.A) == 0x0010
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.B, SinglePhaseKind.B) == 0x0020
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.B, SinglePhaseKind.C) == 0x0040
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.B, SinglePhaseKind.N) == 0x0080
    assert TracedPhasesBitManipulation().set(0xFFFF, SinglePhaseKind.B, SinglePhaseKind.NONE) == 0xFF0F

    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.C, SinglePhaseKind.A) == 0x0100
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.C, SinglePhaseKind.B) == 0x0200
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.C, SinglePhaseKind.C) == 0x0400
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.C, SinglePhaseKind.N) == 0x0800
    assert TracedPhasesBitManipulation().set(0xFFFF, SinglePhaseKind.C, SinglePhaseKind.NONE) == 0xF0FF

    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.N, SinglePhaseKind.A) == 0x1000
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.N, SinglePhaseKind.B) == 0x2000
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.N, SinglePhaseKind.C) == 0x4000
    assert TracedPhasesBitManipulation().set(0x0000, SinglePhaseKind.N, SinglePhaseKind.N) == 0x8000
    assert TracedPhasesBitManipulation().set(0xFFFF, SinglePhaseKind.N, SinglePhaseKind.NONE) == 0x0FFF
