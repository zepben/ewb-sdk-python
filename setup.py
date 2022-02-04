#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

test_deps = ["pytest", "pytest-cov", "pytest-asyncio", "pytest-timeout", "hypothesis<6", "grpcio-testing==1.36.0"]
setup(
    name="zepben.evolve",
    version="0.27.0b12",
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
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    python_requires='>=3.7',
    install_requires=[
        "requests<2.27.0,>=2.26.0",
        "zepben.protobuf==0.19.0b6",
        "zepben.auth==0.7.0b2",
        "dataclassy==0.6.2",
        "grpcio==1.41.1"
    ],
    extras_require={
        "test": test_deps,
    }
)
