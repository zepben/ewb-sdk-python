#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve import PerLengthSequenceImpedance, TestNetworkBuilder, AcLineSegment, Terminal, PhaseCode, WireInfo, CableInfo, Feeder
from zepben.evolve.processors.simplification.common_impedance_combiner import CommonImpedanceCombiner
from zepben.evolve.processors.simplification.reshape import Reshape


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_combine_common_impedance_lines():
    plsi = PerLengthSequenceImpedance()
    plsi.r = 0.001

    test_network = (await TestNetworkBuilder()
                    .from_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .to_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .build())
    test_network.add(plsi)

    what_it_did = await CommonImpedanceCombiner().process(test_network)

    combinedLine = list(test_network.objects(AcLineSegment))[0]
    combinedLineT1 = combinedLine.get_terminal_by_sn(1)
    combinedLineT2 = combinedLine.get_terminal_by_sn(2)

    assert len(list(test_network.objects(AcLineSegment))) == 1
    assert len(list(test_network.objects(Terminal))) == 2
    assert combinedLine.num_terminals() == 2
    assert combinedLine.per_length_sequence_impedance == plsi

    assert set(what_it_did.originalToNew.keys()) == {"c0-t1", "c0", "c0-t2", "generated_cn_0", "c1-t1", "c1", "c1-t2"}
    assert what_it_did.originalToNew["c0-t1"] == {combinedLineT1}
    assert what_it_did.originalToNew["c1-t2"] == {combinedLineT2}
    assert what_it_did.originalToNew["c0-t1"] != what_it_did.originalToNew["c1-t2"]
    for thing in {"c0", "c0-t2", "generated_cn_0", "c1-t1", "c1"}:
        assert what_it_did.originalToNew[thing] == {combinedLine}
    assert what_it_did.newToOriginal[combinedLineT1.mrid] == {"c0-t1"}
    assert what_it_did.newToOriginal[combinedLineT2.mrid] == {"c1-t2"}
    assert what_it_did.newToOriginal[combinedLine.mrid] == {"c0", "c0-t2", "generated_cn_0", "c1-t1", "c1"}


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_keeps_branches():
    plsi = PerLengthSequenceImpedance()
    plsi.r = 0.001

    test_network = (await TestNetworkBuilder()
                    .from_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .to_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .to_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .branch_from("c0")
                    .to_power_transformer()
                    .branch_from("c1")
                    .to_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .build())
    test_network.add(plsi)

    what_it_did = await CommonImpedanceCombiner().process(test_network)
    assert {acls.mrid for acls in test_network.objects(AcLineSegment)} == {"c0", "c1", "c2", "c4"}  # using sets here isn't as smart as you think it is
    assert what_it_did.newToOriginal == {}
    assert what_it_did.originalToNew == {}


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_keeps_impedance_changes():
    plsi = PerLengthSequenceImpedance()
    plsi.r = 0.001
    plsi2 = PerLengthSequenceImpedance()
    plsi2.r = 0.002

    test_network = (await TestNetworkBuilder()
                    .from_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .to_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi2))
                    .build())
    test_network.add(plsi)
    test_network.add(plsi2)

    what_it_did = await CommonImpedanceCombiner().process(test_network)
    assert {acls.mrid for acls in test_network.objects(AcLineSegment)} == {"c0", "c1"}  # using sets here isn't as smart as you think it is
    assert what_it_did.newToOriginal == {}
    assert what_it_did.originalToNew == {}


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_keeps_impedance_changes():
    plsi = PerLengthSequenceImpedance()
    plsi.r = 0.001

    test_network = (await TestNetworkBuilder()
                    .from_acls(nominal_phases=PhaseCode.AB, action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .to_acls(nominal_phases=PhaseCode.BC, action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .build())
    test_network.add(plsi)

    what_it_did = await CommonImpedanceCombiner().process(test_network)
    assert {acls.mrid for acls in test_network.objects(AcLineSegment)} == {"c0", "c1"}  # using sets here isn't as smart as you think it is
    assert what_it_did.newToOriginal == {}
    assert what_it_did.originalToNew == {}


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_keeps_wire_info_changes():
    plsi = PerLengthSequenceImpedance()
    plsi.r = 0.001

    wi1 = CableInfo()
    wi1.rated_current = 15
    wi2 = CableInfo()
    wi2.rated_current = 20

    test_network = (await TestNetworkBuilder()
                    .from_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .to_acls(action=lambda c: _acls_setup(c, plsi, wireInfo=wi1))
                    .to_acls(action=lambda c: _acls_setup(c, plsi, wireInfo=wi2))
                    .build())
    test_network.add(plsi)
    test_network.add(wi1)
    test_network.add(wi2)

    what_it_did = await CommonImpedanceCombiner().process(test_network)
    assert {acls.mrid for acls in test_network.objects(AcLineSegment)} == {"c0", "c1", "c2"}  # using sets here isn't as smart as you think it is
    assert what_it_did.newToOriginal == {}
    assert what_it_did.originalToNew == {}


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_keeps_service_status_changes():
    plsi = PerLengthSequenceImpedance()
    plsi.r = 0.001

    def create_out_of_service(acls: AcLineSegment):
        acls.in_service = False
        setattr(acls, "per_length_sequence_impedance", plsi)

    test_network = (await TestNetworkBuilder()
                    .from_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .to_acls(action=create_out_of_service)
                    .build())
    test_network.add(plsi)

    what_it_did = await CommonImpedanceCombiner(lambda c: c.in_service).process(test_network)
    assert {acls.mrid for acls in test_network.objects(AcLineSegment)} == {"c0", "c1"}  # using sets here isn't as smart as you think it is
    assert what_it_did.newToOriginal == {}
    assert what_it_did.originalToNew == {}


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_keeps_important_nodes():
    plsi = PerLengthSequenceImpedance()
    plsi.r = 0.001

    detachedFeeder = Feeder()
    detachedFeeder.normal_head_terminal = Terminal(mrid="removed-terminal")

    test_network = (await TestNetworkBuilder()
                    .from_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .to_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .to_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .add_feeder("c0")
                    .build())
    test_network.add(plsi)
    test_network.add(detachedFeeder)

    what_it_did = await CommonImpedanceCombiner().process(test_network, Reshape({"removed-terminal": {test_network.get("generated_cn_1")}}, dict()))
    assert {acls.mrid for acls in test_network.objects(AcLineSegment)} == {"c0", "c1", "c2"}  # using sets here isn't as smart as you think it is
    assert what_it_did.newToOriginal == {}
    assert what_it_did.originalToNew == {}


def _acls_setup(acls: AcLineSegment, plsi: PerLengthSequenceImpedance = None, length: float = None, wireInfo: WireInfo = None):
    if plsi is not None:
        acls.per_length_sequence_impedance = plsi
    if length is not None:
        acls.length = length
    if wireInfo is not None:
        acls.asset_info = wireInfo
