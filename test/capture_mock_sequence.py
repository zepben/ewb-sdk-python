#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import Mock


class CaptureMockSequence:

    def __init__(self, **kwargs):
        super().__init__()

        self.sequence = Mock()

        for key, mock in kwargs.items():
            self.sequence.attach_mock(mock, key)

    def verify_sequence(self, expected_calls):
        assert self.sequence.mock_calls == expected_calls, "mismatch in actual vs expected calls"
