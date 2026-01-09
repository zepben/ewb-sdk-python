#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import importlib
import pkgutil
from concurrent import futures

import grpc
from hypothesis.strategies import uuids


def all_subclasses(cls, package):
    """
    Get all concrete subclasses of a given class that are defined under `package`
    :param cls: The class to check
    :param package: The package to find classes under
    :return: A set of all concrete implementations of `cls` under `package`
    """
    y = set()

    def find_subclasses(recurse_cls):
        for c in recurse_cls.__subclasses__():
            # The abstract check doesn't work the same in python, so we add all items and remove the ones that are parent classes below.
            # Checking for ABC in bases works if all classes are marked with ABC, but this is not compatible with using dataclassy.
            if c.__module__.startswith(package):
                y.add(c)
            find_subclasses(c)

    find_subclasses(cls)

    # The abstract check doesn't work the same in python, so remove all parent classes we added above.
    supers = {it.__mro__[1] for it in y}
    return {it for it in y if it not in supers}


def import_submodules(package: str, recursive=True):
    """ Import all submodules of a module, optionally recursively, including subpackages

    `package` package (name or actual module)
    `recursive` Whether to recursively import modules
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = f"{package.__name__}.{module_name}"
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def grpc_aio_server():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=1))
    host = 'localhost:50053'
    server.add_insecure_port(host)

    return server, host


mrid_strategy = uuids(version=4).map(lambda x: str(x))
