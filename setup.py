"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from setuptools import setup, find_namespace_packages

test_deps = ["pytest", "pytest-asyncio"]
setup(
    name="zepben.cimbend",
    version="0.2.0b1",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "protobuf",
        "requests",
        "zepben.protobuf",
        "python-jose-cryptodome",
    ],
    extras_require={
        "test": test_deps,
    }
)
