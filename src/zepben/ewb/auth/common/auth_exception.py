#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["AuthException"]


class AuthException(Exception):

    status_code: int

    def __init__(self, status_code: int, *args):
        super().__init__(*args)
        self.status_code = status_code
