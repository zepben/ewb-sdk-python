#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclassy import dataclass

from zepben.evolve import FifoQueue, normal_direction, BranchRecursiveTraversal, current_direction, NetworkService, Terminal, FeederDirection
from zepben.evolve.types import DirectionSelector

__all__ = ["RemoveDirection"]


@dataclass(slots=True)
class TerminalDirection:
    """
    A terminal linked with a direction
    """

    terminal: Terminal
    direction_to_ebb: FeederDirection


class RemoveDirection:
    """
    Convenience class that provides methods for removing feeder direction on a [NetworkService]
    This class is backed by a [BranchRecursiveTraversal].
    """

    def __init__(self) -> None:
        super().__init__()

        # noinspection PyArgumentList
        self.normal_traversal: BranchRecursiveTraversal[TerminalDirection] = BranchRecursiveTraversal(
            queue_next=lambda current, traversal: self._ebb_and_queue(traversal, current, normal_direction),
            process_queue=FifoQueue(),
            branch_queue=FifoQueue()
        )
        """
        The [BranchRecursiveTraversal] used when tracing the normal state of the network.

        NOTE: If you add stop conditions to this traversal it may no longer work correctly, use at your own risk.
        """

        # noinspection PyArgumentList
        self.current_traversal: BranchRecursiveTraversal[TerminalDirection] = BranchRecursiveTraversal(
            queue_next=lambda current, traversal: self._ebb_and_queue(traversal, current, current_direction),
            process_queue=FifoQueue(),
            branch_queue=FifoQueue()
        )
        """
        The [BranchRecursiveTraversal] used when tracing the current state of the network.

        NOTE: If you add stop conditions to this traversal it may no longer work correctly, use at your own risk.
        """

    @staticmethod
    def run(network_service: NetworkService):
        """
        Remove all feeder directions from the specified network.

        :param network_service: The network service to remove feeder directions from.
        """
        for terminal in network_service.objects(Terminal):
            terminal.normal_feeder_direction = FeederDirection.NONE
            terminal.current_feeder_direction = FeederDirection.NONE

    async def run_terminal(self, terminal: Terminal, direction: FeederDirection = FeederDirection.NONE):
        """
        Allows the removal of feeder direction from a terminal and the connected equipment chain.

        :param terminal: The terminal from which to start the direction removal.
        :param direction: The feeder direction to remove. Defaults to all present directions. Specifying [FeederDirection.BOTH] will cause all directions
                          to be cleared from all connected equipment.
        """
        await self._run_from_terminal(
            self.normal_traversal,
            TerminalDirection(terminal, self._validate_direction(direction, terminal.normal_feeder_direction))
        )
        await self._run_from_terminal(
            self.current_traversal,
            TerminalDirection(terminal, self._validate_direction(direction, terminal.current_feeder_direction))
        )

    @staticmethod
    async def _run_from_terminal(traversal: BranchRecursiveTraversal[TerminalDirection], start: TerminalDirection):
        await traversal.reset().run(start)

    def _ebb_and_queue(self, traversal: BranchRecursiveTraversal[TerminalDirection], current: TerminalDirection, direction_selector: DirectionSelector):
        if not direction_selector(current.terminal).remove(current.direction_to_ebb):
            return

        other_terminals = [t for t in current.terminal.connectivity_node or [] if t != current.terminal]

        if current.direction_to_ebb == FeederDirection.BOTH:
            for other in other_terminals:
                if direction_selector(other).remove(FeederDirection.BOTH):
                    self._queue_if_required(traversal, other, FeederDirection.BOTH, direction_selector)
        else:
            #
            # Check the number of other terminals with same direction:
            #    0:  remove opposite direction from all other terminals.
            #    1:  remove opposite direction from only the matched terminal.
            #    2+: do not queue or remove anything else as everything is still valid.
            #
            opposite_direction = self._find_opposite(current.direction_to_ebb)
            matching_terminals = [t for t in other_terminals if current.direction_to_ebb in direction_selector(t).value()]
            if not matching_terminals:
                for other in other_terminals:
                    if direction_selector(other).remove(opposite_direction):
                        self._queue_if_required(traversal, other, opposite_direction, direction_selector)

                for other in other_terminals:
                    traversal.process_queue.put(TerminalDirection(other, opposite_direction))
            elif len(matching_terminals) == 1:
                match = matching_terminals[0]
                if direction_selector(match).remove(opposite_direction):
                    self._queue_if_required(traversal, match, opposite_direction, direction_selector)

    def _queue_if_required(
        self,
        traversal: BranchRecursiveTraversal[TerminalDirection],
        terminal: Terminal,
        direction_ebbed: FeederDirection,
        direction_selector: DirectionSelector
    ):
        ce = terminal.conducting_equipment
        if not ce:
            return
        other_terminals = [t for t in ce.terminals if t != terminal]

        if direction_ebbed == FeederDirection.BOTH:
            for other in other_terminals:
                traversal.process_queue.put(TerminalDirection(other, direction_ebbed))
        else:
            #
            # Check the number of other terminals with same direction:
            #    0:  remove opposite direction from all other terminals.
            #    1:  remove opposite direction from only the matched terminal.
            #    2+: do not queue or remove anything else as everything is still valid.
            #
            opposite_direction = self._find_opposite(direction_ebbed)
            matching_terminals = [t for t in other_terminals if direction_ebbed in direction_selector(t).value()]
            if not matching_terminals:
                for other in other_terminals:
                    traversal.process_queue.put(TerminalDirection(other, opposite_direction))
            elif len(matching_terminals) == 1:
                traversal.process_queue.put(TerminalDirection(matching_terminals[0], opposite_direction))

    @staticmethod
    def _validate_direction(direction: FeederDirection, default: FeederDirection) -> FeederDirection:
        if direction == FeederDirection.NONE:
            return default
        return direction

    @staticmethod
    def _find_opposite(direction: FeederDirection) -> FeederDirection:
        # This will never be called for NONE or BOTH.
        if direction == FeederDirection.UPSTREAM:
            return FeederDirection.DOWNSTREAM
        return FeederDirection.UPSTREAM
