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


import glob
import pkg_resources
from os.path import basename
from os.path import splitext
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as build_py_orig


class BuildWithProto(build_py_orig):

    def run(self):
        self.build_proto()

    def build_proto(self):
        """This will build the pb2 files at pip install time"""
        import grpc_tools.protoc
        proto_include = pkg_resources.resource_filename('grpc_tools', '_proto')
        files = glob.glob("protos/**/*.proto", recursive=True)
        print(f"Compiling protos: {', '.join(files)}")

        result = grpc_tools.protoc.main([
            'grpc_tools.protoc',
            '-Iprotos',
            f'-I{proto_include}',
            '--python_out=src/',
            '--grpc_python_out=src/',
            *files
        ])

        if result:
            raise Exception(f'protoc failed with {result}')


test_deps = ["pytest"]
setup(
    name="cimbend",
    version="0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob.glob('src/*.py')],
    install_requires=[
        "grpcio",
        "grpcio-tools",
        "protobuf"
    ],
    extras_require={
        "test": test_deps,
    },
    cmdclass={
        'build_ext': BuildWithProto
    }
)
