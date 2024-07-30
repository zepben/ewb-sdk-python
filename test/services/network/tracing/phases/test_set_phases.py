#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from network_fixtures import phase_swap_loop_network  # noqa (Fixtures)
from services.network.tracing.phases.util import connected_equipment_trace_with_logging, validate_phases, validate_phases_from_term_or_equip, get_t
from zepben.evolve import SetPhases, EnergySource, ConductingEquipment, SinglePhaseKind as SPK, TestNetworkBuilder, PhaseCode, Breaker
from zepben.evolve.exceptions import TracingException, PhaseException


@pytest.mark.asyncio
@pytest.mark.parametrize('phase_swap_loop_network', [(False,)], indirect=True)
async def test_set_phases(phase_swap_loop_network):
    await SetPhases().run(phase_swap_loop_network)
    await connected_equipment_trace_with_logging(phase_swap_loop_network.objects(EnergySource))

    validate_phases(get_t(phase_swap_loop_network, "ac0", 1), [SPK.A, SPK.B, SPK.C, SPK.N])
    validate_phases(get_t(phase_swap_loop_network, "ac0", 2), [SPK.A, SPK.B, SPK.C, SPK.N])
    validate_phases(get_t(phase_swap_loop_network, "ac1", 1), [SPK.A, SPK.B, SPK.C, SPK.N])
    validate_phases(get_t(phase_swap_loop_network, "ac4", 1), [SPK.A, SPK.B])
    validate_phases(get_t(phase_swap_loop_network, "n4", 1), [SPK.A, SPK.B])
    validate_phases(get_t(phase_swap_loop_network, "n4", 2), [SPK.A, SPK.B])
    validate_phases(get_t(phase_swap_loop_network, "n4", 3), [SPK.A, SPK.B])
    validate_phases(get_t(phase_swap_loop_network, "n8", 1), [SPK.A])
    validate_phases(get_t(phase_swap_loop_network, "n5", 1), [SPK.A, SPK.B])
    validate_phases(get_t(phase_swap_loop_network, "n5", 2), [SPK.A, SPK.B])
    validate_phases(get_t(phase_swap_loop_network, "n5", 3), [SPK.A, SPK.B])
    validate_phases(get_t(phase_swap_loop_network, "n9", 1), [SPK.B])
    validate_phases(get_t(phase_swap_loop_network, "n6", 1), [SPK.A, SPK.B])
    validate_phases(get_t(phase_swap_loop_network, "n6", 2), [SPK.B, SPK.C])
    validate_phases(get_t(phase_swap_loop_network, "ac2", 2), [SPK.A, SPK.B, SPK.C, SPK.N])
    validate_phases(get_t(phase_swap_loop_network, "ac3", 1), [SPK.A, SPK.B, SPK.C, SPK.N])
    validate_phases(get_t(phase_swap_loop_network, "ac9", 2), [SPK.B, SPK.C])
    validate_phases(get_t(phase_swap_loop_network, "n2", 1), [SPK.A, SPK.B, SPK.C, SPK.N])


@pytest.mark.asyncio
async def test_applies_phases_from_sources():
    """
    s0 12--c1--21--c2--2
                1--c3--2

    1--c4--2
    """
    network_service = await (
        TestNetworkBuilder()
        .from_source(PhaseCode.ABCN)  # s0
        .to_acls(PhaseCode.ABCN)  # c1
        .to_acls(PhaseCode.ABCN)  # c2
        .branch_from("c1")
        .to_acls(PhaseCode.AB)  # c3
        .from_acls(PhaseCode.ABCN)  # c4
        .build()
    )
    await connected_equipment_trace_with_logging(network_service.objects(EnergySource))

    validate_phases_from_term_or_equip(network_service, "s0", PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "c1", PhaseCode.ABCN, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "c2", PhaseCode.ABCN, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "c3", PhaseCode.AB, PhaseCode.AB)
    validate_phases_from_term_or_equip(network_service, "c4", PhaseCode.NONE, PhaseCode.NONE)


@pytest.mark.asyncio
async def test_stops_at_open_points():
    """
    s0 11 b1 21--c2--2

    s3 11 b4 21--c5--2
    """
    network_service = await (
        TestNetworkBuilder()
        .from_source(PhaseCode.ABCN)  # s0
        .to_breaker(PhaseCode.ABCN, is_normally_open=True, is_open=False)  # b1
        .to_acls(PhaseCode.ABCN)  # c2
        .from_source(PhaseCode.ABCN)  # s3
        .to_breaker(PhaseCode.ABCN, is_open=True)  # b4
        .to_acls(PhaseCode.ABCN)  # c5
        .build()
    )
    await connected_equipment_trace_with_logging(network_service.objects(EnergySource))

    validate_phases_from_term_or_equip(network_service, "s0-t1", PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "b1-t1", PhaseCode.ABCN, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "b1-t2", PhaseCode.NONE, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "c2-t1", PhaseCode.NONE, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "c2-t2", PhaseCode.NONE, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "s3-t1", PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "b4-t1", PhaseCode.ABCN, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "b4-t2", PhaseCode.ABCN, PhaseCode.NONE)
    validate_phases_from_term_or_equip(network_service, "c5-t1", PhaseCode.ABCN, PhaseCode.NONE)
    validate_phases_from_term_or_equip(network_service, "c5-t2", PhaseCode.ABCN, PhaseCode.NONE)


@pytest.mark.asyncio
async def test_traces_unganged():
    """
    s0 11 b1 21--c2--1
    """

    def set_open_status(breaker: Breaker):
        breaker.set_open(True, SPK.A)
        breaker.set_normally_open(True, SPK.B)

    network_service = await (
        TestNetworkBuilder()
        .from_source(PhaseCode.ABCN)  # s0
        .to_breaker(PhaseCode.ABCN, action=set_open_status)  # b1
        .to_acls(PhaseCode.ABCN)
        .build()
    )
    await connected_equipment_trace_with_logging(network_service.objects(EnergySource))

    validate_phases_from_term_or_equip(network_service, "s0", PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "b1-t1", PhaseCode.ABCN, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "b1-t2", [SPK.A, SPK.NONE, SPK.C, SPK.N], [SPK.NONE, SPK.B, SPK.C, SPK.N])
    validate_phases_from_term_or_equip(network_service, "c2-t1", [SPK.A, SPK.NONE, SPK.C, SPK.N], [SPK.NONE, SPK.B, SPK.C, SPK.N])
    validate_phases_from_term_or_equip(network_service, "c2-t2", [SPK.A, SPK.NONE, SPK.C, SPK.N], [SPK.NONE, SPK.B, SPK.C, SPK.N])


@pytest.mark.asyncio
async def test_can_run_from_terminal():
    """
    1--c0--21--c1--21--c2--2
    """
    network_service = await (
        TestNetworkBuilder()
        .from_acls(PhaseCode.ABCN)  # c0
        .to_acls(PhaseCode.ABCN)  # c1
        .to_acls(PhaseCode.ABCN)  # c2
        .build()
    )
    await connected_equipment_trace_with_logging(network_service.objects(EnergySource))

    await SetPhases().run_with_terminal(get_t(network_service, "c1", 2))

    validate_phases_from_term_or_equip(network_service, "c0", PhaseCode.NONE, PhaseCode.NONE)
    validate_phases_from_term_or_equip(network_service, "c1", PhaseCode.NONE, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(network_service, "c2", PhaseCode.ABCN, PhaseCode.ABCN)


@pytest.mark.asyncio
async def test_must_provide_the_correct_number_of_phases():
    """
    1--c0--21--c1--2
    """
    network_service = await (
        TestNetworkBuilder()
        .from_acls(PhaseCode.A)  # c0
        .to_acls(PhaseCode.A)  # c1
        .build()
    )
    await connected_equipment_trace_with_logging(network_service.objects(EnergySource))

    with pytest.raises(TracingException) as e_info:
        await SetPhases().run_with_terminal(get_t(network_service, "c0", 2), PhaseCode.AB)

    assert str(e_info.value) == "Attempted to apply phases [A, B] to Terminal{c0-t2} with nominal phases A. Number of phases to apply must match the " \
                                "number of nominal phases. Found 2, expected 1"


@pytest.mark.asyncio
async def test_detects_cross_phasing_flow():
    """
    1--c0--21--c1--2
    """
    network_service = await (
        TestNetworkBuilder()
        .from_acls(PhaseCode.A, action=_set_normal_phase(1, SPK.A, SPK.A))
        .to_acls(PhaseCode.A, action=_set_normal_phase(1, SPK.A, SPK.B))
        .build()
    )
    await connected_equipment_trace_with_logging(network_service.objects(EnergySource))

    c1 = network_service["c1"]

    with pytest.raises(PhaseException) as e_info:
        await SetPhases().run_with_terminal(get_t(network_service, "c0", 2))

    assert e_info.value.args[0] == f"Attempted to flow conflicting phase A onto B on nominal phase A. This occurred while flowing from " \
                                   f"{list(c1.terminals)[0]} to {list(c1.terminals)[1]} through {c1}. This is caused by missing open " \
                                   f"points, or incorrect phases in upstream equipment that should be corrected in the source data."


@pytest.mark.asyncio
async def test_detects_cross_phasing_connected():
    """
    1--c0--21--c1--21--c2--2
    """
    network_service = await (
        TestNetworkBuilder()
        .from_acls(PhaseCode.A, action=_set_normal_phase(1, SPK.A, SPK.A))
        .to_acls(PhaseCode.A)
        .to_acls(PhaseCode.A, action=_set_normal_phase(0, SPK.A, SPK.B))
        .build()
    )
    await connected_equipment_trace_with_logging(network_service.objects(EnergySource))

    c1 = network_service["c1"]
    c2 = network_service["c2"]

    with pytest.raises(PhaseException) as e_info:
        await SetPhases().run_with_terminal(get_t(network_service, "c0", 2))

    assert e_info.value.args[0] == f"Attempted to flow conflicting phase A onto B on nominal phase A. This occurred while flowing between " \
                                   f"{list(c1.terminals)[1]} on {c1} and {list(c2.terminals)[0]} on {c2}. This is caused by " \
                                   f"missing open points, or incorrect phases in upstream equipment that should be corrected in the source data."


@pytest.mark.asyncio
async def test_can_back_trace_through_xn_xy_transformer_loop():
    """
       1 tx1 21--\
    s0 1         c2
       2 tx3 12--/
    """
    network_service = await (
        TestNetworkBuilder()
        .from_source(PhaseCode.ABC)  # s0
        .to_power_transformer([PhaseCode.XY, PhaseCode.XN])  # tx1
        .to_acls(PhaseCode.XN)  # c2
        .to_power_transformer([PhaseCode.XN, PhaseCode.XY])  # tx3
        .connect("tx3", "s0", 2, 1)
        .build()
    )
    await connected_equipment_trace_with_logging(network_service.objects(EnergySource))

    validate_phases_from_term_or_equip(network_service, "s0", PhaseCode.ABC)
    validate_phases_from_term_or_equip(network_service, "tx1", PhaseCode.AC, PhaseCode.AN)
    validate_phases_from_term_or_equip(network_service, "c2", PhaseCode.AN, PhaseCode.AN)
    validate_phases_from_term_or_equip(network_service, "tx3", PhaseCode.AN, PhaseCode.AC)


@pytest.mark.asyncio
async def test_can_back_trace_through_xn_xy_transformer_spur():
    """
    s0 11 tx1 21--c2--21 tx3 2
    """
    network_service = await (
        TestNetworkBuilder()
        .from_source(PhaseCode.ABC)  # s0
        .to_power_transformer([PhaseCode.XY, PhaseCode.XN])  # tx1
        .to_acls(PhaseCode.XN)  # c2
        .to_power_transformer([PhaseCode.XN, PhaseCode.XY])  # tx3
        .build()
    )

    validate_phases_from_term_or_equip(network_service, "s0", PhaseCode.ABC)
    validate_phases_from_term_or_equip(network_service, "tx1", PhaseCode.AC, PhaseCode.AN)
    validate_phases_from_term_or_equip(network_service, "c2", PhaseCode.AN, PhaseCode.AN)
    validate_phases_from_term_or_equip(network_service, "tx3", PhaseCode.AN.single_phases, [SPK.A, SPK.NONE])


def _set_normal_phase(terminal_index, from_phase: SPK, to_phase: SPK):
    def action(ce: ConductingEquipment):
        list(ce.terminals)[terminal_index].normal_phases[from_phase] = to_phase

    return action
