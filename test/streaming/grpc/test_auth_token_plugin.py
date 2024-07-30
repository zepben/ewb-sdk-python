#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import Mock

from zepben.evolve import AuthTokenPlugin


def test_auth_token_plugin():
    token_fetcher = Mock()
    token_fetcher.fetch_token = Mock(return_value="fake token")
    callback = Mock()

    plugin = AuthTokenPlugin(token_fetcher)
    plugin(Mock(), callback)

    callback.assert_called_once_with((("authorization", "fake token"),), None)
