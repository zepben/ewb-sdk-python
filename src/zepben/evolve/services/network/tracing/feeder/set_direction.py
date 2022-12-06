#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Callable

from zepben.evolve import BranchRecursiveTraversal, Terminal, FifoQueue, NetworkService, Feeder, FeederDirection, normally_open, \
    currently_open, current_direction, normal_direction
from zepben.evolve.types import OpenTest, DirectionSelector

__all__ = ["SetDirection"]


class SetDirection:
    """
    Convenience class that provides methods for setting feeder direction on a [NetworkService]
    This class is backed by a [BranchRecursiveTraversal].
    """

    def __init__(self) -> None:
        super().__init__()

        # noinspection PyArgumentList
        self.normal_traversal: BranchRecursiveTraversal[Terminal] = BranchRecursiveTraversal(
            queue_next=lambda terminal, traversal: self._set_downstream_and_queue_next(traversal, terminal, normally_open, normal_direction),
            process_queue=FifoQueue(),
            branch_queue=FifoQueue()
        )
        """
         The [BranchRecursiveTraversal] used when tracing the normal state of the network.
    
         NOTE: If you add stop conditions to this traversal it may no longer work correctly, use at your own risk.
         """

        # noinspection PyArgumentList
        self.current_traversal: BranchRecursiveTraversal[Terminal] = BranchRecursiveTraversal(
            queue_next=lambda terminal, traversal: self._set_downstream_and_queue_next(traversal, terminal, currently_open, current_direction),
            process_queue=FifoQueue(),
            branch_queue=FifoQueue()
        )
        """
         The [BranchRecursiveTraversal] used when tracing the current state of the network.
    
         NOTE: If you add stop conditions to this traversal it may no longer work correctly, use at your own risk.
         """

    async def run(self, network: NetworkService):
        """
         Apply feeder directions from all feeder head terminals in the network.

         :param network: The network in which to apply feeder directions.
         """
        await self._run_terminals([f.normal_head_terminal for f in network.objects(Feeder) if f.normal_head_terminal])

    async def run_terminal(self, terminal: Terminal):
        """
         Apply [FeederDirection.DOWNSTREAM] from the [terminal].

         :param terminal: The terminal to start applying feeder direction from.
         """
        await self._run_terminals([terminal])

    async def _run_terminals(self, start_terminals: List[Terminal]):
        self.normal_traversal.tracker.clear()
        self.current_traversal.tracker.clear()

        for t in start_terminals:
            await self.normal_traversal.reset().run(t)
            await self.current_traversal.reset().run(t)

    def _set_downstream_and_queue_next(
        self,
        traversal: BranchRecursiveTraversal[Terminal],
        terminal: Terminal,
        open_test: OpenTest,
        direction_selector: DirectionSelector
    ):
        direction = direction_selector(terminal)
        if not direction.add(FeederDirection.DOWNSTREAM):
            return

        connected = [t for t in terminal.connectivity_node or [] if t != terminal]
        processor = self._flow_upstream_and_queue_next_straight if len(connected) == 1 else self._flow_upstream_and_queue_next_branch

        for t in connected:
            # noinspection PyArgumentList
            processor(traversal, t, open_test, direction_selector)

    @staticmethod
    def _is_feeder_head_terminal(terminal: Terminal) -> bool:
        ce = terminal.conducting_equipment
        if not ce:
            return False

        return any(f.normal_head_terminal == terminal for f in ce.containers if isinstance(f, Feeder))

    def _flow_upstream_and_queue_next_straight(
        self,
        traversal: BranchRecursiveTraversal[Terminal],
        terminal: Terminal,
        open_test: OpenTest,
        direction_selector: DirectionSelector
    ):
        if not traversal.tracker.visit(terminal):
            return

        if terminal.conducting_equipment and (terminal.conducting_equipment.num_terminals() == 2):
            self._flow_upstream_and_queue_next(terminal, open_test, direction_selector, traversal.process_queue.put)
        else:
            self._flow_upstream_and_queue_next(terminal, open_test, direction_selector, lambda it: self._start_new_branch(traversal, it))

    def _flow_upstream_and_queue_next_branch(
        self,
        traversal: BranchRecursiveTraversal[Terminal],
        terminal: Terminal,
        open_test: OpenTest,
        direction_selector: DirectionSelector
    ):
        # We don't want to visit the upstream terminal if we have branched as it prevents the downstream path of a loop processing correctly, but we
        # still need to make sure we don't re-visit the upstream terminal.
        if traversal.has_visited(terminal):
            return

        self._flow_upstream_and_queue_next(terminal, open_test, direction_selector, lambda it: self._start_new_branch(traversal, it))

    def _flow_upstream_and_queue_next(
        self,
        terminal: Terminal,
        open_test: OpenTest,
        direction_selector: DirectionSelector,
        queue: Callable[[Terminal], None]
    ):
        direction = direction_selector(terminal)
        if not direction.add(FeederDirection.UPSTREAM):
            return

        if self._is_feeder_head_terminal(terminal):
            return

        ce = terminal.conducting_equipment
        if not ce:
            return
        if open_test(ce, None):
            return

        for t in ce.terminals:
            if t != terminal:
                queue(t)

    @staticmethod
    def _start_new_branch(traversal: BranchRecursiveTraversal[Terminal], terminal: Terminal):
        branch = traversal.create_branch()
        branch.start_item = terminal
        traversal.branch_queue.put(branch)
