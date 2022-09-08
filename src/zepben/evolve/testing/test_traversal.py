#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Callable, TypeVar, Tuple, Awaitable
from unittest.mock import Mock

T = TypeVar('T')

__all__ = ["verify_stop_conditions", "step_on_when_run", "step_on_when_run_with_is_stopping"]


async def verify_stop_conditions(traversal: Mock, *stop_condition_validation: Callable[[Callable[[T], Awaitable[None]]], Awaitable[None]]):
    """
    Verify that stop conditions are registered, and they behave correctly.

    :param traversal: The mocked `BasicTraversal` to verify.
    :param stop_condition_validation: A collection of verification blocks that are executed on each stop condition. The number of entries in this collection
                                      must match the number of expected stop conditions, and match the registration order of the stop conditions.
    """
    # To get access to private stop conditions (and to check they are actually registered) we need to capture the conditions that are registered.
    assert traversal.add_stop_condition.call_count == len(stop_condition_validation)

    for index, stop_condition_call in enumerate(traversal.add_stop_condition.call_args_list):
        await stop_condition_validation[index](stop_condition_call.args[0])


def step_on_when_run(traversal: Mock, *step_on: T):
    """
    Call the step action with the specified arguments when the trace is run. Only supports single step actions.

    :param traversal: The mocked `BasicTraversal` that will be run.
    :param step_on: A collection of items to step on when `traversal` is run.
    """

    # The step actions must be called while the trace is running, so this needs to be done in the mock of the run command.
    async def mock_run(_):
        traversal.add_step_action.assert_called_once()

        # To get access to private step actions (and to check they are actually registered) we need to capture the actions that are registered.
        step_action = traversal.add_step_action.call_args.args[0]
        for item in step_on:
            await step_action(item, False)

    traversal.run.side_effect = mock_run


def step_on_when_run_with_is_stopping(traversal: Mock, *step_on: Tuple[T, bool]):
    """
    Call the step action with the specified arguments when the trace is run. Only supports single step actions.

    :param traversal: The mocked `BasicTraversal` that will be run.
    :param step_on: A collection of items and is_stopping flags to step on when `traversal` is run.
    """

    # The step actions must be called while the trace is running, so this needs to be done in the mock of the run command.
    async def mock_run(_):
        traversal.add_step_action.assert_called_once()

        # To get access to private step actions (and to check they are actually registered) we need to capture the actions that are registered.
        step_action = traversal.add_step_action.call_args.args[0]
        for (item, is_stopping) in step_on:
            await step_action(item, is_stopping)

    traversal.run.side_effect = mock_run
