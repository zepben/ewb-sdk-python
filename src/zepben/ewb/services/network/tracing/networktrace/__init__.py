#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['NetworkTrace', 'is_c_extension_available', 'use_c_extension']

# Use C-accelerated NetworkTrace if available, otherwise fall back to Python
try:
    from zepben.ewb.services.network.tracing._network_trace_c import (
        NetworkTraceC as NetworkTrace,
        is_c_extension_available,
        use_c_extension,
    )
except ImportError:
    from zepben.ewb.services.network.tracing.networktrace.network_trace import (
        NetworkTrace,
    )

    def is_c_extension_available() -> bool:
        return False

    def use_c_extension(enabled=None):
        return False
