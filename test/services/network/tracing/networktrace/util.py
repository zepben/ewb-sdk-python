#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import MagicMock, Mock

from zepben.evolve import NetworkTraceStep, ConductingEquipment, StepContext


def mock_nts(path: NetworkTraceStep.Path=None,
             num_terminal_steps=0,
             num_equipment_steps=0,
             data=None
             ):
    nts = Mock(wraps=NetworkTraceStep(path, num_terminal_steps, num_equipment_steps, data))
    nts.configure_mock(
        num_terminal_steps=3,
        num_equipment_steps=1,
        path=path
    )
    return nts


def mock_nts_path(to_equipment: ConductingEquipment=None,
                  traced_internally: bool=None):
    if traced_internally:
        terminal = Mock()
        next_path = MagicMock(wraps=NetworkTraceStep.Path(terminal, terminal))
    else:
        next_path = MagicMock(wraps=NetworkTraceStep.Path(Mock(), Mock()))


    return next_path

def mock_ctx(value: int=None):
    ctx = MagicMock(spec=StepContext)
    if value is not None:
        ctx.get_value = lambda key: value

    return ctx

