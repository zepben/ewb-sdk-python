#!/usr/bin/env python3
#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Build script for the C-accelerated tracing extension.

The extension is optional: if gcc is not available or compilation fails,
the package still installs and falls back to the pure-Python implementation.
"""

import sysconfig
from pathlib import Path

from setuptools import Extension, setup, find_packages
TRACING_DIR = Path("src/zepben/ewb/services/network/tracing")
C_SOURCE = TRACING_DIR / "_tracing_c.c"
EXT_DIR = TRACING_DIR / "_tracing_c_ext"
EXT_NAME = "_tracing_c"

# Check if the C source exists
if C_SOURCE.exists():
    extension = Extension(
        name=f"zepben.ewb.services.network.tracing._tracing_c_ext.{EXT_NAME}",
        sources=[str(C_SOURCE)],
        extra_compile_args=["-std=c11", "-O2", "-Wall", "-Wno-unused-function"],
        define_macros=[("PY_SSIZE_T_CLEAN", None)],
        include_dirs=[sysconfig.get_path("include")],
    )
    ext_modules = [extension]
else:
    raise Exception("C source not found")

setup(
    name="zwpben.ewb",
    packages=find_packages(where="src"),
    ext_modules=ext_modules,
)
