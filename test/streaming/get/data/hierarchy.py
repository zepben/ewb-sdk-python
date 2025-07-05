#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import NetworkService, Loop, Circuit, Substation
from zepben.evolve.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.geographical_region import GeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.feeder import Feeder


def create_hierarchy_network() -> NetworkService:
    ns = NetworkService()

    ns.add(GeographicalRegion(mrid="g1"))
    ns.add(GeographicalRegion(mrid="g2"))

    ns.add(SubGeographicalRegion(mrid="sg1"))
    ns.add(SubGeographicalRegion(mrid="sg2"))

    ns.add(Substation(mrid="s1"))
    ns.add(Substation(mrid="s2"))

    ns.add(Feeder(mrid="f1"))
    ns.add(Feeder(mrid="f2"))

    ns.add(Circuit(mrid="c1"))
    ns.add(Circuit(mrid="c2"))

    ns.add(Loop(mrid="l1"))
    ns.add(Loop(mrid="l2"))

    return ns
