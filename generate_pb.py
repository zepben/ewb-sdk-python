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


import grpc_tools.protoc
import pkg_resources
import glob
import sys

if len(sys.argv) > 1:
    include = {arg for arg in sys.argv[1:]}
else:
    include = None


proto_include = pkg_resources.resource_filename('grpc_tools', '_proto')
files = glob.glob("protos/**/*.proto", recursive=True)
if include is not None:
    files_filtered = {f for f in files if f in include}
else:
    files_filtered = files

print(f"Compiling protos: {', '.join(files_filtered)}")
result = grpc_tools.protoc.main([
    'grpc_tools.protoc',
    '-Iprotos',
    f'-I{proto_include}',
    '--python_out=src/',
    '--grpc_python_out=src/',
    *files_filtered
])
