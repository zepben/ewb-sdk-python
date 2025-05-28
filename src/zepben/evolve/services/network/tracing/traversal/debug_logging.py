#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import functools
from logging import Logger
from types import FunctionType
from typing import TypeVar, Union

from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.evolve.services.network.tracing.traversal.step_action import StepAction
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition
from zepben.evolve.services.network.tracing.traversal.traversal_condition import TraversalCondition

T = TypeVar('T')


class DebugLoggingWrapper:

    def __init__(self, description: str, logger: Logger):
        self.description: str = description
        self._logger: Logger = logger

    def wrap(self, obj: Union[StepAction[T], TraversalCondition[T]], count: int=None):
        def wrapattr(attr, msg) -> None:
            setattr(obj, attr, self._log_method_call(getattr(obj, attr), msg))

        if isinstance(obj, StepAction):
            wrapattr('apply', f'{self.description}: stepping_on({count})' + ' [item={args[0]}, context={args[1]}]')
        elif isinstance(obj, StopCondition):
            wrapattr('should_stop', f'{self.description}: should_stop({count})' + '={result} [item={args[0]}, context={args[1]}]')
        elif isinstance(obj, QueueCondition):
            wrapattr('should_queue',  f'{self.description}: should_queue({count})' + (
                    '={result} [next_item={args[0]}, next_context={args[1]}, current_item={args[2]}, current_context={args[3]}]'))
            wrapattr('should_queue_start_item', f'{self.description}: should_queue({count})' + '={result} [item={args[0]}]')
        else:
            raise AttributeError(f'{type(self)} does not support wrapping {obj}')
        return obj

    def _log_method_call(self, func: FunctionType, log_string: str):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            msg = f"{self._logger.name}: {log_string.format(result=result, args=list(map(bool, (args))))}"
            self._logger.debug(msg)
            print(msg)
            return result
        return wrapper
