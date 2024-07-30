#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import NetworkService, Substation, Loop, Circuit, EquipmentContainer, Junction, Terminal, Feeder


#
#              cir4
#           /------- sub4
#   -- sub1 --
#   |        |
#   | cir1   | cir2
#   |   cir3 |
#  sub2 --- sub3
#
# Each circuit contains an object
# Each substation contains an object plus a feeder with an additional object
#
def create_loops_network() -> NetworkService:
    ns = NetworkService()

    sub1 = Substation(mrid="sub1")
    sub2 = Substation(mrid="sub2")
    sub3 = Substation(mrid="sub3")
    sub4 = Substation(mrid="sub4")

    fdr1 = Feeder(mrid="fdr1")
    fdr2 = Feeder(mrid="fdr2")
    fdr3 = Feeder(mrid="fdr3")
    fdr4 = Feeder(mrid="fdr4")

    cir1 = Circuit(mrid="cir1")
    cir2 = Circuit(mrid="cir2")
    cir3 = Circuit(mrid="cir3")
    cir4 = Circuit(mrid="cir4")

    loop1 = Loop(mrid="loop1")
    loop2 = Loop(mrid="loop2")

    sub1.add_feeder(fdr1)
    sub2.add_feeder(fdr2)
    sub3.add_feeder(fdr3)
    sub4.add_feeder(fdr4)

    fdr1.normal_energizing_substation = sub1
    fdr2.normal_energizing_substation = sub2
    fdr3.normal_energizing_substation = sub3
    fdr4.normal_energizing_substation = sub4

    cir1.add_end_substation(sub1)
    cir1.add_end_substation(sub2)
    cir2.add_end_substation(sub1)
    cir2.add_end_substation(sub3)
    cir3.add_end_substation(sub2)
    cir3.add_end_substation(sub3)
    cir4.add_end_substation(sub1)
    cir4.add_end_substation(sub4)

    sub1.add_circuit(cir1)
    sub1.add_circuit(cir2)
    sub1.add_circuit(cir4)
    sub2.add_circuit(cir1)
    sub2.add_circuit(cir3)
    sub3.add_circuit(cir2)
    sub3.add_circuit(cir3)
    sub4.add_circuit(cir4)

    loop1.add_circuit(cir1)
    loop1.add_circuit(cir2)
    loop1.add_circuit(cir3)
    loop1.add_energizing_substation(sub1)
    loop1.add_substation(sub2)
    loop1.add_substation(sub3)
    loop2.add_circuit(cir4)
    loop2.add_energizing_substation(sub1)
    loop2.add_substation(sub4)

    cir1.loop = loop1
    cir2.loop = loop1
    cir3.loop = loop1
    cir4.loop = loop2

    sub1.add_energized_loop(loop1)
    sub1.add_energized_loop(loop2)
    sub2.add_loop(loop1)
    sub3.add_loop(loop1)
    sub4.add_loop(loop2)

    _create_junction(ns, sub1)
    _create_junction(ns, sub2)
    _create_junction(ns, sub3)
    _create_junction(ns, sub4)
    _create_junction(ns, fdr1)
    _create_junction(ns, fdr2)
    _create_junction(ns, fdr3)
    _create_junction(ns, fdr4)
    _create_junction(ns, cir1)
    _create_junction(ns, cir2)
    _create_junction(ns, cir3)
    _create_junction(ns, cir4)

    ns.add(sub1)
    ns.add(sub2)
    ns.add(sub3)
    ns.add(sub4)
    ns.add(fdr1)
    ns.add(fdr2)
    ns.add(fdr3)
    ns.add(fdr4)
    ns.add(cir1)
    ns.add(cir2)
    ns.add(cir3)
    ns.add(cir4)
    ns.add(loop1)
    ns.add(loop2)

    return ns


def _create_junction(ns: NetworkService, container: EquipmentContainer):
    j = Junction(mrid=f"{container.mrid}-j")
    j.add_container(container)
    container.add_equipment(j)

    t = Terminal(mrid=f"{j.mrid}-t")
    t.conducting_equipment = j
    j.add_terminal(t)

    ns.add(j)
    ns.add(t)
