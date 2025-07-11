#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from _pytest.python_api import raises

from zepben.ewb import StepAction, StepContext
from zepben.ewb.services.network.tracing.traversal.step_action import T


class TestStepAction:

    def test_can_apply_lambda(self):
        """Make sure we can use a lambda as the StepAction"""
        captured = []
        step_action = StepAction(lambda it, ctx: captured.append((it, ctx)))

        expected_item = 1
        expected_ctx = StepContext(is_start_item=True, is_branch_start_item=False)

        step_action.apply(expected_item, expected_ctx)

        assert captured == [(expected_item, expected_ctx)]

    def test_cant_override_apply(self):
        """This is testing that if you ignore the @final on apply, you will get an exception."""
        with raises(Exception, match="method 'apply' should not be directly overridden, override '_apply' instead."):
            class MyStepAction(StepAction):

                # noinspection PyFinal
                def apply(self, item: T, context: StepContext):
                    pass

    def test_can_apply_descendant(self):
        """Simulate someone doing what the exception told you to do"""
        captured = []

        class MyStepAction(StepAction):

            def _apply(self, item: T, context: StepContext):
                captured.append((item, context))

        step_action = MyStepAction()

        expected_item = 1
        expected_ctx = StepContext(is_start_item=True, is_branch_start_item=False)

        step_action.apply(expected_item, expected_ctx)

        assert captured == [(expected_item, expected_ctx)]
