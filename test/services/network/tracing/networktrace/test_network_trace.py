#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.testing.test_network_builder import TestNetworkBuilder


class TestNetworkTrace:

    @pytest.mark.asyncio
    async def test_can_run_large_branching_traces(self):
        builder = TestNetworkBuilder()
        network = builder.network

        builder.from_junction(num_terminals=1) \
               .to_acls()

        for i in range(250):
            builder.to_junction(mrid=f'junc-{i}', num_terminals=3) \
                   .to_acls(mrid=f'acls-{i}-top') \
                   .from_acls(mrid=f'acls-{i}-bottom') \
                   .connect(f'junc-{i}', f'acls-{i}-bottom', 2, 1)

        await Tracing.network_trace_branching().run(network['j0'].get_terminal_by_sn(1))