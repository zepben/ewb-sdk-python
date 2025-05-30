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
                   .with_clamp(length_from_terminal_1=1.0)  # c1-clamp1
                   .with_cut(length_from_terminal_1=2.0, is_normally_open=False)  # c1-cut1
                   .with_clamp(length_from_terminal_1=3.0)  # c1-clamp2
                   .with_clamp(length_from_terminal_1=4.0)  # c1-clamp3
                   .with_cut(length_from_terminal_1=5.0, is_normally_open=False)  # c1-cut2
                   .with_clamp(length_from_terminal_1=6.0)  # c1-clamp4
                   .to_breaker()  # b2
                   .from_acls()  # c3
                   .connect_to('c1-clamp1', from_terminal=1)
                   .from_acls()  # c4
                   .connect_to('c1-cut1', from_terminal=1)
                   .from_acls()  # c5
                   .connect_to('c1-cut1', to_terminal=2, from_terminal=1)
                   .from_acls()  # c6
                   .connect_to('c1-clamp2', from_terminal=1)
                   .from_acls()  # c7
                   .connect_to('c1-clamp3', from_terminal=1)
                   .from_acls()  # c8
                   .connect_to('c1-cut2', from_terminal=1)
                   .from_acls()  # c9
                   .connect_to('c1-cut2', to_terminal=2, from_terminal=1)
                   .from_acls()  # c10
                   .connect_to('c1-clamp4', from_terminal=1)
                   )

        return builder


