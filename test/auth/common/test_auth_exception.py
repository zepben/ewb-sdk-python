#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb.auth import AuthException


def test_auth_exception():
    auth_exception = AuthException(404, "Not Found")
    assert auth_exception.status_code == 404
    assert auth_exception.args == ("Not Found",)
