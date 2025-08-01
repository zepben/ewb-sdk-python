#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

deps = [
    "zepben-protobuf==1.0.0b1",
    "typing_extensions==4.12.2",
    "requests>=2.26.0, <3.0.0",
    "urllib3>=1.26.6, <1.27.0",
    "PyJWT>=2.1.0, <2.2.0",
    "dataclassy==0.6.2",
]

test_deps = [
    "pytest==7.1.2",
    "pytest-cov==2.10.1",
    "pytest-asyncio==0.19.0",
    "pytest-timeout==1.4.2",
    'pytest-subtests',
    "hypothesis==6.56.3",
    "grpcio-testing==1.61.3",
    "pylint==2.14.5",
    "six==1.16.0",
    "tox"
]

setup(
    name="zepben.ewb",
    version="1.0.0b3",
    description="Python SDK for interacting with the Energy Workbench platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zepben/evolve-sdk-python",
    author="Kurt Greaves",
    author_email="kurt.greaves@zepben.com",
    license="MPL 2.0",
    classifiers=[
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    python_requires='>=3.9,<3.13',
    install_requires=deps,
    extras_require={
        "test": test_deps,
    }
)
