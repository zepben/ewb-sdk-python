#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Dict, List, Generator, overload, TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

from zepben.evolve.dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.core.name import Name

__all__ = ["NameType"]


@dataclass(slots=True)
class NameType:
    """
    Type of name. Possible values for attribute 'name' are implementation dependent but standard profiles may specify types. An enterprise may have multiple
    IT systems each having its own local name for the same object, e.g. a planning system may have different names from an EMS. An object may also have
    different names within the same IT system, e.g. localName as defined in CIM version 14. The definition from CIM14 is:
    The localName is a human-readable name of the object. It is a free text name local to a node in a naming hierarchy similar to a file directory structure.
    A power system related naming hierarchy may be: Substation, VoltageLevel, Equipment etc. Children of the same parent in such a hierarchy have names that
    typically are unique among them.
    """

    name: str
    """Name of the name type."""

    description: str = ""
    """Description of the name type."""

    _names_index: Dict[str, Name] = dict()
    _names_multi_index: Dict[str, List[Name]] = dict()

    def __str__(self):
        return f"NameType(name='{self.name}', description='{self.description}')"

    @property
    def names(self) -> Generator[Name, None, None]:
        """All names of this type."""
        for names_ in self._names_multi_index.values():
            for name in names_:
                yield name

        for name_ in self._names_index.values():
            yield name_

    @overload
    def has_name(self, name: str):
        """Indicates if this :class:`NameType` contains `Name` with `name`."""

    @overload
    def has_name(self, name: Name):
        """Indicates if this :class:`NameType` contains specific `name`."""

    def has_name(self, name):
        if isinstance(name, str):
            return name in self._names_index or name in self._names_multi_index
        if isinstance(name, Name):
            return name in self._names_index.values() or name in self._names_multi_index.values()

    @overload
    def get_names(self, name: str) -> Generator[Name, None, None]:
        ...

    @overload
    def get_names(self, io) -> Generator[Name, None, None]:
        ...

    def get_names(self, name_or_io) -> Generator[Name, None, None]:
        """Get all the :class:`Name` instances for the provided `name` or `IdentifiedObject`.

        :return: A `Generator` of `Name`
        """
        if isinstance(name_or_io, str):
            try:
                yield self._names_index[name_or_io]
            except KeyError:
                try:
                    for name_ in self._names_multi_index[name_or_io]:
                        yield name_
                except KeyError:
                    pass
        else:
            try:
                for name_ in self._names_index.values():
                    if name_.identified_object == name_or_io:
                        yield name_
                for names in self._names_multi_index.values():
                    for name_ in names:
                        if name_.identified_object == name_or_io:
                            yield name_
            except KeyError:
                pass

    def get_or_add_name(self, name: str, identified_object: IdentifiedObject) -> Name:
        """
        Gets a :class:`Name` for the given `name` and `identifiedObject` combination or adds a new :class:`Name`
        to this :class:`NameType` with the combination and returns the new instance.
        """
        if name in self._names_index:
            existing = self._names_index[name]
            if existing.identified_object is identified_object:
                return existing

            def move_to_multi_index(name_obj: Name):
                self._names_multi_index[name] = [existing, name_obj]
                del self._names_index[name]

            return self._get_or_create_name(name, identified_object, move_to_multi_index)
        elif name in self._names_multi_index:
            for n in self._names_multi_index[name]:
                if n.identified_object is identified_object:
                    return n

            def expand_multi_index(name_obj: Name):
                self._names_multi_index[name].append(name_obj)

            return self._get_or_create_name(name, identified_object, expand_multi_index)
        else:
            def add_to_index(name_obj: Name):
                self._names_index[name] = name_obj

            return self._get_or_create_name(name, identified_object, add_to_index)

    def remove_name(self, name: Name) -> NameType:
        """
        Removes the `name` from this name type.
        Removes the `name` from associated `IdentifiedObject`

        :return: True if the name instance was successfully removed
        """
        if name.type is not self:
            raise ValueError(f"NameType.remove_name(name): {name} not in {self}")

        try:
            del self._names_index[name.name]
            if name.identified_object.get_name(name.type, name.name):
                name.identified_object.remove_name(name)
            return self
        except KeyError:
            try:
                names = self._names_multi_index[name.name]
                names.remove(name)
                if not names:
                    del self._names_multi_index[name.name]
                name.identified_object.remove_name(name)
                return self
            except KeyError:
                return self

    def remove_names(self, name: str) -> NameType:
        """
        Removes all :class:`Name` instances associated with name `name`.

        :return: True if a matching name was removed.
        """
        try:
            name_obj = self._names_index[name]
            del self._names_index[name]
            name_obj.identified_object.remove_name(name_obj)
            return self
        except KeyError:
            try:
                name_list = list(self._names_multi_index[name])
                del self._names_multi_index[name]
                for name_obj in name_list:
                    name_obj.identified_object.remove_name(name_obj)
                return self
            except KeyError:
                return self

    def clear_names(self) -> NameType:
        for name in list(self._names_index.values()):
            name.identified_object.remove_name(name)
        for names in list(self._names_multi_index.values()):
            for name in names:
                name.identified_object.remove_name(name)
        self._names_index = dict()
        self._names_multi_index = dict()
        return self

    def _get_or_create_name(self, name: str, identified_object: IdentifiedObject, update_index: Callable[[Name], None]) -> Name:
        #
        # NOTE: In Python, we can add names directly into the names collection of an object, so there is a chance that we just need to update the index rather
        # than create a new Name class
        #
        had_name = identified_object.has_name(self, name)
        if had_name:
            name_obj = identified_object.get_name(self, name)
        else:
            name_obj = Name(name, self, identified_object)

        update_index(name_obj)

        if not had_name:
            identified_object.add_name(self, name)

        return name_obj
