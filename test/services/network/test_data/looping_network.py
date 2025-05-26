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
    #            Python Diagram                                   JVM SDK Diagram
    #
    # j0   c1    j2   c13   j14  c15   j16          // j0   ac0   j1   ac1   j2   ac2   j3
    # *11------21*21------21*21------21*            // *11------21*21------21*21------21*
    #            3                     2            //            3                     2
    #            1                     1            //            1                     1
    #         c3 |                     | c17        //        ac3 |                     | ac4
    #            2                     2            //            2                     2
    #            1    c20              1            //            1  ac5                1
    #         j4 *21------21* j21      * b18 (open) //         j4 *21------21* j5       * j6 (open)
    #            3                     2            //            3                     2
    #            1                     1            //            1                     1
    #         c5 |                     | c19        //        ac6 |                     | ac7
    #            2                     2            //            2                     2
    #            1    c22  j23   c24   2            //            1    ac8   j8   ac9   2
    #         j6 *21------21*21------21* j25        //         j7 *21------21*21------21* j9
    #            3                                  //            3
    #            1     c29                          //            1    ac11
    #            |      /--21* j30                  //            |      /--21* j11
    #         c7 |     /     2                      //       ac10 |     /     2
    #            |    /      1                      //            |    /      1
    #            2   /       | c31                  //            2   /       | ac13
    #            1  /        2                      //            1  /        2
    #         j8 *21   c9    2    c11               //        j10 *21 ac12    2   ac14
    #            31--------21*31------21* j12       //            31--------21*31------21* j13
    #             1        2 j10                    //             1        2 j12
    #              \       |                        //              \       |
    #               \      1 c28                    //               \      1 ac16
    #                \     2                        //                \     2
    #                 \--21* j27                    //                 \--21* j14
    #                c26                            //               ac15
    #
    return (
        TestNetworkBuilder()
        .from_junction(nominal_phases=PhaseCode.ABCN, num_terminals=1, mrid='j0')  # j0
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac0')  # c1
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3, mrid='j1')  # j2
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac3')  # c3
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3, mrid='j4')  # j4
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac6')  # c5
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3, mrid='j7')  # j6
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac10')  # c7
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3, mrid='j10')  # j8
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac12')  # c9
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=3, mrid='j12')  # j10
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac14')  # c11
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=1, mrid='j13')  # j12
        .branch_from("j1", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac1')  # c13
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j2')  # j14
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac2')  # c15
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j3')  # j16
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac4')  # c17
        .to_breaker(nominal_phases=PhaseCode.ABCN, is_normally_open=True, is_open=True, mrid='j6')  # b18
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac7')  # c19
        .branch_from("j4", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac5')  # c20
        .to_junction(nominal_phases=PhaseCode.ABCN, num_terminals=1, mrid='j5')  # j21
        .branch_from("j7", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac8')  # c22
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j8')  # j23
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac9')  # c24
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j9')  # j25
        .connect("ac7", "j9", 2, 2)
        .branch_from("j10", 3)
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac15')  # c26
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j14')  # j27
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac16')  # c28
        .connect("ac16", "j12", 2, 1)
        .branch_from("j10", 2)
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac11')  # c29
        .to_junction(nominal_phases=PhaseCode.ABCN, mrid='j11')  # j30
        .to_acls(nominal_phases=PhaseCode.ABCN, mrid='ac13')  # c31
        .connect("ac13", "j12", 2, 2)
        .network
    )
