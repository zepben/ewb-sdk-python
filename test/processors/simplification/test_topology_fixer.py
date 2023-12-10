#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve import NetworkService, Terminal, EnergySource, ConnectivityNode
from zepben.evolve.processors.simplification.topology_fixer import TopologyFixer


class TestTopologyFixer:

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_removes_terminals_without_equipment(self):
        service = NetworkService()
        terminal = Terminal(mrid="t")
        service.add(terminal)
        service.connect_by_mrid(terminal, "cn")
        result = await TopologyFixer().process(service)

        assert len(list(service.objects(Terminal))) == 0
        assert result.originalToNew == {"t": set()}
        assert result.newToOriginal == {}

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_ensure_each_terminal_is_connected(self):
        service = NetworkService()
        terminal = Terminal(mrid="t")
        service.add(terminal)
        energy_source = EnergySource()
        energy_source.add_terminal(terminal)
        service.add(energy_source)

        result = await TopologyFixer().process(service)

        assert len(list(service.objects(ConnectivityNode))) == 1
        cn = next(service.objects(ConnectivityNode))
        assert terminal.connectivity_node is cn
        assert result.originalToNew == {}
        assert result.newToOriginal == {cn: set()}

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_removes_disconnected_connectivity_nodes(self):
        service = NetworkService()
        connectivity_node = ConnectivityNode(mrid="cn")
        service.add(connectivity_node)

        result = await TopologyFixer().process(service)

        assert len(list(service.objects(ConnectivityNode))) == 0
        assert result.originalToNew == {"cn": set()}
        assert result.newToOriginal == {}
