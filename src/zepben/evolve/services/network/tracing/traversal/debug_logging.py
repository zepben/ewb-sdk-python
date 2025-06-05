#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import functools
from logging import Logger
from types import FunctionType
from typing import TypeVar, Union, cast, Optional, Type

from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.evolve.services.network.tracing.traversal.step_action import StepAction
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition

T = TypeVar('T')

__all__ = ['DebugLoggingWrapper']


Wrappable = Union[StepAction[T], QueueCondition[T], StopCondition[T]]

data = {
    StepAction: [('apply', ' [item={args[0]}, context={args[1]}]')],
    StopCondition: [('should_stop', '={result} [item={args[0]}, context={args[1]}]')],
    QueueCondition: [
        ('should_queue', '={result} [next_item={args[0]}, next_context={args[1]}, current_item={args[2]}, current_context={args[3]}]'),
        ('should_queue_start_item', '={result} [item={args[0]}]'),
    ],
}


class DebugLoggingWrapper:

    def __init__(self, description: str, logger: Logger):
        self.description: str = description
        self._logger: Logger = logger
        self._wrapped = {StepAction: [], StopCondition: [], QueueCondition: []}

    def wrap(self, obj: Wrappable, count: Optional[int] = None, allow_re_wrapping: bool = False):
        """
        Wrap, in place, supported methods of the object passed in.

        Supported object.methods:

        - StepAction.action
        - StopCondition.should_stop
        - QueueCondition

          - should_queue
          - should_queue_start_item

        :param obj: Instantiated object representing a condition or action in a `Traversal`
        :param count: (optional) Set the `count` in the log message
        :param allow_re_wrapping: (optional) Replace the existing logging wrapper, if it exists.
        :return: the object passed in for fluent use
        """

        def get_logger_index(_clazz: Type[Wrappable], _attr: str) -> int:
            """
            This is just a very lazy way of auto counting the number of objects wrapped
            based on their basic classification without requiring any information in the
            object aside from what it inherits from
            """

            # We need to check if the object has already been wrapped with logging so we can determine the
            #  count number we should use.
            if hasattr(getattr(obj, _attr), '__wrapped__'):
                # It has been, now we need to decide whether to use the previously assigned count by this class
                #  or - if it was wrapped with another class, we need to generate a new one.
                if obj in self._wrapped[clazz]:
                    # if it was wrapped by this class, return the original count
                    return self._wrapped[clazz].index(obj) + 1

            if obj not in self._wrapped[clazz]:
                self._wrapped[clazz].append(obj)

            # if we had a requested count number passed in, use it
            if count is not None:
                return count

            return len(self._wrapped[clazz])

        def wrap_attr(_attr: str) -> None:
            """
            Replaces the specified attr with a wrapper around the same attr to inject
            logging.

            :param _attr: Method/Function name.
            """

            # wrapped methods will have `__wrapped__` set to the original method that was wrapped - if it exists on
            #  the methods were interested in wrapping, the object has already been wrapped. We will re-wrap it, but
            #  only if we have been explicitly told its ok, otherwise we want to catch the bug.
            if (to_wrap := getattr(obj, _attr)) and hasattr(to_wrap, '__wrapped__'):
                if not allow_re_wrapping:
                    raise AttributeError(f'Wrappable cannot be rewrapped without explicitly specifying you would like to replace the logging wrapper')
                to_wrap = getattr(to_wrap, '__wrapped__')

            setattr(obj, _attr, self._log_method_call(to_wrap, f'{self.description}: {_attr}({get_logger_index(clazz, _attr)})' + msg))

        for clazz in (StepAction, StopCondition, QueueCondition):
            if isinstance(obj, clazz):
                for attr, msg in data.get(clazz):
                    wrap_attr(attr)
                return obj
        else:
            raise AttributeError(f'{type(self).__name__} does not support wrapping {obj}')

    def _log_method_call(self, func: FunctionType, log_string: str):
        """
        returns `func` wrapped with call to `self._logger` using `log_string` as the format

        :param func: any callable
        :param log_string: Log message format string to output when `attr` is called.
                    args/kwargs passed to the function are passed to `str.format()`,
                    as well as is `result` which is the result of the function itself
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            msg = f"{self._logger.name}: {log_string.format(result=result, args=args, kwargs=kwargs)}"
            self._logger.debug(msg)
            return result

        return wrapper
