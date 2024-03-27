#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import importlib
import importlib.util
import importlib.util
import pkgutil

import pytest
from pytest import raises

from zepben.evolve.database.sqlite.tables.database_tables import DatabaseTables
from zepben.evolve.database.sqlite.tables.exceptions import MissingTableConfigException
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


def isabstract(object):
    for name, value in object.__dict__.items():
        if getattr(value, "__isabstractmethod__", False):
            return True
    for base in object.__bases__:
        for name in getattr(base, "__abstractmethods__", ()):
            value = getattr(object, name, None)
            if getattr(value, "__isabstractmethod__", False):
                return True
    return False


def all_subclasses(cls, package):
    """
    Get all concrete subclasses of a given class that are defined under `package`
    :param cls: The class to check
    :param package: The package to find classes under
    :return: A set of all concrete implementations of `cls` under `package`
    """
    y = set()
    for c in cls.__subclasses__():
        if not isabstract(c) and c.__module__.startswith(package):
            y.add(c)
        y.update(all_subclasses(c, package))
    return y


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

def test_has_all_tables():
    """
    This test detects if a Table class has been added under zepben.evolve.database.sqlite.tables however hasn't been added to
    DatabaseTables
    """
    res = import_submodules('zepben.evolve.database.sqlite.tables')
    subclasses = all_subclasses(SqliteTable, 'zepben.evolve.database.sqlite.tables')
    tables = DatabaseTables()
    for clazz in subclasses:
        tables.get_table(clazz)
    assert len(subclasses) == len([t for t in tables.tables]), "More concrete subclasses were found than exist in DatabaseTables."


def test_database_tables():
    class NotATable(SqliteTable):
        pass

    d = DatabaseTables()
    assert len(list(d.tables)) > 0
    for t in d.tables:
        assert t == d.get_table(type(t))
        insert = d.get_insert(type(t))
        assert insert.statement == t.prepared_insert_sql()
        assert insert.num_columns == t.prepared_insert_sql().count('?')

    with raises(MissingTableConfigException):
        d.get_table(NotATable)

    with raises(MissingTableConfigException):
        d.get_insert(NotATable)

