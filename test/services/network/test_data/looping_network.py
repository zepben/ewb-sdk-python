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
    # j0   ac0   j1   ac1   j2   ac2   j3
    # *11------21*21------21*21------21*
    #            3                     2
    #            1                     1
    #        ac3 |                     | ac4
    #            2                     2
    #            1  ac5                1
    #         j4 *21------21* j5       * j6 (open)
    #            3                     2
    #            1                     1
    #        ac6 |                     | ac7
    #            2                     2
    #            1    ac8   j8   ac9   2
    #         j7 *21------21*21------21* j9
    #            3
    #            1    ac11
    #            |      /--21* j11
    #       ac10 |     /     2
    #            |    /      1
    #            2   /       | ac13
    #            1  /        2
    #        j10 *21 ac12    2   ac14
    #            31--------21*31------21* j13
    #             1        2 j12
    #              \       |
    #               \      1 ac16
    #                \     2
    #                 \--21* j14
    #               ac15
    #
    return (
        TestNetworkBuilder()
        .from_junction(nominal_phases=PhaseCode.ABCN, num_terminals=1, mrid='j0')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac0')
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3, mrid='j1')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac3')
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3, mrid='j4')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac6')
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3, mrid='j7')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac10')
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3, mrid='j10')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac12')
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3, mrid='j12')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac14')
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=1, mrid='j13')
        .branch_from("j1", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac1')
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j2')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac2')
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j3')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac4')
        .to_breaker(nominal_phases=PhaseCode.ABCN, is_normally_open=True, is_open=True, mrid='j6')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac7')
        .branch_from("j4", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac5')
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=1, mrid='j5')
        .branch_from("j7", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac8')
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j8')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac9')
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j9')
        .connect("ac7", "j9", 2, 2)
        .branch_from("j10", 3)
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac15')
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j14')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac16')
        .connect("ac16", "j12", 2, 1)
        .branch_from("j10", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac11')
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j11')
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac13')
        .connect("ac13", "j12", 2, 2)
        .network
    )
