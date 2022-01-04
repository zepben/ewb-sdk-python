#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode

from test.cim.enum_verifier import verify_enum
from zepben.evolve import PhaseCode, phase_code_by_id


def test_phase_code_enum():
    verify_enum(PhaseCode, PBPhaseCode)


def test_phase_code_value_lookup():
    for pc in PhaseCode:
        assert phase_code_by_id(pc.value[0]) == pc, f"value lookup of {pc.name} resulted in {phase_code_by_id(pc.value[0]).name}"
