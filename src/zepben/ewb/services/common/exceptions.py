#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

__all__ = ["UnsupportedIdentifiableException", "IllegalStateException"]


class UnsupportedIdentifiableException(Exception):
    """
    Raised when a service is asked to add or remove an `Identifiable` type that it does not support.
    """


class IllegalStateException(Exception):
    """
    Mirrors Kotlin's `IllegalStateException` for cases where an object is in an unexpected state.
    """
