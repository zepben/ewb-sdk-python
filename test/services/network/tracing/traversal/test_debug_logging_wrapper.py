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

    def _wrap(self, condition, count=None):
        return DebugLoggingWrapper('my desc', self.logger).wrap(condition, count)

    def test_wrapped_object_is_original_object(self):
        should_stop = bool_generator()

        stop_condition = StopCondition(lambda item, ctx: next(should_stop))
        wrapped = self._wrap(stop_condition, 100)
        assert wrapped is stop_condition
        assert isinstance(wrapped, StopCondition)
        assert not isinstance(wrapped, QueueCondition)
        assert not isinstance(wrapped, StepAction)

        queue_condition = QueueCondition(lambda nitem, nctx, item, ctx: next(should_stop))
        wrapped = self._wrap(queue_condition, 20)
        assert wrapped is queue_condition
        assert not isinstance(wrapped, StopCondition)
        assert isinstance(wrapped, QueueCondition)
        assert not isinstance(wrapped, StepAction)

        action = StepAction(lambda item, context: None)
        wrapped = self._wrap(action, 20)
        assert wrapped is action
        assert not isinstance(wrapped, StopCondition)
        assert not isinstance(wrapped, QueueCondition)
        assert isinstance(wrapped, StepAction)

    def test_can_wrap_stop_condition(self):
        should_stop = bool_generator()

        wrapped = self._wrap(StopCondition(lambda item, ctx: next(should_stop)), 100)

        with self._log_handler() as handler:
            assert wrapped.should_stop(self.item_1, self.context_1)
            assert not wrapped.should_stop(self.item_2, self.context_2)

            assert handler.log_list.get() == f"root: my desc: should_stop(100)=True [item={self.item_1}, context={self.context_1}]"
            assert handler.log_list.get() == f"root: my desc: should_stop(100)=False [item={self.item_2}, context={self.context_2}]"

    def test_can_wrap_queue_conditions(self):
        should_stop = bool_generator()

        condition = QueueCondition(lambda nitem, nctx, item, ctx: next(should_stop))
        condition.should_queue_start_item = lambda item: next(should_stop)
        self._wrap(condition, 50)

        with self._log_handler() as handler:
            assert condition.should_queue(self.item_1, self.context_1, self.item_2, self.context_2)
            assert not condition.should_queue(self.item_2, self.context_2, self.item_1, self.context_1)

            assert next(should_stop)  # we need to skip the `True` the generators returning next

            assert not condition.should_queue_start_item(self.item_1)
            assert condition.should_queue_start_item(self.item_2)

            assert handler.log_list.get() == (
                f"root: my desc: should_queue(50)=True ["
                f"next_item={self.item_1}, next_context={self.context_1}, current_item={self.item_2}, current_context={self.context_2}]"
            )
            assert handler.log_list.get() == (
                f"root: my desc: should_queue(50)=False ["
                f"next_item={self.item_2}, next_context={self.context_2}, current_item={self.item_1}, current_context={self.context_1}]"
            )
            assert handler.log_list.get() == f"root: my desc: should_queue_start_item(50)=False [item={self.item_1}]"
            assert handler.log_list.get() == f"root: my desc: should_queue_start_item(50)=True [item={self.item_2}]"

    def test_can_wrap_step_actions(self):
        action = self._wrap(StepAction(lambda item, context: None), 1)

        with self._log_handler() as handler:
            action.apply(self.item_1, self.context_1)
            action.apply(self.item_2, self.context_2)

            assert handler.log_list.get() == f"root: my desc: apply(1) [item={self.item_1}, context={self.context_1}]"
            assert handler.log_list.get() == f"root: my desc: apply(1) [item={self.item_2}, context={self.context_2}]"

    def test_rewrapping_step_action_throws_attribute_error_when_allow_re_wrapping_is_false(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        action = StepAction(lambda item, context: None)
        logging_wrapper.wrap(action)

        assert isinstance(action, StepAction)
        assert action in logging_wrapper._wrapped[StepAction]

        with pytest.raises(AttributeError):
            logging_wrapper.wrap(action)

    def test_rewrapping_step_action_works_when_allow_re_wrapping_is_true(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        action = StepAction(lambda item, context: None)
        logging_wrapper.wrap(action)
        assert len(logging_wrapper._wrapped[StepAction]) == 1

        assert isinstance(action, StepAction)
        assert action in logging_wrapper._wrapped[StepAction]

        logging_wrapper.wrap(action, allow_re_wrapping=True)

        # Make sure we didn't double add it.
        assert len(logging_wrapper._wrapped[StepAction]) == 1

    def test_rewrapping_queue_condition_throws_attribute_error_when_allow_re_wrapping_is_false(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        should_stop = bool_generator()
        condition = QueueCondition(lambda nitem, nctx, item, ctx: next(should_stop))

        logging_wrapper.wrap(condition)

        assert isinstance(condition, QueueCondition)
        assert condition in logging_wrapper._wrapped[QueueCondition]

        with pytest.raises(AttributeError):
            logging_wrapper.wrap(condition)

    def test_rewrapping_queue_condition_works_when_allow_re_wrapping_is_true(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        should_stop = bool_generator()
        condition = QueueCondition(lambda nitem, nctx, item, ctx: next(should_stop))

        assert condition.should_queue(False, False, False, False)

        logging_wrapper.wrap(condition)

        assert not condition.should_queue(False, False, False, False)
        assert len(logging_wrapper._wrapped[QueueCondition]) == 1
        assert isinstance(condition, QueueCondition)
        assert condition in logging_wrapper._wrapped[QueueCondition]

        logging_wrapper.wrap(condition, allow_re_wrapping=True)

        assert condition.should_queue(False, False, False, False)

        # Make sure we didn't double add it.
        assert len(logging_wrapper._wrapped[QueueCondition]) == 1

    def test_rewrapping_stop_condition_throws_attribute_error_when_allow_re_wrapping_is_false(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        condition = StopCondition(lambda item, context: True)
        logging_wrapper.wrap(condition)

        assert isinstance(condition, StopCondition)
        assert condition in logging_wrapper._wrapped[StopCondition]

        with pytest.raises(AttributeError):
            logging_wrapper.wrap(condition)

        # ensure rewrapping conditions already wrapped by another logger requires explicit approval
        logging_wrapper2 = DebugLoggingWrapper('my desc', self.logger)
        with pytest.raises(AttributeError):
            logging_wrapper2.wrap(condition)

    def test_rewrapping_stop_condition_works_when_allow_re_wrapping_is_true(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        condition = StopCondition(lambda item, context: True)
        logging_wrapper.wrap(condition)
        assert len(logging_wrapper._wrapped[StopCondition]) == 1

        assert isinstance(condition, StopCondition)
        assert condition in logging_wrapper._wrapped[StopCondition]

        logging_wrapper.wrap(condition, allow_re_wrapping=True)

        # Make sure we didn't double add it.
        assert len(logging_wrapper._wrapped[StopCondition]) == 1

        # ensure rewrapping conditions already wrapped by another logger works when specified
        logging_wrapper2 = DebugLoggingWrapper('my desc', self.logger)
        logging_wrapper2.wrap(condition, allow_re_wrapping=True)

    def test_adding_to_debug_logging_wrapper_increments_count_as_expected(self):
        logging_wrapper = DebugLoggingWrapper('my desc', self.logger)

        condition = StopCondition(lambda item, context: True)
        logging_wrapper.wrap(condition)

        # check count starts at 1, and double adding the same condition doesnt increment count
        with self._log_handler() as handler:
            condition.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(1)=True [item=False, context=False]"

            logging_wrapper.wrap(condition, allow_re_wrapping=True)
            condition.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(1)=True [item=False, context=False]"

        condition2 = StopCondition(lambda item, context: True)
        logging_wrapper.wrap(condition2)

        with self._log_handler() as handler:
            # check the new condition is marked as "2"
            condition2.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(2)=True [item=False, context=False]"

            # check the original condition hasnt changed from "1"
            condition.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(1)=True [item=False, context=False]"

        # check that addind the already wrapped conditions to a new logger resets the count.
        logging_wrapper2 = DebugLoggingWrapper('my desc', self.logger)

        logging_wrapper2.wrap(condition, allow_re_wrapping=True)
        logging_wrapper2.wrap(condition2, allow_re_wrapping=True)

        with self._log_handler() as handler:
            condition.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(1)=True [item=False, context=False]"

            # check the new condition is marked as "2"
            condition2.should_stop(False, False)
            assert handler.log_list.get() == f"root: my desc: should_stop(2)=True [item=False, context=False]"
