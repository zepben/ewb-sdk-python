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
from collections import OrderedDict


def create_registrar():
    registry = {}

    def registrar(func):
        registry[func.__name__] = func
        return func
    registrar.all = registry
    return registrar


def map_type():
    # Maps types to the decorated function. The ordering here is important, as we use this ordering when we
    # serialise or deserialise from an EquipmentContainer.
    type_map = OrderedDict()
    # Maps protobuf types to CIM types
    pb_to_cim = OrderedDict()
    # Maps protobuf types to the name of a gRPC streaming function.
    # For example, a Protobuf BaseVoltage maps to createBaseVoltage.
    # This is used when streaming an EquipmentContainer.
    grpc_func_map = dict()

    def wrap(typ, pb_typ=None, stream_func_name=None):
        def mapper(func):
            if pb_typ is None and stream_func_name is not None:
                raise Exception(f"A protobuf type must be provided for {typ} because stream_func_name is set. We can only stream types with protobuf mappings.")
            if typ in type_map:
                raise Exception(f"Type {typ} already has an associated map - ensure {typ} corresponds to only one map")
            if pb_typ in type_map:
                raise Exception(f"Protobuf Type {pb_typ} already has an associated map - ensure {typ} corresponds to only one map")
            type_map[typ] = func
            if pb_typ is not None:
                type_map[pb_typ] = func
                pb_to_cim[pb_typ] = typ
                if stream_func_name is not None:
                    grpc_func_map[pb_typ] = stream_func_name

            return func
        return mapper
    wrap.all = type_map
    wrap.pb_to_cim = pb_to_cim
    wrap.grpc = grpc_func_map
    return wrap
