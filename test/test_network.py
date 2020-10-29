#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.protobuf.cim.iec61970 import EnergySource as PBEnergySource, BaseVoltage as PBBaseVoltage, Voltage as PBVoltage, \
    EnergyConsumer as PBEnergyConsumer, AcLineSegment as PBACLineSegment, PowerTransformer as PBPowerTransformer, \
    Breaker as PBBreaker, PerLengthSequenceImpedance as PBPLSI, Terminal as PBTerminal
from zepben.protobuf.cim.iec61968 import CableInfo as PBCableInfo, OverheadWireInfo as PBOverheadWireInfo, Customer as PBCustomer, \
    UsagePoint as PBUsagePoint, Meter as PBMeter, AssetInfo as PBAssetInfo, MeterReading as PBMeterReading
from zepben.cimbend import EnergySource, BaseVoltage, EnergyConsumer, AcLineSegment, PowerTransformer, Breaker, \
    PerLengthSequenceImpedance, Terminal, VoltageReading
from zepben.cimbend import CableInfo, OverheadWireInfo, Customer, UsagePoint, Meter, MeterReading
from zepben.cimbend import NetworkService, MetricsStore, ReadingType

"""
TODO:
    - Test __getitem__ for all types
"""


class TestEquipmentContainer(object):
    def test_add_pb(self):
        """Test addition to the network works for all PB types."""
        ms = MetricsStore()
        network = NetworkService(ms)
        bv1 = PBBaseVoltage(mRID="bv1", nominalVoltage=PBVoltage(value=22000))
        network.add(bv1)
        bv2 = PBBaseVoltage(mRID="bv2", nominalVoltage=PBVoltage(value=415))
        network.add(bv2)
        t = PBTerminal(mRID="t1", connectivityNodeMRID="c1")
        es = PBEnergySource(mRID="1", baseVoltageMRID="bv1", terminals=[t])
        network.add(es)
        ec = PBEnergyConsumer(mRID="2", baseVoltageMRID="bv2")
        network.add(ec)
        plsi = PBPLSI(mRID="plsi1")
        network.add(plsi)
        ci = PBCableInfo(mRID="7")
        ai1 = PBAssetInfo(cableInfo=ci)
        network.add(ai1)
        acls = PBACLineSegment(mRID="3", baseVoltageMRID="bv1", perLengthSequenceImpedanceMRID="plsi1", assetInfoMRID="7")
        network.add(acls)
        pt = PBPowerTransformer(mRID="4", baseVoltageMRID="bv2")
        network.add(pt)
        br = PBBreaker(mRID="5", baseVoltageMRID="bv2")
        network.add(br)
        cust = PBCustomer(mRID="6")
        network.add(cust)
        owi = PBOverheadWireInfo(mRID="8")
        ai2 = PBAssetInfo(overheadWireInfo=owi)
        network.add(ai2)
        up = PBUsagePoint(mRID="up1")
        network.add(up)
        m = PBMeter(mRID="10", usagePointMRIDs=["up1"])
        network.add(m)
        # Ensure types made it to correct maps
        assert network.energy_sources["1"].mrid == es.mRID
        assert network.base_voltages["bv1"].mrid == bv1.mRID
        assert network.base_voltages["bv2"].mrid == bv2.mRID
        assert network.energy_consumers["2"].mrid == ec.mRID
        assert network.lines["3"].mrid == acls.mRID
        assert network.transformers["4"].mrid == pt.mRID
        assert network.breakers["5"].mrid == br.mRID
        assert network.seq_impedances["plsi1"].mrid == plsi.mRID
        assert network.meters["10"].mrid == m.mRID
        assert network.usage_points["up1"].mrid == up.mRID
        assert network.asset_infos["7"].mrid == ci.mRID
        assert network.asset_infos["8"].mrid == owi.mRID
        assert network.customers["6"].mrid == cust.mRID
        assert network.connectivity_nodes["c1"].mrid == "c1"
        # ensure no extras in any map
        assert len(network.energy_sources) == 1
        assert len(network.asset_infos) == 2
        assert len(network.energy_consumers) == 1
        assert len(network.base_voltages) == 2
        assert len(network.lines) == 1
        assert len(network.transformers) == 1
        assert len(network.seq_impedances) == 1
        assert len(network.breakers) == 1
        assert len(network.customers) == 1
        assert len(network.meters) == 1
        assert len(network.usage_points) == 1
        assert len(network.connectivity_nodes) == 1

    def test_add(self):
        """Test addition to the network works for all CIM types."""
        ms = MetricsStore()
        network = NetworkService(ms)
        bv1 = BaseVoltage(mrid="bv1", nom_volt=22000)
        network.add(bv1)
        bv2 = BaseVoltage(mrid="bv2", nom_volt=415)
        network.add(bv2)
        c1 = network.add_connectivitynode("c1")
        t = Terminal(mrid="t1", connectivity_node=c1)
        es = EnergySource(mrid="1", base_voltage=bv1, terminals=[t])
        network.add(es)
        ec = EnergyConsumer(mrid="2", base_voltage=bv2)
        network.add(ec)
        plsi = PerLengthSequenceImpedance(mrid="plsi1")
        network.add(plsi)
        ci = CableInfo(mrid="7")
        network.add(ci)
        acls = AcLineSegment(mrid="3", base_voltage=bv1, plsi=plsi, wire_info=ci)
        network.add(acls)
        pt = PowerTransformer(mrid="4")
        network.add(pt)
        br = Breaker(mrid="5", base_voltage=bv2)
        network.add(br)
        cust = Customer(mrid="6")
        network.add(cust)
        owi = OverheadWireInfo(mrid="8")
        network.add(owi)
        up = UsagePoint(mrid="up1")
        network.add(up)
        m = Meter(mrid="10", usage_points=[up])
        network.add(m)
        # Ensure types made it to correct maps
        assert network.energy_sources["1"].mrid == es.mrid
        assert network.base_voltages["bv1"].mrid == bv1.mrid
        assert network.base_voltages["bv2"].mrid == bv2.mrid
        assert network.energy_consumers["2"].mrid == ec.mrid
        assert network.lines["3"].mrid == acls.mrid
        assert network.transformers["4"].mrid == pt.mrid
        assert network.breakers["5"].mrid == br.mrid
        assert network.seq_impedances["plsi1"].mrid == plsi.mrid
        assert network.meters["10"].mrid == m.mrid
        assert network.usage_points["up1"].mrid == up.mrid
        assert network.asset_infos["7"].mrid == ci.mrid
        assert network.asset_infos["8"].mrid == owi.mrid
        assert network.customers["6"].mrid == cust.mrid
        assert network.connectivity_nodes["c1"].mrid == "c1"
        # ensure no extras in any map
        assert len(network.energy_sources) == 1
        assert len(network.asset_infos) == 2
        assert len(network.energy_consumers) == 1
        assert len(network.base_voltages) == 2
        assert len(network.lines) == 1
        assert len(network.transformers) == 1
        assert len(network.seq_impedances) == 1
        assert len(network.breakers) == 1
        assert len(network.customers) == 1
        assert len(network.meters) == 1
        assert len(network.usage_points) == 1
        assert len(network.connectivity_nodes) == 1
