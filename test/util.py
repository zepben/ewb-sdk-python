#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import importlib
import pkgutil
from concurrent import futures
from typing import Generator, TypeVar, Callable, Any, Optional

import grpc
from hypothesis.strategies import uuids

T = TypeVar("T")


def all_subclasses(cls, package):
    """
    Get all concrete subclasses of a given class that are defined under `package`
    :param cls: The class to check
    :param package: The package to find classes under
    :return: A set of all concrete implementations of `cls` under `package`
    """
    y = {}

    def add_by_name(c: type):
        y[c.__name__] = c

    def find_subclasses(recurse_cls):

        found = False
        children = {}
        for c in recurse_cls.__subclasses__():
            name = c.__name__
            if name in children:
                if len(children[name].__subclasses__()) < len(c.__subclasses__()):
                    children[name] = c
            else:
                children[name] = c

        for c in children.values():
            # Metaclasses don't properly work for abstraction denotion (need abstract methods)
            # So we can use inheritance checks instead
            rec = find_subclasses(c)
            found = rec or found
        if not found and recurse_cls.__module__.startswith(package):
            add_by_name(recurse_cls)
            return True

        return found

    find_subclasses(cls)

    return set(y.values())


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


def assert_or_empty(
    gen: Generator[T, None, None],
    arg: list[T] | None,
    sorted_by: Optional[Callable[[T], Any]] = None,
    sort_reversed: bool = False,
) -> list[T] | None:
    actual = list(gen)
    expected = arg or []
    if sorted_by:
        expected.sort(key=sorted_by, reverse=sort_reversed)

    assert actual == expected

mrid_strategy = uuids(version=4).map(lambda x: str(x))
