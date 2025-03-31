#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import Mock

import pytest


class CaptureMockSequence:

    def __init__(self, **kwargs):
        super().__init__()

        self.sequence = Mock()

        for key, mock in kwargs.items():
            self.sequence.attach_mock(mock, key)

    def verify_sequence(self, expected_calls):
        mock_calls = list(self.sequence.mock_calls)

        mock_call_len = len(mock_calls)
        if mock_call_len != len(expected_calls):
            print(f'call sequence lengths not the same\n\n +++++++++++ \n\n')
            if mock_call_len > len(expected_calls):
                enum_list = mock_calls
                cmp_list = expected_calls
            else:
                enum_list = expected_calls
                cmp_list = mock_calls
        else:
            enum_list = mock_calls
            cmp_list = expected_calls

        for i, call in enumerate(enum_list):
            if i < len(cmp_list):
                print(f'{call} => {cmp_list[i]}')
            else:
                print(f'{call}')
        assert mock_calls == expected_calls, "mismatch in actual vs expected calls"
