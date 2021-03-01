#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

import inspect
from abc import ABCMeta, abstractmethod, ABC
from typing import List, Optional, Type, TypeVar, Dict

from dataclassy import dataclass

from zepben.evolve import Column


Any = TypeVar("Any")


@dataclass(slots=True)
class SqliteTable(object):

    _column_index: int = 0
    _column_set: Optional[List[Column]] = None
    _create_table_sql: Optional[str] = None
    _prepared_insert_sql: Optional[str] = None
    _prepared_update_sql: Optional[str] = None
    _create_indexes_sql: Optional[List[str]] = None
    _select_sql: Optional[str] = None

    @property
    @abstractmethod
    def table_class(self) -> Type[T]:
        pass

    @property
    @abstractmethod
    def table_class_instance(self) -> T:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    def unique_index_columns(self) -> List[List[Column]]:
        return []

    def non_unique_index_columns(self) -> List[List[Column]]:
        return []

    @property
    def column_set(self) -> List[Column]:
        return self._column_set if self._column_set else self._create_column_set(self.table_class, self.table_class_instance)

    @property
    def create_table_sql(self):
        return self._create_table_sql if self._create_table_sql else self._create_create_table_sql()

    @property
    def select_sql(self):
        return self._select_sql if self._select_sql else self._create_select_sql()

    @property
    def prepared_insert_sql(self):
        return self._prepared_insert_sql if self._prepared_insert_sql else self._create_prepared_insert_sql()

    @property
    def prepared_update_sql(self):
        return self._prepared_update_sql if self._prepared_update_sql else self._create_prepared_update_sql()

    def _create_column_set(self, clazz: Type[Any], instance: Any) -> Dict[Column, None]:
        cols = dict()
        repeated_field = False

        if clazz.__base__:
            cols.update(self._create_column_set(clazz.__base__, instance))

        attributes = inspect.getmembers(SqliteTable, lambda x: not inspect.isdatadescriptor(x) and not inspect.isroutine(x))
        declared_fields = [a for a in attributes if not a[0].startswith('_')]
        for field in declared_fields:
            pass

    def _create_create_table_sql(self):
        pass

    def _create_select_sql(self):
        pass

    def _create_prepared_insert_sql(self):
        pass

    def _create_prepared_update_sql(self):
        pass



T = TypeVar("T", bound=SqliteTable)
