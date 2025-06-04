#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from logging import Logger
from types import FunctionType
from typing import TypeVar, Union, cast, Optional, Type

from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.evolve.services.network.tracing.traversal.step_action import StepAction
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition

T = TypeVar('T')

Wrappable = Union[StepAction[T], QueueCondition[T], StopCondition[T]]


class DebugLoggingWrapper:

    _wrapped = {
        StepAction: [],
        StopCondition: [],
        QueueCondition: []
    }

    def __init__(self, description: str, logger: Logger):
        self.description: str = description
        self._logger: Logger = logger

    def wrap(self, obj: Wrappable, count: Optional[int]=None):
        """
        Wrap, in place, supported methods of the object passed in.

        Supported object.methods:

        - StepAction.action
        - StopCondition.should_stop
        - QueueCondition

          - should_queue
          - should_queue_start_item

        :param obj: instantiated object representing a condition or action in a `Traversal`
        :param count: (optional) set the `count` in the log message
        :return: the object passed in for fluent use
        """

        def wrapobj(_clazz: Type[Wrappable]) -> int:
            """
            This is just a very lazy way of auto counting the number of objects wrapped
            based on their basic classification without requiring any information in the
            object aside from what it inherits from
            """

            self._wrapped[clazz].append(obj)
            if count is not None:
                return count
            return len(self._wrapped[clazz])

        def wrapattr(attr: str, msg: str) -> None:
            """
            Replaces the specified attr with a wrapper around the same attr to inject
            logging.

            :param attr: Method/Function name.
            :param msg: Log message format string to output when `attr` is called.
                        args/kwargs passed to the function are passed to `str.format()`,
                        as is `result` which is the result of the function itself
            """

            setattr(obj, attr, self._log_method_call(getattr(obj, attr), msg))

        # FIXME: when we drop 3.9 support, this can be replaced with a match case statement based
        #  on the below one-liner, and multiple calls to _count can be dropped as we will know the
        #  class before hitting any of the case blocks.
        #  _subtype = [t for t in (StepAction, StopCondition, QueueCondition) if t in type(obj).mro()].pop() or None

        if isinstance(obj, clazz := StepAction):
            _count = wrapobj(clazz)
            wrapattr('apply', f'{self.description}: stepping_on({_count})' + ' [item={args[0]}, context={args[1]}]')

        elif isinstance(obj, clazz := StopCondition):
            _count = wrapobj(clazz)
            wrapattr('should_stop', f'{self.description}: should_stop({_count})' + '={result} [item={args[0]}, context={args[1]}]')

        elif isinstance(obj, clazz := QueueCondition):
            _count = wrapobj(clazz)
            wrapattr('should_queue',  f'{self.description}: should_queue({_count})' + (
                    '={result} [next_item={args[0]}, next_context={args[1]}, current_item={args[2]}, current_context={args[3]}]'))
            wrapattr('should_queue_start_item', f'{self.description}: should_queue_start_item({_count})' + '={result} [item={args[0]}]')

        else:
            raise AttributeError(f'{type(self)} does not support wrapping {obj}')
        # This cast is for type hints, without it, any object returned is treated as a combination of all types accepted as `obj`
        return cast(clazz, obj)

    def _log_method_call(self, func: FunctionType, log_string: str):
        """
        returns `func` wrapped with call to `self._logger` using `log_string` as the format

        :param func: any callable
        :param log_string: any string supported by `str.format()`
        """

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            msg = f"{self._logger.name}: {log_string.format(result=result, args=args, kwargs=kwargs)}"
            self._logger.debug(msg)
            return result
        return wrapper
