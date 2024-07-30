#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import TestNetworkBuilder, PhaseCode


def create_looping_network():
    """
    Network with loops in it. This was originally written in the JVM SDK without the use of TestNetworkBuilder.
    Line lengths and impedances have been omitted in the absence of any tests where they matter.
    :return: An example network with loops.
    """
    #
    # j0   c1    j2   c13   j14  c15   j16
    # *11------21*21------21*21------21*
    #            3                     2
    #            1                     1
    #         c3 |                     | c17
    #            2                     2
    #            1    c20              1
    #         j4 *21------21* j21      * b18 (open)
    #            3                     2
    #            1                     1
    #         c5 |                     | c19
    #            2                     2
    #            1    c22  j23   c24   2
    #         j6 *21------21*21------21* j25
    #            3
    #            1     c29
    #            |      /--21* j30
    #         c7 |     /     2
    #            |    /      1
    #            2   /       | c31
    #            1  /        2
    #         j8 *21   c9    2    c11
    #            31--------21*31------21* j12
    #             1        2 j10
    #              \       |
    #               \      1 c28
    #                \     2
    #                 \--21* j27
    #                c26
    #
    return (
        TestNetworkBuilder()
        .from_junction(nominal_phases=PhaseCode.ABCN, num_terminals=1)  # j0
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c1
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3)  # j2
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c3
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3)  # j4
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c5
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3)  # j6
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c7
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3)  # j8
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c9
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3)  # j10
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c11
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=1)  # j12
        .branch_from("j2", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c13
        .to_junction(nominal_phases=PhaseCode.ABCN)  # j14
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c15
        .to_junction(nominal_phases=PhaseCode.ABCN)  # j16
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c17
        .to_breaker(nominal_phases=PhaseCode.ABCN, is_normally_open=True)  # b18
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c19
        .branch_from("j4", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c20
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=1)  # j21
        .branch_from("j6", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c22
        .to_junction(nominal_phases=PhaseCode.ABCN)  # j23
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c24
        .to_junction(nominal_phases=PhaseCode.ABCN)  # j25
        .connect("c19", "j25", 2, 2)
        .branch_from("j8", 3)
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c26
        .to_junction(nominal_phases=PhaseCode.ABCN)  # j27
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c28
        .connect("c28", "j10", 2, 1)
        .branch_from("j8", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c29
        .to_junction(nominal_phases=PhaseCode.ABCN)  # j30
        .to_acls(nominal_phases=PhaseCode.ABCN)  # c31
        .connect("c31", "j10", 2, 2)
        .network
    )
