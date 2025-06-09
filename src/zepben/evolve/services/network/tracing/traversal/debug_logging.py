#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import functools
from logging import Logger
from types import FunctionType
from typing import TypeVar, Union, Optional, Type

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

        Supported methods by object class::

            - :method:`StepAction.action`
            - :method:`StopCondition.should_stop`
            - :class:`QueueCondition`
              - :method:`should_queue`
              - :method:`should_queue_start_item`

        :param obj: Instantiated object representing a condition or action in a :class:`zepben.evolve.Traversal`.
        :param count: (optional) Set the ``count`` in the log message.
        :param allow_re_wrapping: (optional) Replace the existing logging wrapper, if it exists.
        :return: the object passed in for fluent use.

        :raises AttributeError: If wrapping the passed in object type is not supported.
        """

        def get_logger_index(_clazz: Type[Wrappable], _attr: str) -> int:
            """
            This is just a very lazy way of auto counting the number of objects wrapped
            based on their basic classification without requiring any information in the
            object aside from what it inherits from
            """

            # if we had a requested count number passed in, we can skip the auto-indexing logic.
            if count is not None:
                return count

            # We need to check if the object has already been wrapped with logging so we can determine the
            #  index number we should use.
            if hasattr(obj, '__wrapped__'):
                # Check to see if it's in our `_wrapped` registry - if so this class wrapped it.
                if obj in self._wrapped[clazz]:
                    # if it was wrapped by this class, return the original index. (list index +1)
                    return self._wrapped[clazz].index(obj) + 1

            # If the object has not been wrapped by this specific class instance, we generate a new index.
            if obj not in self._wrapped[clazz]:
                self._wrapped[clazz].append(obj)
            else:  # This code path should NEVER be reached as we should never have an object at this point that is not in our `_wrapped` registry
                raise IndexError(f'INTERNAL ERROR: {obj} not found in self._wrapped(\n{self._wrapped}\n)')

            return len(self._wrapped[clazz])

        def wrap_attr(_attr: str) -> None:
            """
            Replaces the specified attr with a wrapper around the same attr to inject
            logging.

            :param _attr: Method/Function name.
            :raises AttributeError: if the ``Wrappable`` cannot be rewrapped
            """

            # wrapped methods will have `__wrapped__` set to the original method that was wrapped - if it exists on
            #  the methods were interested in wrapping, the object has already been wrapped. We will re-wrap it, but
            #  only if we have been explicitly told it's ok, otherwise we want to catch the bug.
            if (to_wrap := getattr(obj, _attr)) and hasattr(to_wrap, '__wrapped__'):
                if not allow_re_wrapping:
                    raise AttributeError(f'Wrappable cannot be rewrapped without explicitly specifying you would like to replace the logging wrapper')
                to_wrap = getattr(to_wrap, '__wrapped__')

            setattr(obj, _attr, self._log_method_call(to_wrap, f'{self.description}: {_attr}({get_logger_index(clazz, _attr)})' + msg))
            setattr(obj, '__wrapped__', True)

        for clazz in (StepAction, StopCondition, QueueCondition):
            if isinstance(obj, clazz):
                for attr, msg in data.get(clazz):
                    wrap_attr(attr)
                return obj
        else:
            raise AttributeError(f'{type(self).__name__} does not support wrapping {obj}')

    def _log_method_call(self, func: FunctionType, log_string: str):
        """
        returns ``func`` wrapped with call to ``self._logger`` using ``log_string`` as the format

        :param func: any callable
        :param log_string: Log message format string to output when ``attr`` is called, args/kwargs
         passed to the function are passed to :code:`str.format()`, as well as is ``result`` which is the
         result of the function itself
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            msg = f"{self._logger.name}: {log_string.format(result=result, args=args, kwargs=kwargs)}"
            self._logger.debug(msg)
            return result

        return wrapper
