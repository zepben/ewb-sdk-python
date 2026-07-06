#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import importlib
import pkgutil
import sys
from concurrent import futures
from typing import Generator, TypeVar, Callable, Any, Optional

import grpc
from hypothesis.strategies import uuids

T = TypeVar("T")

def _is_stale_class(cls: type) -> bool:
    """
    Dataclasses create stale class objects that mess with the inheritance tree.
    We check that the class has not been re-assigned in its own containing module

    Example::

        @dataclass(slots=True)
        class Dummy:
            ...

    This creates two classes ``Dummy`` - with and without slots. This function
    will return False for the one with slots, since that is the one that
    the module now recognises as the true Dummy.
    """
    module = sys.modules.get(cls.__module__)
    if module is None:
        return True
    current = getattr(module, cls.__name__, None)
    return cls is not current


def all_subclasses(cls, package) -> set[type]:
    """
    Get all concrete subclasses of a given class that are defined under `package`
    Account for stale classes created with ``@dataclass`` decorator

    NOTE: This method does not recognise nested classes as subclasses
    :param cls: The class to check
    :param package: The package to find classes under
    :return: A set of all concrete implementations of `cls` under `package`
    """
    leaves = set()

    def find_subclasses(recurse_cls):
        children = list(recurse_cls.__subclasses__())
        # Filter out subclasses that are outside the target package
        children = [c for c in children if c.__module__.startswith(package)]
        # Filter out subclasses that are stale references
        children = [c for c in children if not _is_stale_class(c)]

        # If no children exist, this is a leaf node
        if not children:
            leaves.add(recurse_cls)

        # Recursively look for leaves in children
        for c in children:
            find_subclasses(c)

    find_subclasses(cls)

    return leaves


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
