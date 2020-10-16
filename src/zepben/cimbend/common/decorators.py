
#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections import OrderedDict


def create_registrar():
    registry = {}

    def registrar(func):
        registry[func.__name__] = func
        return func
    registrar.all = registry
    return registrar


    # # A decorator simply used for registering Network getter functions.
    # # If you create a new equipment map in __init__, you should create a corresponding getter function and
    # # decorate it with @getter
    # getter: ClassVar = create_registrar()
    #
    # # A decorator used to specify which types are stored in each map. For every map there should be a
    # # corresponding `@property` declaration that is decorated with `type_map(class, [pb_class, gRPC_create_func])`,
    # # where `class` indicates the CIM type stored in that map, `pb_class` optionally indicates `class`'s corresponding
    # # Protobuf class, and `gRPC_create_func` indicates `pb_class`'s corresponding gRPC function for streaming.
    # # Utilised in the `add` method, but also in the streaming library.
    # type_map: ClassVar = map_type()
def map_type():
    # Maps types to the decorated function. The ordering here is important, as we use this ordering when we
    # serialise or deserialise from an Network.
    type_map = OrderedDict()
    types = []
    # Maps protobuf types to CIM types
    pb_to_cim = OrderedDict()
    # Maps protobuf types to the name of a gRPC streaming function.
    # For example, a Protobuf BaseVoltage maps to createBaseVoltage.
    # This is used when streaming an Network.
    grpc_func_map = dict()

    def wrap(typ, weight: int, pb_typ=None, stream_func_name=None):
        def mapper(func):
            if pb_typ is None and stream_func_name is not None:
                raise Exception(f"A protobuf type must be provided for {typ} because stream_func_name is set. We can only stream types with protobuf mappings.")
            if typ in type_map:
                raise Exception(f"Type {typ} already has an associated map - ensure {typ} corresponds to only one map")
            if pb_typ in type_map:
                raise Exception(f"Protobuf Type {pb_typ} already has an associated map - ensure {typ} corresponds to only one map")
            types.append((typ, weight))
            type_map[typ] = func
            if pb_typ is not None:
                type_map[pb_typ] = func
                pb_to_cim[pb_typ] = typ
                if stream_func_name is not None:
                    grpc_func_map[pb_typ] = stream_func_name

            return func
        return mapper
    wrap.types = sorted(types, key=lambda t: t[1])
    wrap.all = type_map
    wrap.pb_to_cim = pb_to_cim
    wrap.grpc = grpc_func_map
    return wrap
