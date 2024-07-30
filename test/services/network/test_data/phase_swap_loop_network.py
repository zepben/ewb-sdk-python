#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from network_fixtures import create_source_for_connecting, create_junction_for_connecting, create_switch_for_connecting, create_acls_for_connecting
from zepben.evolve import NetworkService, PhaseCode, Feeder


def create_phase_swap_loop_network() -> NetworkService:
    """
    Creates a network with phase twisting for testing

    :return: the NetworkService populated with the twisted phase network
    """
    #
    #  n0 ac0        ac1     n1   ac2        ac3   n2
    #  *==ABCN==+====ABCN====*====ABCN====+==ABCN==*
    #           |                         |
    #       ac4 AB                        BC ac9
    #           |                         |
    #        n3 *                         * n7
    #           |                         |
    #       ac5 XY                        XY ac8
    #           |            n5           |
    #        n4 *-----XY-----*-----XY-----* n6 (open)
    #           |     ac6    |     ac7
    #      ac10 X            Y ac11
    #           |            |
    #        n8 *            * n9
    #
    network = NetworkService()
    node0 = create_source_for_connecting(network, "node0", 1, PhaseCode.ABCN)
    node1 = create_junction_for_connecting(network, "node1", 2, PhaseCode.ABCN)
    node2 = create_junction_for_connecting(network, "node2", 1, PhaseCode.ABCN)
    node3 = create_junction_for_connecting(network, "node3", 2, PhaseCode.AB)
    node4 = create_junction_for_connecting(network, "node4", 3, PhaseCode.XY)
    node5 = create_junction_for_connecting(network, "node5", 3, PhaseCode.XY)
    node6 = create_switch_for_connecting(network, "node6", 2, PhaseCode.XY, [True, True], [True, True])
    node7 = create_junction_for_connecting(network, "node7", 2, PhaseCode.BC)
    node8 = create_junction_for_connecting(network, "node8", 1, PhaseCode.X)
    node9 = create_junction_for_connecting(network, "node9", 1, PhaseCode.Y)

    ac_line_segment0 = create_acls_for_connecting(network, "ac_line_segment0", PhaseCode.ABCN)
    ac_line_segment1 = create_acls_for_connecting(network, "ac_line_segment1", PhaseCode.ABCN)
    ac_line_segment2 = create_acls_for_connecting(network, "ac_line_segment2", PhaseCode.ABCN)
    ac_line_segment3 = create_acls_for_connecting(network, "ac_line_segment3", PhaseCode.ABCN)
    ac_line_segment4 = create_acls_for_connecting(network, "ac_line_segment4", PhaseCode.AB)
    ac_line_segment5 = create_acls_for_connecting(network, "ac_line_segment5", PhaseCode.XY)
    ac_line_segment6 = create_acls_for_connecting(network, "ac_line_segment6", PhaseCode.XY)
    ac_line_segment7 = create_acls_for_connecting(network, "ac_line_segment7", PhaseCode.XY)
    ac_line_segment8 = create_acls_for_connecting(network, "ac_line_segment8", PhaseCode.XY)
    ac_line_segment9 = create_acls_for_connecting(network, "ac_line_segment9", PhaseCode.BC)
    ac_line_segment10 = create_acls_for_connecting(network, "ac_line_segment10", PhaseCode.X)
    ac_line_segment11 = create_acls_for_connecting(network, "ac_line_segment11", PhaseCode.Y)

    feeder = Feeder(mrid="fdr", normal_head_terminal=node0.get_terminal_by_sn(1))
    network.add(feeder)

    # Connect up a network so we can check connectivity.
    network.connect_by_mrid(node0.get_terminal_by_sn(1), "cn_0")
    network.connect_by_mrid(ac_line_segment0.get_terminal_by_sn(1), "cn_0")
    network.connect_by_mrid(ac_line_segment0.get_terminal_by_sn(2), "cn_1")
    network.connect_by_mrid(ac_line_segment1.get_terminal_by_sn(1), "cn_1")
    network.connect_by_mrid(ac_line_segment1.get_terminal_by_sn(2), "cn_2")
    network.connect_by_mrid(node1.get_terminal_by_sn(1), "cn_2")
    network.connect_by_mrid(node1.get_terminal_by_sn(2), "cn_3")
    network.connect_by_mrid(ac_line_segment2.get_terminal_by_sn(1), "cn_3")
    network.connect_by_mrid(ac_line_segment2.get_terminal_by_sn(2), "cn_4")
    network.connect_by_mrid(ac_line_segment3.get_terminal_by_sn(1), "cn_4")
    network.connect_by_mrid(ac_line_segment3.get_terminal_by_sn(2), "cn_5")
    network.connect_by_mrid(node2.get_terminal_by_sn(1), "cn_5")
    network.connect_by_mrid(ac_line_segment4.get_terminal_by_sn(1), "cn_1")
    network.connect_by_mrid(ac_line_segment4.get_terminal_by_sn(2), "cn_6")
    network.connect_by_mrid(node3.get_terminal_by_sn(1), "cn_6")
    network.connect_by_mrid(node3.get_terminal_by_sn(2), "cn_7")
    network.connect_by_mrid(ac_line_segment5.get_terminal_by_sn(1), "cn_7")
    network.connect_by_mrid(ac_line_segment5.get_terminal_by_sn(2), "cn_8")
    network.connect_by_mrid(node4.get_terminal_by_sn(1), "cn_8")
    network.connect_by_mrid(node4.get_terminal_by_sn(2), "cn_9")
    network.connect_by_mrid(node4.get_terminal_by_sn(3), "cn_16")
    network.connect_by_mrid(ac_line_segment6.get_terminal_by_sn(1), "cn_9")
    network.connect_by_mrid(ac_line_segment6.get_terminal_by_sn(2), "cn_10")
    network.connect_by_mrid(node5.get_terminal_by_sn(1), "cn_10")
    network.connect_by_mrid(node5.get_terminal_by_sn(2), "cn_11")
    network.connect_by_mrid(node5.get_terminal_by_sn(3), "cn_18")
    network.connect_by_mrid(ac_line_segment7.get_terminal_by_sn(1), "cn_11")
    network.connect_by_mrid(ac_line_segment7.get_terminal_by_sn(2), "cn_12")
    network.connect_by_mrid(node6.get_terminal_by_sn(1), "cn_12")
    network.connect_by_mrid(node6.get_terminal_by_sn(2), "cn_13")
    network.connect_by_mrid(ac_line_segment8.get_terminal_by_sn(1), "cn_13")
    network.connect_by_mrid(ac_line_segment8.get_terminal_by_sn(2), "cn_14")
    network.connect_by_mrid(node7.get_terminal_by_sn(1), "cn_14")
    network.connect_by_mrid(node7.get_terminal_by_sn(2), "cn_15")
    network.connect_by_mrid(ac_line_segment9.get_terminal_by_sn(1), "cn_15")
    network.connect_by_mrid(ac_line_segment9.get_terminal_by_sn(2), "cn_4")
    network.connect_by_mrid(ac_line_segment10.get_terminal_by_sn(1), "cn_16")
    network.connect_by_mrid(ac_line_segment10.get_terminal_by_sn(2), "cn_17")
    network.connect_by_mrid(node8.get_terminal_by_sn(1), "cn_17")
    network.connect_by_mrid(ac_line_segment11.get_terminal_by_sn(1), "cn_18")
    network.connect_by_mrid(ac_line_segment11.get_terminal_by_sn(2), "cn_19")
    network.connect_by_mrid(node9.get_terminal_by_sn(1), "cn_19")

    return network
