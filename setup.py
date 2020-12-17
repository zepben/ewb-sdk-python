#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

test_deps = ["pytest", "pytest-asyncio", "hypothesis<6"]
setup(
    name="zepben.evolve",
    version="0.21.0",
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
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    python_requires='>=3.7',
    install_requires=[
        "protobuf",
        "requests",
        "zepben.protobuf==0.9.0",
        "python-jose-cryptodome",
        "dataclassy"
    ],
    extras_require={
        "test": test_deps,
    }
)
