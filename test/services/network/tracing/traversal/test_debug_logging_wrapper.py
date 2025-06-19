#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import queue
from contextlib import contextmanager

import pytest

from zepben.evolve import StepContext, StopCondition, QueueCondition, StepAction
from zepben.evolve.services.network.tracing.traversal.debug_logging import DebugLoggingWrapper


def bool_generator():
    while True:
        yield True
        yield False


class TestDebugLoggingWrappers:
    class ListHandler(logging.Handler):
        log_list = queue.Queue()

        def emit(self, record):
            self.log_list.put(self.format(record).rstrip('\n'))

    @contextmanager
    def _log_handler(self):
        self.logger.addHandler(handler := self.ListHandler())
        try:
            yield handler
        finally:
            self.logger.removeHandler(handler)

    logger = logging.getLogger()

    context_1 = StepContext(True, True)
    context_1.__str__ = 'context 1 string'
    assert f'{context_1}' == str(context_1)
    assert context_1.__str__ == 'context 1 string'

    context_2 = StepContext(True, True)
    context_2.__str__ = 'context 2 string'
    assert f'{context_2}' == str(context_2)
    assert context_2.__str__ == 'context 2 string'

    item_1 = (1, 1.1)
    item_2 = (2, 2.2)

    def _wrap(self, condition):
        return DebugLoggingWrapper('my desc', self.logger).wrap(condition)

    def test_wrapped_object_is_original_object(self):
        should_stop = bool_generator()

        stop_condition = StopCondition(lambda item, ctx: next(should_stop))
        wrapped = self._wrap(stop_condition)

        assert isinstance(wrapped, StopCondition)
        assert not isinstance(wrapped, (QueueCondition, StepAction))

        queue_condition = QueueCondition(lambda nitem, nctx, item, ctx: next(should_stop))
        wrapped = self._wrap(queue_condition)

        assert not isinstance(wrapped, (StopCondition, StepAction))
        assert isinstance(wrapped, QueueCondition)

        action = StepAction(lambda item, context: None)
        wrapped = self._wrap(action)

        assert not isinstance(wrapped, (StopCondition, QueueCondition))
        assert isinstance(wrapped, StepAction)

    def test_can_wrap_stop_condition(self):
        should_stop = bool_generator()

        wrapped = self._wrap(StopCondition(lambda item, ctx: next(should_stop)))

        with self._log_handler() as handler:
            assert wrapped.should_stop(self.item_1, self.context_1)
            assert not wrapped.should_stop(self.item_2, self.context_2)

            assert handler.log_list.get() == f"root: my desc: should_stop(1)=True [item={self.item_1}, context={self.context_1}]"
            assert handler.log_list.get() == f"root: my desc: should_stop(1)=False [item={self.item_2}, context={self.context_2}]"

    def test_can_wrap_queue_conditions(self):
        should_stop = bool_generator()

        condition = QueueCondition(lambda nitem, nctx, item, ctx: next(should_stop))
        condition.should_queue_start_item = lambda item: next(should_stop)
        condition = self._wrap(condition)

        with self._log_handler() as handler:
            assert condition.should_queue(self.item_1, self.context_1, self.item_2, self.context_2)
            assert not condition.should_queue(self.item_2, self.context_2, self.item_1, self.context_1)

            assert next(should_stop)  # we need to skip the `True` the generators returning next

            assert not condition.should_queue_start_item(self.item_1)
            assert condition.should_queue_start_item(self.item_2)

            assert handler.log_list.get() == (
                f"root: my desc: should_queue(1)=True ["
                f"next_item={self.item_1}, next_context={self.context_1}, current_item={self.item_2}, current_context={self.context_2}]"
            )
            assert handler.log_list.get() == (
                f"root: my desc: should_queue(1)=False ["
                f"next_item={self.item_2}, next_context={self.context_2}, current_item={self.item_1}, current_context={self.context_1}]"
            )
            assert handler.log_list.get() == f"root: my desc: should_queue_start_item(1)=False [item={self.item_1}]"
            assert handler.log_list.get() == f"root: my desc: should_queue_start_item(1)=True [item={self.item_2}]"

    def test_can_wrap_step_actions(self):
        action = self._wrap(StepAction(lambda item, context: None))

        with self._log_handler() as handler:
            action.apply(self.item_1, self.context_1)
            action.apply(self.item_2, self.context_2)

            assert handler.log_list.get() == f"root: my desc: stepped_on(1) [item={self.item_1}, context={self.context_1}]"
            assert handler.log_list.get() == f"root: my desc: stepped_on(1) [item={self.item_2}, context={self.context_2}]"

    def test_rewrapping_step_action_throws_attribute_error_when_allow_re_wrapping_is_false(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        action = StepAction(lambda item, context: None)
        wrapped_action = logging_wrapper.wrap(action)

        assert isinstance(wrapped_action, StepAction)

        with pytest.raises(AttributeError):
            logging_wrapper.wrap(wrapped_action)

    def test_rewrapping_queue_condition_throws_attribute_error_when_allow_re_wrapping_is_false(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        should_stop = bool_generator()
        condition = QueueCondition(lambda nitem, nctx, item, ctx: next(should_stop))

        wrapped_condition = logging_wrapper.wrap(condition)

        assert isinstance(wrapped_condition, QueueCondition)

        with pytest.raises(AttributeError):
            logging_wrapper.wrap(wrapped_condition)

    def test_rewrapping_stop_condition_throws_attribute_error_when_allow_re_wrapping_is_false(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        condition = StopCondition(lambda item, context: True)
        wrapped_condition = logging_wrapper.wrap(condition)

        assert isinstance(wrapped_condition, StopCondition)

        with pytest.raises(AttributeError):
            logging_wrapper.wrap(wrapped_condition)

        # Ensure rewrapping conditions already wrapped by another logger requires explicit approval
        logging_wrapper2 = DebugLoggingWrapper('my desc', self.logger)
        with pytest.raises(AttributeError):
            logging_wrapper2.wrap(wrapped_condition)

    def test_adding_to_debug_logging_wrapper_increments_count_as_expected(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        condition = StopCondition(lambda item, context: True)
        wrapped_condition = logging_wrapper.wrap(condition)

        # Check count starts at 1, and double adding the same condition doesn't increment count
        with self._log_handler() as handler:
            wrapped_condition.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(1)=True [item=False, context=False]"

        condition2 = StopCondition(lambda item, context: True)
        wrapped_condition2 = logging_wrapper.wrap(condition2)

        with self._log_handler() as handler:
            # check the new condition is marked as "2"
            wrapped_condition2.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(2)=True [item=False, context=False]"

            # check the original condition hasnt changed from "1"
            wrapped_condition.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(1)=True [item=False, context=False]"

        # check that adding the original condition to a new logger works, and resets the count.
        logging_wrapper2 = DebugLoggingWrapper('my desc', self.logger)

        wrapped_original_condition = logging_wrapper2.wrap(condition)
        wrapped_original_condition2 = logging_wrapper2.wrap(condition2)

        with self._log_handler() as handler:
            wrapped_original_condition.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(1)=True [item=False, context=False]"

            # check the new condition is marked as "2"
            wrapped_original_condition2.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(2)=True [item=False, context=False]"
