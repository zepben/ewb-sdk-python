#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sys

from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

deps = [
    "requests<2.27.0,>=2.26.0",
    "zepben.protobuf==0.24.1",
    "zepben.auth==0.10.0",
    "dataclassy==0.6.2",
    "six==1.16.0"
]

# AsyncMock was not included in the base module until 3.8, so use the backport instead if required
v = sys.version_info
if v.major == 3 and v.minor < 8:
    deps.append("mock==4.0.3")

test_deps = [
    "pytest==7.1.2",
    "pytest-cov==2.10.1",
    "pytest-asyncio==0.19.0",
    "pytest-timeout==1.4.2",
    "hypothesis==6.56.3",
    "grpcio-testing==1.46.3",
    "pylint==2.14.5",
    "tox"
]

setup(
    name="zepben.evolve",
    version="0.36.0b1",
    description="Python SDK for interacting with the Evolve platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zepben/evolve-sdk-python",
    author="Kurt Greaves",
    author_email="kurt.greaves@zepben.com",
    license="MPL 2.0",
    classifiers=[
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    python_requires='>=3.7',
    install_requires=deps,
    extras_require={
        "test": test_deps,
    }
)
