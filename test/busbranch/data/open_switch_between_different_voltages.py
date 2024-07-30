#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from busbranch.data.creators import _create_per_length_sequence_impedance
from network_fixtures import create_terminals
from zepben.evolve import NetworkService, Breaker, AcLineSegment, BaseVoltage


def open_switch_between_different_voltages():
    """
    both acls have the same plsi

       415V     433V    433V
                  /
     +-------+---*  --+-------+
       acls1    open    acls2
               switch
    """
    network = NetworkService()

    plsi = _create_per_length_sequence_impedance(1.0)
    network.add(plsi)

    bv415 = BaseVoltage(mrid="bv_415", nominal_voltage=415)
    bv433 = BaseVoltage(mrid="bv_433", nominal_voltage=433)

    open_switch = Breaker(mrid="open_switch", base_voltage=bv433)
    open_switch.set_normally_open(True)
    open_switch.set_open(True)
    network.add(open_switch)
    open_switch_ts = create_terminals(network, open_switch, 2)

    acls1 = AcLineSegment(mrid="acls_415", length=1.0, base_voltage=bv415, per_length_sequence_impedance=plsi)
    network.add(acls1)
    acls1_ts = create_terminals(network, acls1, 2)

    acls2 = AcLineSegment(mrid="acls_433", length=1.0, base_voltage=bv433, per_length_sequence_impedance=plsi)
    network.add(acls2)
    acls2_ts = create_terminals(network, acls2, 2)

    network.connect_terminals(acls1_ts[1], open_switch_ts[0])
    network.connect_terminals(open_switch_ts[1], acls2_ts[0])

    return network
