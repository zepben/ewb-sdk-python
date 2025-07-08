#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Union, List

import pytest

from network_fixtures import phase_swap_loop_network  # noqa (Fixtures)
from services.network.tracing.phases.util import connected_equipment_trace_with_logging, validate_phases, validate_phases_from_term_or_equip, get_t
from zepben.ewb import SetPhases, EnergySource, ConductingEquipment, SinglePhaseKind as SPK, TestNetworkBuilder, PhaseCode, Breaker, NetworkStateOperators
from zepben.ewb.exceptions import TracingException, PhaseException


@pytest.mark.asyncio
@pytest.mark.parametrize('phase_swap_loop_network', [(False,)], indirect=True)
async def test_set_phases(phase_swap_loop_network):
    print(phase_swap_loop_network.__doc__)
    await SetPhases().run(phase_swap_loop_network, network_state_operators=NetworkStateOperators.NORMAL)
    await SetPhases().run(phase_swap_loop_network, network_state_operators=NetworkStateOperators.CURRENT)

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

    t = get_t(network_service, 'c1', 2)
    await SetPhases().run(t, t.phases, network_state_operators=NetworkStateOperators.NORMAL)
    await SetPhases().run(t, t.phases, network_state_operators=NetworkStateOperators.CURRENT)

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
        await SetPhases().run(get_t(network_service, "c0", 2), PhaseCode.AB, network_state_operators=NetworkStateOperators.NORMAL)
        await SetPhases().run(get_t(network_service, "c0", 2), PhaseCode.AB, network_state_operators=NetworkStateOperators.CURRENT)

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
        await SetPhases().run(get_t(network_service, "c0", 2), network_state_operators=NetworkStateOperators.NORMAL)
        await SetPhases().run(get_t(network_service, "c0", 2), network_state_operators=NetworkStateOperators.CURRENT)

    assert e_info.value.args[0] == f"Attempted to flow conflicting phase A onto B on nominal phase A. This occurred while flowing from " \
                                   f"{list(c1.terminals)[0]} to {list(c1.terminals)[1]} through {c1}. This is often caused by missing open " \
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
        await SetPhases().run(get_t(network_service, "c0", 2), network_state_operators=NetworkStateOperators.NORMAL)
        await SetPhases().run(get_t(network_service, "c0", 2), network_state_operators=NetworkStateOperators.CURRENT)

    assert e_info.value.args[0] == f"Attempted to flow conflicting phase A onto B on nominal phase A. This occurred while flowing between " \
                                   f"{list(c1.terminals)[1]} on {c1} and {list(c2.terminals)[0]} on {c2}. This is often caused by " \
                                   f"missing open points, or incorrect phases in upstream equipment that should be corrected in the source data."


@pytest.mark.asyncio
async def test_adds_neutral_through_transformers():
    #
    # s0 11--tx1--21--c2--2
    #
    n = await (TestNetworkBuilder()
               .from_source(PhaseCode.ABC)  # s0
               .to_power_transformer([PhaseCode.ABC, PhaseCode.ABCN])  # tx1
               .to_acls(PhaseCode.ABCN)  # c2
               ).build()

    validate_phases_from_term_or_equip(n, 's0', PhaseCode.ABC)
    validate_phases_from_term_or_equip(n, 'tx1', PhaseCode.ABC, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(n, 'c2', PhaseCode.ABCN, PhaseCode.ABCN)


@pytest.mark.asyncio
async def test_applies_unknown_phases_through_transformers():
    #
    # s0 11--tx1--21--c2--2
    #
    n = await (TestNetworkBuilder()
               .from_source(PhaseCode.BC)  # s0
               .to_power_transformer([PhaseCode.BC, PhaseCode.XN])  # tx1
               .to_acls(PhaseCode.XN)  # c2
               ).build()

    validate_phases_from_term_or_equip(n, 's0', PhaseCode.BC)
    validate_phases_from_term_or_equip(n, 'tx1', PhaseCode.BC, PhaseCode.BN)
    validate_phases_from_term_or_equip(n, 'c2', PhaseCode.BN, PhaseCode.BN)


@pytest.mark.asyncio
async def test_energises_transformer_phases_straight():
    # Without neutral.
    await _validate_tx_phases(*[PhaseCode.ABC] * 5)

    await _validate_tx_phases(*[PhaseCode.AB] * 5)
    await _validate_tx_phases(*[PhaseCode.BC] * 5)
    await _validate_tx_phases(*[PhaseCode.AC] * 5)

    await _validate_tx_phases(PhaseCode.AB, PhaseCode.AB, PhaseCode.XY, PhaseCode.AB, PhaseCode.AB)
    await _validate_tx_phases(PhaseCode.BC, PhaseCode.BC, PhaseCode.XY, PhaseCode.BC, PhaseCode.BC)
    await _validate_tx_phases(PhaseCode.AC, PhaseCode.AC, PhaseCode.XY, PhaseCode.AC, PhaseCode.AC)

    await _validate_tx_phases(PhaseCode.AB, PhaseCode.XY, PhaseCode.XY, PhaseCode.AB, PhaseCode.AB)
    await _validate_tx_phases(PhaseCode.BC, PhaseCode.XY, PhaseCode.XY, PhaseCode.BC, PhaseCode.BC)
    await _validate_tx_phases(PhaseCode.AC, PhaseCode.XY, PhaseCode.XY, PhaseCode.AC, PhaseCode.AC)

    await _validate_tx_phases(*[PhaseCode.A] * 5)
    await _validate_tx_phases(*[PhaseCode.B] * 5)
    await _validate_tx_phases(*[PhaseCode.C] * 5)

    await _validate_tx_phases(PhaseCode.A, PhaseCode.A, PhaseCode.X, PhaseCode.A, PhaseCode.A)
    await _validate_tx_phases(PhaseCode.B, PhaseCode.B, PhaseCode.X, PhaseCode.B, PhaseCode.B)
    await _validate_tx_phases(PhaseCode.C, PhaseCode.C, PhaseCode.X, PhaseCode.C, PhaseCode.C)

    await _validate_tx_phases(PhaseCode.A, PhaseCode.X, PhaseCode.X, PhaseCode.A, PhaseCode.A)
    await _validate_tx_phases(PhaseCode.B, PhaseCode.X, PhaseCode.X, PhaseCode.B, PhaseCode.B)
    await _validate_tx_phases(PhaseCode.C, PhaseCode.X, PhaseCode.X, PhaseCode.C, PhaseCode.C)

    # With neutral.
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.ABC, PhaseCode.ABCN, PhaseCode.ABC, PhaseCode.ABCN)

    await _validate_tx_phases(PhaseCode.AB, PhaseCode.AB, PhaseCode.ABN, PhaseCode.AB, PhaseCode.ABN)
    await _validate_tx_phases(PhaseCode.BC, PhaseCode.BC, PhaseCode.BCN, PhaseCode.BC, PhaseCode.BCN)
    await _validate_tx_phases(PhaseCode.AC, PhaseCode.AC, PhaseCode.ACN, PhaseCode.AC, PhaseCode.ACN)

    await _validate_tx_phases(PhaseCode.AB, PhaseCode.AB, PhaseCode.XYN, PhaseCode.AB, PhaseCode.ABN)
    await _validate_tx_phases(PhaseCode.BC, PhaseCode.BC, PhaseCode.XYN, PhaseCode.BC, PhaseCode.BCN)
    await _validate_tx_phases(PhaseCode.AC, PhaseCode.AC, PhaseCode.XYN, PhaseCode.AC, PhaseCode.ACN)

    await _validate_tx_phases(PhaseCode.AB, PhaseCode.XY, PhaseCode.XYN, PhaseCode.AB, PhaseCode.ABN)
    await _validate_tx_phases(PhaseCode.BC, PhaseCode.XY, PhaseCode.XYN, PhaseCode.BC, PhaseCode.BCN)
    await _validate_tx_phases(PhaseCode.AC, PhaseCode.XY, PhaseCode.XYN, PhaseCode.AC, PhaseCode.ACN)

    await _validate_tx_phases(PhaseCode.A, PhaseCode.A, PhaseCode.AN, PhaseCode.A, PhaseCode.AN)
    await _validate_tx_phases(PhaseCode.B, PhaseCode.B, PhaseCode.BN, PhaseCode.B, PhaseCode.BN)
    await _validate_tx_phases(PhaseCode.C, PhaseCode.C, PhaseCode.CN, PhaseCode.C, PhaseCode.CN)

    await _validate_tx_phases(PhaseCode.A, PhaseCode.A, PhaseCode.XN, PhaseCode.A, PhaseCode.AN)
    await _validate_tx_phases(PhaseCode.B, PhaseCode.B, PhaseCode.XN, PhaseCode.B, PhaseCode.BN)
    await _validate_tx_phases(PhaseCode.C, PhaseCode.C, PhaseCode.XN, PhaseCode.C, PhaseCode.CN)

    await _validate_tx_phases(PhaseCode.A, PhaseCode.X, PhaseCode.XN, PhaseCode.A, PhaseCode.AN)
    await _validate_tx_phases(PhaseCode.B, PhaseCode.X, PhaseCode.XN, PhaseCode.B, PhaseCode.BN)
    await _validate_tx_phases(PhaseCode.C, PhaseCode.X, PhaseCode.XN, PhaseCode.C, PhaseCode.CN)


@pytest.mark.asyncio
async def test_energises_transformer_phases_added():
    #
    # NOTE: When adding a Y phase to an X -> XY transformer that is downstream of a C, the C phase will be spread on the X and the Y
    #       will be left de-energised.
    #
    #       You could rework it so this works as intended, but there are dramatic flow on effects making sure the XY (AC) is correctly
    #       connected at the other end to follow up equipment with non XY phases. Given this is only an issue where the phases of the
    #       transformer are unknown, and this is a SWER to split-phase transformer that happens to be on the end of a C phase SWER line, and
    #       you can resolve it by specifying the transformer phases explicitly (i.e. C -> ACN), it won't be fixed for now.
    #

    # Without neutral.
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.A, PhaseCode.AB, PhaseCode.A, PhaseCode.AB)
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.B, PhaseCode.BC, PhaseCode.B, PhaseCode.BC)
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.C, PhaseCode.AC, PhaseCode.C, PhaseCode.AC)

    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.A, PhaseCode.XY, PhaseCode.A, PhaseCode.AB)
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.B, PhaseCode.XY, PhaseCode.B, PhaseCode.BC)
    # As per the note above, this is not ideal. Ideally the note above would be removed and the test below would be replaced with
    # `await _validate_tx_phases(PhaseCode.ABC, PhaseCode.C, PhaseCode.XY, PhaseCode.C, PhaseCode.AC)` and the single phase variant of
    # await _validate_tx_phases would be removed.
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.C, PhaseCode.XY, PhaseCode.C, [SPK.C, SPK.NONE])

    await _validate_tx_phases(PhaseCode.A, PhaseCode.X, PhaseCode.XY, PhaseCode.A, PhaseCode.AB)
    await _validate_tx_phases(PhaseCode.B, PhaseCode.X, PhaseCode.XY, PhaseCode.B, PhaseCode.BC)

    # As per the note above, this is not ideal. Ideally the note above would be removed and the test below would be replaced with
    # `await _validate_tx_phases(PhaseCode.C, PhaseCode.X, PhaseCode.XY, PhaseCode.C, PhaseCode.AC)` and the single phase variant of
    # await _validate_tx_phases would be removed.
    await _validate_tx_phases(PhaseCode.C, PhaseCode.X, PhaseCode.XY, PhaseCode.C, [SPK.C, SPK.NONE])

    # With neutral.
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.A, PhaseCode.ABN, PhaseCode.A, PhaseCode.ABN)
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.B, PhaseCode.BCN, PhaseCode.B, PhaseCode.BCN)
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.C, PhaseCode.ACN, PhaseCode.C, PhaseCode.ACN)

    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.A, PhaseCode.XYN, PhaseCode.A, PhaseCode.ABN)
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.B, PhaseCode.XYN, PhaseCode.B, PhaseCode.BCN)
    # As per the note above, this is not ideal. Ideally the note above would be removed and the test below would be replaced with
    # `await _validate_tx_phases(PhaseCode.ABC, PhaseCode.C, PhaseCode.XYN, PhaseCode.C, PhaseCode.ACN)` and the single phase variant of
    # await _validate_tx_phases would be removed.
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.C, PhaseCode.XYN, PhaseCode.C, [SPK.C, SPK.NONE, SPK.N])

    await _validate_tx_phases(PhaseCode.A, PhaseCode.X, PhaseCode.XYN, PhaseCode.A, PhaseCode.ABN)
    await _validate_tx_phases(PhaseCode.B, PhaseCode.X, PhaseCode.XYN, PhaseCode.B, PhaseCode.BCN)

    # As per the note above, this is not ideal. Ideally the note above would be removed and the test below would be replaced with
    # `await _validate_tx_phases(PhaseCode.C, PhaseCode.X, PhaseCode.XY, PhaseCode.C, PhaseCode.AC)` and the single phase variant of
    # await _validate_tx_phases would be removed.
    await _validate_tx_phases(PhaseCode.C, PhaseCode.X, PhaseCode.XYN, PhaseCode.C, [SPK.C, SPK.NONE, SPK.N])


@pytest.mark.asyncio
async def test_energises_transformer_phases_dropped():
    #
    # NOTE: When dropping a Y phase to an XY -> X transformer that is downstream of an AC, the A phase will be spread on the X,
    #       and the C phase will be dropped.
    #
    #       You could rework it so this works as intended, but there are dramatic flow on effects making sure the XY (AC) is correctly
    #       connected at the other end to follow up equipment with non XY phases. Given this is only an issue where the phases of the
    #       transformer are unknown, and this is a split-phase to SWER transformer that happens to be on the end of an AC line, and
    #       you can resolve it by specifying the transformer phases explicitly (i.e. ACN -> C), it won't be fixed for now.
    #

    # Without neutral.
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.AB, PhaseCode.A, PhaseCode.AB, PhaseCode.A)
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.BC, PhaseCode.B, PhaseCode.BC, PhaseCode.B)
    await _validate_tx_phases(PhaseCode.ABC, PhaseCode.AC, PhaseCode.C, PhaseCode.AC, PhaseCode.C)

    await _validate_tx_phases(PhaseCode.AB, PhaseCode.XY, PhaseCode.A, PhaseCode.AB, PhaseCode.A)
    await _validate_tx_phases(PhaseCode.BC, PhaseCode.XY, PhaseCode.B, PhaseCode.BC, PhaseCode.B)

    # As per the note above, this is not ideal. Ideally the note above would be removed and the test below would be replaced with
    # `await _validate_tx_phases(PhaseCode.AC, PhaseCode.XY, PhaseCode.C, PhaseCode.AC, PhaseCode.C)`.
    await _validate_tx_phases(PhaseCode.AC, PhaseCode.XY, PhaseCode.C, PhaseCode.AC, PhaseCode.A)

    await _validate_tx_phases(PhaseCode.AB, PhaseCode.XY, PhaseCode.X, PhaseCode.AB, PhaseCode.A)
    await _validate_tx_phases(PhaseCode.BC, PhaseCode.XY, PhaseCode.X, PhaseCode.BC, PhaseCode.B)

    # As per the note above, this is not ideal. Ideally the note above would be removed and the test below would be replaced with
    # `await _validate_tx_phases(PhaseCode.AC, PhaseCode.XY, PhaseCode.X, PhaseCode.AC, PhaseCode.C)`.
    await _validate_tx_phases(PhaseCode.AC, PhaseCode.XY, PhaseCode.X, PhaseCode.AC, PhaseCode.A)

    # With neutral.
    await _validate_tx_phases(PhaseCode.ABCN, PhaseCode.ABN, PhaseCode.A, PhaseCode.ABN, PhaseCode.A)
    await _validate_tx_phases(PhaseCode.ABCN, PhaseCode.BCN, PhaseCode.B, PhaseCode.BCN, PhaseCode.B)
    await _validate_tx_phases(PhaseCode.ABCN, PhaseCode.ACN, PhaseCode.C, PhaseCode.ACN, PhaseCode.C)

    await _validate_tx_phases(PhaseCode.ABN, PhaseCode.XYN, PhaseCode.A, PhaseCode.ABN, PhaseCode.A)
    await _validate_tx_phases(PhaseCode.BCN, PhaseCode.XYN, PhaseCode.B, PhaseCode.BCN, PhaseCode.B)
    # As per the note above, this is not ideal. Ideally the note above would be removed and the test below would be replaced with
    # `await _validate_tx_phases(PhaseCode.ACN, PhaseCode.XYN, PhaseCode.C, PhaseCode.ACN, PhaseCode.C)`.
    await _validate_tx_phases(PhaseCode.ACN, PhaseCode.XYN, PhaseCode.C, PhaseCode.ACN, PhaseCode.A)

    await _validate_tx_phases(PhaseCode.ABN, PhaseCode.XYN, PhaseCode.X, PhaseCode.ABN, PhaseCode.A)
    await _validate_tx_phases(PhaseCode.BCN, PhaseCode.XYN, PhaseCode.X, PhaseCode.BCN, PhaseCode.B)

    # As per the note above, this is not ideal. Ideally the note above would be removed and the test below would be replaced with
    # `await _validate_tx_phases(PhaseCode.ACN, PhaseCode.XYN, PhaseCode.X, PhaseCode.ACN, PhaseCode.C)`.
    await _validate_tx_phases(PhaseCode.ACN, PhaseCode.XYN, PhaseCode.X, PhaseCode.ACN, PhaseCode.A)


@pytest.mark.asyncio
async def test_applies_phases_to_unknown_hv():
    #
    # s0 11--c1--21--c2--2
    #
    n = await (TestNetworkBuilder()
               .from_source(PhaseCode.BC)  # s0
               .to_acls(PhaseCode.BC)  # c1
               .to_acls(PhaseCode.XY)  # c2
               ).build()

    validate_phases_from_term_or_equip(n, 's0', PhaseCode.BC)
    validate_phases_from_term_or_equip(n, 'c1', PhaseCode.BC, PhaseCode.BC)
    validate_phases_from_term_or_equip(n, 'c2', PhaseCode.BC, PhaseCode.BC)


@pytest.mark.asyncio
async def test_applies_phases_to_unknown_lv():
    #
    # s0 11--c1--21--c2--2
    #
    n = await (TestNetworkBuilder()
               .from_source(PhaseCode.CN)  # s0
               .to_acls(PhaseCode.CN)  # c1
               .to_acls(PhaseCode.XN)  # c2
               ).build()

    validate_phases_from_term_or_equip(n, 's0', PhaseCode.CN)
    validate_phases_from_term_or_equip(n, 'c1', PhaseCode.CN, PhaseCode.CN)
    validate_phases_from_term_or_equip(n, 'c2', PhaseCode.CN, PhaseCode.CN)


@pytest.mark.asyncio
async def test_applies_phases_on_to_swerv():
    #
    # s0 11--tx1--21--c2--2
    #
    n = await (TestNetworkBuilder()
               .from_source(PhaseCode.AC)  # s0
               .to_power_transformer([PhaseCode.AC, PhaseCode.X])  # tx1
               .to_acls(PhaseCode.X)  # c2
               ).build()

    validate_phases_from_term_or_equip(n, 's0', PhaseCode.AC)
    validate_phases_from_term_or_equip(n, 'tx1', PhaseCode.AC, PhaseCode.C)
    validate_phases_from_term_or_equip(n, 'c2', PhaseCode.C, PhaseCode.C)


@pytest.mark.asyncio
async def test_uses_transformer_paths():
    #
    # s0 11--tx1--21--c2--2
    #
    n = await (TestNetworkBuilder()
               .from_source(PhaseCode.AC)  # s0
               .to_power_transformer([PhaseCode.AC, PhaseCode.CN])  # tx1
               .to_acls(PhaseCode.CN)  # c2
               ).build()

    validate_phases_from_term_or_equip(n, 's0', PhaseCode.AC)
    validate_phases_from_term_or_equip(n, 'tx1', PhaseCode.AC, PhaseCode.CN)
    validate_phases_from_term_or_equip(n, 'c2', PhaseCode.CN, PhaseCode.CN)


@pytest.mark.asyncio
async def test_does_not_remove_phase_when_applying_subset_out_of_loop():
    #
    # s0 12-----c5------1
    #    1              2
    #   tx1            tx4
    #    2              1
    #    1--c2--21--c3--2
    #
    n = await (TestNetworkBuilder()
               .from_source(PhaseCode.ABC)  # s0
               .to_power_transformer([PhaseCode.ABC, PhaseCode.ABCN])  # tx1
               .to_acls(PhaseCode.ABCN)  # c2
               .to_acls(PhaseCode.CN)  # c3
               .to_power_transformer([PhaseCode.CN, PhaseCode.AC])  # tx4
               .to_acls(PhaseCode.ABC)  # c5
               .connect('c5', 's0', 2, 1)
               ).build()

    validate_phases_from_term_or_equip(n, 's0', PhaseCode.ABC)
    validate_phases_from_term_or_equip(n, 'tx1', PhaseCode.ABC, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(n, 'c2', PhaseCode.ABCN, PhaseCode.ABCN)
    validate_phases_from_term_or_equip(n, 'c3', PhaseCode.CN, PhaseCode.CN)
    validate_phases_from_term_or_equip(n, 'tx4', PhaseCode.CN, PhaseCode.AC)
    validate_phases_from_term_or_equip(n, 'c5', PhaseCode.ABC, PhaseCode.ABC)


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
    #
    # NOTE: This is impacted on the XY -> X issue as described elsewhere. If this is fixed you should replace the following test with
    #       `validate_phases_from_term_or_equip(network_service, "tx3", PhaseCode.AN, PhaseCode.AC)`
    #

    validate_phases_from_term_or_equip(network_service, "tx3", PhaseCode.AN, PhaseCode.AB)


def _set_normal_phase(terminal_index, from_phase: SPK, to_phase: SPK):
    def action(ce: ConductingEquipment):
        list(ce.terminals)[terminal_index].normal_phases[from_phase] = to_phase

    return action


@pytest.mark.asyncio
async def test_can_set_phases_from_an_unknown_nominal_phase():
    """
    1--c0--21--c1--2
    """
    n = TestNetworkBuilder() \
        .from_acls(PhaseCode.X) \
        .to_acls(PhaseCode.ABC) \
        .network

    acls = n['c0']
    t = get_t(n, 'c0', 2)
    t.normal_phases[SPK.X] = SPK.A
    t.current_phases[SPK.X] = SPK.A

    await SetPhases().run(t, network_state_operators=NetworkStateOperators.NORMAL)
    await SetPhases().run(t, network_state_operators=NetworkStateOperators.CURRENT)

    validate_phases_from_term_or_equip(n, 'c0', PhaseCode.NONE, PhaseCode.A)
    validate_phases_from_term_or_equip(n, 'c1', [SPK.A, SPK.NONE, SPK.NONE], [SPK.A, SPK.NONE, SPK.NONE])


@pytest.mark.asyncio
async def test_energises_around_dropped_phase_dual_transformer_loop():
    #
    # This was seen in PCOR data for a dual transformer site (BET006 - RHEOLA P58E) on a SWER line with an LV2 circuit
    #
    #            21--c3--21 tx4 21--c5--21
    #            |                       |
    #            c2                      |
    #            |                       |
    #            1                       |
    # s0 11--c1--2                       c6
    #            1                       |
    #            |                       |
    #            c7                      |
    #            |                       |
    #            21--c8--21 tx9 21--c10-221--c11-2
    ns = await (TestNetworkBuilder()
                .from_source(PhaseCode.A)  # s0
                .to_acls(PhaseCode.A)  # c1
                .to_acls(PhaseCode.A)  # c2
                .to_acls(PhaseCode.A)  # c3
                .to_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx4
                .to_acls(PhaseCode.AN)  # c5
                .to_acls(PhaseCode.AN)  # c6
                .branch_from('c1')
                .to_acls(PhaseCode.A)  # c7
                .to_acls(PhaseCode.A)  # c8
                .to_power_transformer([PhaseCode.A, PhaseCode.ABN])  # tx9
                .to_acls(PhaseCode.ABN)  # c10
                .connect_to('c6', 2)
                .to_acls(PhaseCode.ABN)  # c11
                ).build()

    validate_phases_from_term_or_equip(ns, 'c1', PhaseCode.A, PhaseCode.A)
    validate_phases_from_term_or_equip(ns, 'c2', PhaseCode.A, PhaseCode.A)
    validate_phases_from_term_or_equip(ns, 'c3', PhaseCode.A, PhaseCode.A)
    validate_phases_from_term_or_equip(ns, 'tx4', PhaseCode.A, PhaseCode.AN)
    validate_phases_from_term_or_equip(ns, 'c5', PhaseCode.AN, PhaseCode.AN)
    validate_phases_from_term_or_equip(ns, 'c6', PhaseCode.AN, PhaseCode.AN)
    validate_phases_from_term_or_equip(ns, 'c7', PhaseCode.A, PhaseCode.A)
    validate_phases_from_term_or_equip(ns, 'c8', PhaseCode.A, PhaseCode.A)
    validate_phases_from_term_or_equip(ns, 'tx9', PhaseCode.A, PhaseCode.ABN)
    validate_phases_from_term_or_equip(ns, 'c10', PhaseCode.ABN, PhaseCode.ABN)
    validate_phases_from_term_or_equip(ns, 'c11', PhaseCode.ABN, PhaseCode.ABN)


async def _validate_tx_phases(
    source_phases: PhaseCode,
    tx_phase_1: PhaseCode,
    tx_phase_2: PhaseCode,
    expected_phases_1: PhaseCode,
    expected_phases_2: Union[PhaseCode, List[SPK]]
):
    if isinstance(expected_phases_2, PhaseCode):
        expected_phases_2 = expected_phases_2.single_phases

    n = await (TestNetworkBuilder()
               .from_source(source_phases)  # s0
               .to_power_transformer([tx_phase_1, tx_phase_2])  # tx1
               .to_acls(tx_phase_2)  # c2
               ).build()
    validate_phases_from_term_or_equip(n, 's0', source_phases)
    validate_phases_from_term_or_equip(n, 'tx1', expected_phases_1.single_phases, expected_phases_2)
    validate_phases_from_term_or_equip(n, 'c2', expected_phases_2, expected_phases_2)
