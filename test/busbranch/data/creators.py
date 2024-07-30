#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve import PerLengthSequenceImpedance, PowerTransformer, PowerTransformerEnd


def _create_per_length_sequence_impedance(i: float) -> PerLengthSequenceImpedance:
    return PerLengthSequenceImpedance(mrid=f"plsi{i}", r=i, x=i, bch=i, gch=i, r0=i, x0=i, b0ch=i, g0ch=i)


def _create_transformer_ends(tx: PowerTransformer, voltages: List[int] = None) -> List[PowerTransformerEnd]:
    if voltages is None:
        voltages = [11000, 415]

    ends = []
    for i in range(0, len(voltages)):
        end = PowerTransformerEnd(mrid=f"{tx.mrid}_e{i + 1}", power_transformer=tx, rated_u=voltages[i])
        terminal = tx.get_terminal_by_sn(i + 1)

        if terminal is None:
            raise ValueError(f"No terminal found to attach transformer end {end.mrid} in power transformer {tx.mrid}")

        tx.add_end(end)
        end.terminal = terminal
        ends.append(end)

    return ends
