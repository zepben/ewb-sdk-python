from zepben.evolve import NetworkService, GeographicalRegion, Loop, Circuit, Feeder, Substation, SubGeographicalRegion


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
