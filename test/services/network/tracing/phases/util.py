#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https: #mozilla.org/MPL/2.0/.
import logging
from typing import Iterable, Optional, Union

from zepben.evolve import ConductingEquipment, connected_equipment_trace, NetworkService, SinglePhaseKind as SPK, Terminal, PhaseStatus, PhaseCode

logger = logging.getLogger("phase_logger.py")


async def connected_equipment_trace_with_logging(assets: Iterable[ConductingEquipment]):
    for asset in assets:
        await connected_equipment_trace().add_step_action(log_equipment).trace(asset)


async def log_equipment(conducting_equipment: ConductingEquipment, _: bool):
    logger.info(f"\n###############################"
                f"\nTracing phases from: {conducting_equipment}"
                f"\n")

    for term in conducting_equipment.terminals:
        def phase_info(phase):
            nps = term.normal_phases[phase]
            cps = term.current_phases[phase]

            return f"{{{phase}: n:{nps}, c:{cps}}}"

        logger.info(f"{conducting_equipment.mrid}-T{term.sequence_number}: " + ", ".join(phase_info(phase) for phase in term.phases.single_phases))


def validate_phases_from_term_or_equip(
    network: NetworkService,
    mrid: str,
    expected_phases1: Union[Iterable[SPK], PhaseCode],
    expected_phases2: Optional[Union[Iterable[SPK], PhaseCode]] = None
):
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
    expected_phases_normal: Union[Iterable[SPK], PhaseCode],
    expected_phases_current: Optional[Union[Iterable[SPK], PhaseCode]] = None
):
    if terminal is None:
        return

    expected_phases_current = expected_phases_current or expected_phases_normal

    do_phase_validation(terminal, terminal.normal_phases, expected_phases_normal)
    do_phase_validation(terminal, terminal.current_phases, expected_phases_current)


def do_phase_validation(terminal: Terminal, phase_status: PhaseStatus, expected_phases: Union[Iterable[SPK], PhaseCode]):
    if list(expected_phases) == [SPK.NONE]:
        for nominal_phase in terminal.phases.single_phases:
            assert phase_status[nominal_phase] == SPK.NONE, f"nominal phase {nominal_phase}"

    else:
        count = -1
        for (count, (nominal_phase, expected_phase)) in enumerate(zip(terminal.phases.single_phases, expected_phases)):
            assert phase_status[nominal_phase] == expected_phase, \
                f"nominal phase {nominal_phase}. expected {expected_phase}, found {phase_status[nominal_phase]}"

        assert len(terminal.phases.single_phases) == count + 1, f"{terminal.phases.single_phases} should be of length {count + 1}"


def get_t(network: NetworkService, mrid: str, sn: int):
    return network[mrid].get_terminal_by_sn(sn)
