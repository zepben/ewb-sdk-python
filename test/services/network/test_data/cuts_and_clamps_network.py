#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve import NetworkService, TestNetworkBuilder, AcLineSegment, Clamp, Terminal, ConductingEquipment, Cut


class CutsAndClampsNetwork:
    @staticmethod
    def multi_cut_and_clamp_network() -> TestNetworkBuilder:
        #
        #          2                     2
        #          c3          2         c7          2
        #          1           c5        1           c9
        #          1 clamp1    1         1 clamp3    1
        #          |           |         |           |
        # 1 b0 21--*--*1 cut1 2*--*--c1--*--*1 cut2 2*--*--21 b2 2
        #             |           |         |           |
        #             1           1 clamp2  1           1 clamp4
        #             c4          1         c8          1
        #             2           c6        2           c10
        #                         2                     2
        #
        builder = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls()  # c1
                   .to_breaker()  # b2
                   .from_acls()  # c3
                   .from_acls()  # c4
                   .from_acls()  # c5
                   .from_acls()  # c6
                   .from_acls()  # c7
                   .from_acls()  # c8
                   .from_acls()  # c9
                   .from_acls()  # c10
                   )

        network = builder.network

        segment: AcLineSegment = network['c1']

        clamp1 = _segment_with_clamp(network, segment, 1.0)
        cut1 = _segment_with_cut(network, segment, 2.0)
        clamp2 = _segment_with_clamp(network, segment, 3.0)
        clamp3 = _segment_with_clamp(network, segment, 4.0)
        cut2 = _segment_with_cut(network, segment, 5.0)
        clamp4 = _segment_with_clamp(network, segment, 6.0)

        network.connect(clamp1[1], network.get('c3', ConductingEquipment)[1])
        network.connect(cut1[1], network.get('c4', ConductingEquipment)[1])
        network.connect(cut1[2], network.get('c5', ConductingEquipment)[1])
        network.connect(clamp2[1], network.get('c6', ConductingEquipment)[1])
        network.connect(clamp3[1], network.get('c7', ConductingEquipment)[1])
        network.connect(cut2[1], network.get('c8', ConductingEquipment)[1])
        network.connect(cut2[2], network.get('c9', ConductingEquipment)[1])
        network.connect(clamp4[1], network.get('c10', ConductingEquipment)[1])

        return builder


def _segment_with_clamp(network: NetworkService, segment: AcLineSegment, length_from_terminal1: Optional[float]) -> Clamp:
    clamp = Clamp(mrid=f'clamp{segment.num_clamps() + 1}')
    clamp.add_terminal(Terminal(mrid=f'{clamp.mrid}-t1'))
    clamp.length_from_terminal_1 = length_from_terminal1

    segment.add_clamp(clamp)
    network.add(clamp)
    return clamp


def _segment_with_cut(network: NetworkService, segment: AcLineSegment, length_from_terminal1: Optional[float]) -> Cut:
    cut = Cut(mrid=f'cut{segment.num_cuts() + 1}', length_from_terminal_1=length_from_terminal1)
    cut.add_terminal(Terminal(mrid=f'{cut.mrid}-t1'))
    cut.add_terminal(Terminal(mrid=f'{cut.mrid}-t2'))

    segment.add_cut(cut)
    network.add(cut)
    return cut
