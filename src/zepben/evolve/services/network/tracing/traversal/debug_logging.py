#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ['DebugLoggingWrapper']

import copy
import functools
from logging import Logger
from types import FunctionType
from typing import TypeVar, Union, Type, List, Tuple, Dict

from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.evolve.services.network.tracing.traversal.step_action import StepAction
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition

T = TypeVar('T')

Wrappable = Union[StepAction[T], QueueCondition[T], StopCondition[T]]

DebugLoggingDataParam = List[Tuple[Union[Tuple[str, str], str], str]]

# class_to_wrap:
#       - attr_name: 'attr_name=(log_msg)'
#       - (attr_name, log_name): 'log_name=(log_msg)'
_data: Dict[Type[Wrappable], DebugLoggingDataParam] = {
    StepAction: [(('apply', 'stepped_on'), ' [item={args[0]}, context={args[1]}]')],
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
        self._wrapped = {
            StepAction: 0,
            StopCondition: 0,
            QueueCondition: 0
        }

    def wrap(self, obj: Wrappable):
        """
        Return a new object with debug logging wrappers applied to supported methods of the object.

        Supported methods by object class::

            - :meth:`StepAction.action`
            - :meth:`StopCondition.should_stop`
            - :class:`QueueCondition`
              - :meth:`should_queue`
              - :meth:`should_queue_start_item`

        :param obj: Instantiated object representing a condition or action in a :class:`zepben.evolve.Traversal`.
        :return: new copy of the object passed in for fluent use.

        :raises AttributeError: If wrapping the passed in object type is not supported.
        """

        # Create a shallow copy of the object as early as possible to avoid accidentally modifying the original.
        w_obj = copy.copy(obj)

        def _get_logger_index(_clazz: Type[Wrappable]) -> int:
            """
            This is just a very lazy way of auto counting the number of objects wrapped
            based on their basic classification without requiring any information in the
            object aside from what it inherits from.

            """

            self._wrapped[clazz] += 1
            return self._wrapped[clazz]

        def _wrap_attr(_index: int, _attr: str, _msg: str) -> None:
            """
            Replaces the specified attr with a wrapper around the same attr to inject
            logging.

            :param _attr: Method/Function name.
            :raises AttributeError: if ``wrappable`` is already wrapped
            """

            if isinstance(_attr, tuple):
                _attr_name, _log_attr_name = _attr
            else:
                _attr_name = _log_attr_name = _attr

            to_wrap = getattr(w_obj, _attr_name)

            setattr(w_obj, _attr_name, self._log_method_call(to_wrap, f'{self.description}: {_log_attr_name}({_index})' + _msg))

        for clazz in (StepAction, StopCondition, QueueCondition):
            if isinstance(w_obj, clazz):
                index = _get_logger_index(clazz)
                for attr, msg in _data.get(clazz):
                    _wrap_attr(index, attr, msg)
                return w_obj
        else:
            raise NotImplementedError(f'{type(self).__name__} does not support wrapping {obj}')

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
