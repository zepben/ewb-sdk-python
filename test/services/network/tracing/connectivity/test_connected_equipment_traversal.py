#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch, MagicMock

import pytest

from zepben.evolve import Junction
from zepben.evolve.services.network.tracing.connectivity.connected_equipment_traversal import ConnectedEquipmentTraversal


class TestConnectedEquipmentTraversal:

    @pytest.mark.asyncio
    async def test_wraps_conducting_equipment_in_step_zero(self):
        with patch.object(ConnectedEquipmentTraversal, "run") as run:
            # noinspection PyArgumentList
            traversal = ConnectedEquipmentTraversal(MagicMock(), MagicMock(), MagicMock())
            j = Junction()

            await traversal.run_from(j)

            run.assert_called_once()
            assert run.call_args.args[0].conducting_equipment == j
            assert run.call_args.args[0].step == 0

    @pytest.mark.asyncio
    async def test_run_defaults_to_stop_on_start(self):
        with patch.object(ConnectedEquipmentTraversal, "run") as run:
            # noinspection PyArgumentList
            traversal = ConnectedEquipmentTraversal(MagicMock(), MagicMock(), MagicMock())
            await traversal.run_from(Junction())

            assert run.call_args.args[1] is True

    @pytest.mark.asyncio
    async def test_run_can_change_stop_on_start(self):
        with patch.object(ConnectedEquipmentTraversal, "run") as run:
            # noinspection PyArgumentList
            traversal = ConnectedEquipmentTraversal(MagicMock(), MagicMock(), MagicMock())
            await traversal.run_from(Junction(), False)

            assert run.call_args.args[1] is False
