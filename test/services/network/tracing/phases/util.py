#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from typing import Iterable, Optional, Union

from zepben.evolve import ConductingEquipment, connected_equipment_trace, NetworkService, SinglePhaseKind as Phase, Terminal, PhaseStatus, PhaseCode, \
    ConductingEquipmentStep

logger = logging.getLogger("phase_logger.py")


async def connected_equipment_trace_with_logging(assets: Iterable[ConductingEquipment]):
    """
    Trace the equipment connected to `assets`, logging the phases of the items that are traced.

    :param assets: An `Iterable` of `ConductingEquipment` to start tracing from.
    """
    for asset in assets:
        trace = connected_equipment_trace()
        trace.add_step_action(_log_equipment)
        await trace.run_from(asset)


def validate_phases_from_term_or_equip(
    network: NetworkService,
    mrid: str,
    expected_phases1: Union[Iterable[Phase], PhaseCode],
    expected_phases2: Optional[Union[Iterable[Phase], PhaseCode]] = None
):
    """
    Validate the phases of a `Terminal`, or all terminals of a `ConductingEquipment`. The behaviour of this function is different depending on the test subject
    type. The differences are described in the parameters below.

    :param network: The `NetworkService` to find the test subject.
    :param mrid: The `mRID` of the test subject
    :param expected_phases1: If the test subject is a `Terminal` this is the expected normal phases, otherwise this is the expected phases of the first
        terminal of the `ConductingEquipment`.
    :param expected_phases2: If the test subject is a `Terminal` this is the expected current phases, otherwise this is the expected phases of the second
        terminal of the `ConductingEquipment`.
    """
    io = network[mrid]
    if isinstance(io, Terminal):
        validate_phases(io, expected_phases1, expected_phases2)

    elif isinstance(io, ConductingEquipment):
        validate_phases(io.get_terminal_by_sn(1), expected_phases1)

        if expected_phases2:
            validate_phases(io.get_terminal_by_sn(2), expected_phases2)

    else:
        raise f"network[{mrid}] must be a Terminal or ConductingEquipment."


def validate_phases(
    terminal: Optional[Terminal],
    expected_phases_normal: Union[Iterable[Phase], PhaseCode],
    expected_phases_current: Optional[Union[Iterable[Phase], PhaseCode]] = None
):
    """
    Validate the phases of a terminal. If current phases are not provided they will be checked against the normal phases.

    :param terminal: The `Terminal` to check.
    :param expected_phases_normal: The expected normal phases.
    :param expected_phases_current: The expected current phases. If these are the same as the normal phases you can ignore this parameter.
    """
    if terminal is None:
        return

    expected_phases_current = expected_phases_current or expected_phases_normal

    _do_phase_validation(terminal, terminal.normal_phases, expected_phases_normal)
    _do_phase_validation(terminal, terminal.current_phases, expected_phases_current)


def get_t(network: NetworkService, mrid: str, sn: int) -> Terminal:
    """
    Helper function to get a terminal by conducting equipment mRID and sequence number.

    :param network: The `NetworkService` to search.
    :param mrid: The `mRID` of the `ConductingEquipment` that contains the `Terminal`
    :param sn: The `sequence_number` of the `Terminal` to find.

    :return: The `Terminal` that matches the criteria.
    """
    return network[mrid].get_terminal_by_sn(sn)


async def _log_equipment(step: ConductingEquipmentStep, _: bool):
    logger.info("\n###############################"
                "\nTracing phases from: %s"
                "\n",
                step.conducting_equipment)

    def phase_info(term, phase):
        nps = term.normal_phases[phase]
        cps = term.current_phases[phase]

        return f"{{{phase}: n:{nps}, c:{cps}}}"

    for t in step.conducting_equipment.terminals:
        logger.info(
            "%s-T%s: %s",
            step.conducting_equipment.mrid,
            t.sequence_number,
            ", ".join(phase_info(t, phase) for phase in t.phases.single_phases)
        )


def _do_phase_validation(terminal: Terminal, phase_status: PhaseStatus, expected_phases: Union[Iterable[Phase], PhaseCode]):
    if list(expected_phases) == [Phase.NONE]:
        for nominal_phase in terminal.phases.single_phases:
            assert phase_status[nominal_phase] == Phase.NONE, f"nominal phase {nominal_phase}"

    else:
        count = -1
        for (count, (nominal_phase, expected_phase)) in enumerate(zip(terminal.phases.single_phases, expected_phases)):
            assert phase_status[nominal_phase] == expected_phase, \
                f"nominal phase {nominal_phase}. expected {expected_phase}, found {phase_status[nominal_phase]}"

        assert len(terminal.phases.single_phases) == count + 1, f"{terminal.phases.single_phases} should be of length {count + 1}"
