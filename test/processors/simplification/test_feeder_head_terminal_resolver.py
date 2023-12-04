#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import Mock

import pytest
from zepben.evolve.processors.simplification.reshape import Reshape

from zepben.evolve import NetworkService, ConnectivityNode, Terminal, Breaker, Feeder, FeederDirection
from zepben.evolve.processors.simplification.feeder_head_terminal_resolver import FeederHeadTerminalResolver


class TestFeederHeadTerminalResolver:

    def before_test(self):  # this is lazy even for me
        self.service = NetworkService()
        self.cn = ConnectivityNode(mrid="cn")
        self.service.add(self.cn)

        self.newHeadTerminal = Terminal()
        self.service.add(self.newHeadTerminal)
        self.service.connect_by_mrid(self.newHeadTerminal, "cn")

        self.breaker = Breaker()
        self.breaker.add_terminal(self.newHeadTerminal)
        self.service.add(self.breaker)

        self.feeder = Feeder("fdr")
        self.feeder.add_equipment(self.breaker)
        self.feeder.add_current_equipment(self.breaker)
        self.feeder.normal_head_terminal = Terminal(mrid="oldHeadTerminal")
        self.service.add(self.feeder)

        self.issues = Mock()

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_head_terminal_replaced_by_single_terminal(self):
        self.before_test()
        FeederHeadTerminalResolver(self.issues).process(self.service,
                                                        Reshape({"oldHeadTerminal": {self.newHeadTerminal}},
                                                                {self.newHeadTerminal: {"oldHeadTerminal"}}))
        assert self.feeder.normal_head_terminal is self.newHeadTerminal
        self.verifyContainedEquipmentAndIssues()

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_head_terminal_replaced_by_single_connectivity_node(self):
        self.before_test()
        FeederHeadTerminalResolver(self.issues).process(self.service,
                                                        Reshape({"oldHeadTerminal": {self.cn}},
                                                                {self.cn: {"oldHeadTerminal"}}))
        assert self.feeder.normal_head_terminal is self.newHeadTerminal
        self.verifyContainedEquipmentAndIssues()

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_head_terminal_replaced_by_nothing(self):
        self.before_test()
        FeederHeadTerminalResolver(self.issues).process(self.service,
                                                        Reshape({"oldHeadTerminal": set()},
                                                                {}))

        assert self.feeder.normal_head_terminal is None
        self.issues.headTerminalMappedToNothing.track.assert_called_once_with("Feeder fdr's head terminal oldHeadTerminal was replaced by nothing. The head "
                                                                              "terminal will be unassigned.")
        self.verifyContainedEquipmentAndIssues()

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_head_terminal_replaced_by_multiple_Objects(self):
        self.before_test()
        FeederHeadTerminalResolver(self.issues).process(self.service,
                                                        Reshape({"oldHeadTerminal": {self.newHeadTerminal, self.cn}},
                                                                {self.cn: {"oldHeadTerminal"}, self.newHeadTerminal: {"oldHeadTerminal"}}))

        assert self.feeder.normal_head_terminal is None
        self.issues.headTerminalMappedToMultipleObjects.track.assert_called_once_with("Feeder fdr's head terminal oldHeadTerminal was replaced by multiple "
                                                                                      "objects. The head terminal will be unassigned.")
        self.verifyContainedEquipmentAndIssues()

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_head_terminal_replaced_by_invalid_Objects(self):
        self.before_test()
        FeederHeadTerminalResolver(self.issues).process(self.service,
                                                        Reshape({"oldHeadTerminal": {self.breaker}},
                                                                {self.breaker: {"oldHeadTerminal"}}))

        assert self.feeder.normal_head_terminal is None
        self.issues.headTerminalMappedToInvalidObject.track.assert_called_once_with("Feeder fdr's head terminal oldHeadTerminal was replaced by something "
                                                                                    f'other than a terminal or connectivity node: {self.breaker}. The head '
                                                                                    f'terminal will be unassigned.')
        self.verifyContainedEquipmentAndIssues()

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_head_terminal_replaced_by_node_without_non_upstream_terminal(self):
        self.before_test()
        self.newHeadTerminal.normal_feeder_direction = FeederDirection.UPSTREAM
        FeederHeadTerminalResolver(self.issues).process(self.service,
                                                        Reshape({"oldHeadTerminal": {self.cn}},
                                                                {self.cn: {"oldHeadTerminal"}}))

        assert self.feeder.normal_head_terminal is None
        self.issues.noValidTerminalFoundForTargetNode.track.assert_called_once_with("Feeder fdr's head terminal oldHeadTerminal was replaced by connectivity "
                                                                                    "node cn, which had no valid connected terminal. The head terminal will "
                                                                                    "be unassigned.")
        self.verifyContainedEquipmentAndIssues()

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_uses_provided_feeder_direction_property_to_find_non_upstream_terminal(self):
        self.before_test()
        self.newHeadTerminal.normal_feeder_direction = FeederDirection.UPSTREAM
        FeederHeadTerminalResolver(self.issues, "current_feeder_direction").process(self.service,
                                                                                    Reshape({"oldHeadTerminal": {self.cn}},
                                                                                            {self.cn: {"oldHeadTerminal"}}))

        assert self.feeder.normal_head_terminal is self.newHeadTerminal
        self.verifyContainedEquipmentAndIssues()

    def verifyContainedEquipmentAndIssues(self):
        assert self.breaker in self.feeder.equipment
        assert self.breaker in self.feeder.current_equipment
