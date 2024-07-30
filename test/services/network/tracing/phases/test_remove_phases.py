#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from services.network.tracing.phases.util import connected_equipment_trace_with_logging, validate_phases_from_term_or_equip, get_t
from zepben.evolve import TestNetworkBuilder, PhaseCode, EnergySource, RemovePhases, remove_all_traced_phases, SinglePhaseKind as SPK


@pytest.fixture()
async def simple_network():
    """
    s0 --c1-- --c2--
             \\-c3--

    s4 --c5--
    """
    network_service = await (
        TestNetworkBuilder()
        .from_source(PhaseCode.ABCN)  # s0
        .to_acls(PhaseCode.ABCN)  # c1
        .to_acls(PhaseCode.ABCN)  # c2
        .branch_from("c1")
        .to_acls(PhaseCode.AB)  # c3
        .from_source(PhaseCode.ABCN)  # s4
        .to_acls(PhaseCode.ABCN)  # c5
        .build()
    )
    await connected_equipment_trace_with_logging(network_service.objects(EnergySource))
    validate_phases_from_term_or_equip(network_service, "s0", PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "c1", PhaseCode.ABCN, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "c2", PhaseCode.ABCN, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "c3", PhaseCode.AB, PhaseCode.AB)
    validate_phases_from_term_or_equip(network_service, "s4", PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "c5", PhaseCode.ABCN, PhaseCode.ABCN)

    return network_service


@pytest.mark.asyncio
async def test_removes_all_core_by_default(simple_network):
    await RemovePhases().run(get_t(simple_network, "c1", 2))

    validate_phases_from_term_or_equip(simple_network, "s0", PhaseCode.ABCN)
    validate_phases_from_term_or_equip(simple_network, "c1", PhaseCode.ABCN, PhaseCode.NONE)
    validate_phases_from_term_or_equip(simple_network, "c2", PhaseCode.NONE, PhaseCode.NONE)
    validate_phases_from_term_or_equip(simple_network, "c3", PhaseCode.NONE, PhaseCode.NONE)
    validate_phases_from_term_or_equip(simple_network, "s4", PhaseCode.ABCN)
    validate_phases_from_term_or_equip(simple_network, "c5", PhaseCode.ABCN, PhaseCode.ABCN)


@pytest.mark.asyncio
async def test_can_remove_specific_phases(simple_network):
    await RemovePhases().run(get_t(simple_network, "s0", 1), PhaseCode.AB)

    validate_phases_from_term_or_equip(simple_network, "s0", [SPK.NONE, SPK.NONE, SPK.C, SPK.N])
    validate_phases_from_term_or_equip(simple_network, "c1", [SPK.NONE, SPK.NONE, SPK.C, SPK.N], [SPK.NONE, SPK.NONE, SPK.C, SPK.N])
    validate_phases_from_term_or_equip(simple_network, "c2", [SPK.NONE, SPK.NONE, SPK.C, SPK.N], [SPK.NONE, SPK.NONE, SPK.C, SPK.N])
    validate_phases_from_term_or_equip(simple_network, "c3", PhaseCode.NONE, PhaseCode.NONE)
    validate_phases_from_term_or_equip(simple_network, "s4", PhaseCode.ABCN)
    validate_phases_from_term_or_equip(simple_network, "c5", PhaseCode.ABCN, PhaseCode.ABCN)


@pytest.mark.asyncio
async def test_can_remove_from_entire_network(simple_network):
    remove_all_traced_phases(simple_network)

    validate_phases_from_term_or_equip(simple_network, "s0", PhaseCode.NONE)
    validate_phases_from_term_or_equip(simple_network, "c1", PhaseCode.NONE, PhaseCode.NONE)
    validate_phases_from_term_or_equip(simple_network, "c2", PhaseCode.NONE, PhaseCode.NONE)
    validate_phases_from_term_or_equip(simple_network, "c3", PhaseCode.NONE, PhaseCode.NONE)
    validate_phases_from_term_or_equip(simple_network, "s4", PhaseCode.NONE)
    validate_phases_from_term_or_equip(simple_network, "c5", PhaseCode.NONE, PhaseCode.NONE)
