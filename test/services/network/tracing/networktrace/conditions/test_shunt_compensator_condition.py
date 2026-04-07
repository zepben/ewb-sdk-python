#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import MagicMock

from zepben.ewb import LinearShuntCompensator, Terminal, generate_id, PhaseCode, NetworkTraceStep, ConductingEquipment
# noinspection PyProtectedMember
from zepben.ewb.services.network.tracing.networktrace.conditions.shunt_compensator_condition import _ShuntCompensatorCondition


#
# TODO: This should be moved into utils, but there is already a copy there that seems busted, so some time and
#       understanding is required to resolve this.
#
def mock_nts(step_type: NetworkTraceStep.Type) -> NetworkTraceStep:
    next_step = MagicMock(spec=NetworkTraceStep)

    next_step.type = lambda: step_type

    return next_step


#
# TODO: This should be moved into utils, but there is already a copy there that seems busted, so some time and
#       understanding is required to resolve this.
#
def mock_nts_path(
    to_equipment: ConductingEquipment,
    traced_internally: bool,
) -> NetworkTraceStep.Path:
    next_path = MagicMock(spec=NetworkTraceStep.Path)

    next_path.to_equipment = to_equipment
    next_path.traced_internally = traced_internally

    return next_path


class TestShuntCompensatorCondition:

    def setup_method(self):
        self.shunt_compensator = LinearShuntCompensator(mrid="sc")
        self.from_term = Terminal(mrid=generate_id())
        self.to_term = Terminal(mrid=generate_id())
        self.ground_term = Terminal(mrid=generate_id())

        self.shunt_compensator.add_terminal(self.from_term)
        self.shunt_compensator.add_terminal(self.to_term)
        self.ground_term.phases = PhaseCode.N
        self.shunt_compensator.grounding_terminal = self.ground_term

    def test_always_queues_external_steps(self):
        self._validate_queues(mock_nts(step_type=NetworkTraceStep.Type.EXTERNAL))

    def test_always_queues_non_shunt_compensator_equipment(self):
        self._validate_queues(
            self._step_of(
                mock_nts_path(to_equipment=ConductingEquipment(mrid="non-shunt-compensator"), traced_internally=True)
            )
        )

    def test_queues_shunt_compensator_paths_that_dont_use_the_grounding_terminal(self):
        self._validate_queues(self._step_of(NetworkTraceStep.Path(self.from_term, self.to_term)))

    def test_does_not_queue_from_grounding_terminal(self):
        self._validate_queues(self._step_of(NetworkTraceStep.Path(self.ground_term, self.to_term)), should_queue=False)

    def test_does_not_queue_onto_grounding_terminal(self):
        self._validate_queues(self._step_of(NetworkTraceStep.Path(self.from_term, self.ground_term)), should_queue=False)

    @staticmethod
    def _step_of(path: NetworkTraceStep.Path) -> NetworkTraceStep:
        return NetworkTraceStep(path, 0, 0, None)

    @staticmethod
    def _validate_queues(next_step: NetworkTraceStep, should_queue: bool = True):
        result = _ShuntCompensatorCondition._StopOnGround().should_queue(next_step, MagicMock(), MagicMock(), MagicMock())
        assert result == should_queue
