#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
from abc import ABCMeta
from collections import OrderedDict
from dataclassy import dataclass
from typing import Dict, Generator, Callable, Optional, List, Set
from itertools import chain
from zepben.cimbend.common.reference_resolvers import BoundReferenceResolver, UnresolvedReference

__all__ = ["BaseService"]

_GET_DEFAULT = (1,)


@dataclass(slots=True)
class BaseService(object, metaclass=ABCMeta):
    name: str
    _objectsByType: Dict[type, Dict[str, IdentifiedObject]] = OrderedDict()
    _unresolved_references: Dict[str, List[UnresolvedReference]] = OrderedDict()

    def __contains__(self, mrid: str) -> bool:
        """
        Check if `mrid` has any associated object.

        `mrid` The mRID to search for.
        Returns True if there is an object associated with the specified `mrid`, False otherwise.
        """
        for type_map in self._objectsByType.values():
            if mrid in type_map:
                return True
        return False

    def __str__(self):
        return f"{type.__name__}{f' {self.name}' if self.name else ''}"

    def has_unresolved_references(self):
        """
        Returns True if this service has unresolved references, False otherwise.
        """
        return len(self._unresolved_references) > 0

    def len_of(self, t: type = None) -> int:
        """
        Get the len of objects of type `t` in the service.
        `t` The type of object to get the len of. If None (default), will get the len of all objects in the service.
        """
        if t is None:
            return sum([len(vals) for vals in self._objectsByType.values()])
        else:
            return len(self._objectsByType[t].values())

    def num_unresolved_references(self):
        """
        Get the total number of unresolved references.
        Note that this is not terribly cheap call, and should be used sparingly. To test if unresolved references exist,
        use `has_unresolved_references()` instead.
        Returns The number of references in the network that have not already been resolved.
        """
        return len({r.to_mrid for reflist in self._unresolved_references.values() for r in reflist})

    def unresolved_references(self):
        for from_mrid, unresolved_refs in self._unresolved_references.copy().items():
            yield from_mrid, unresolved_refs

    def unresolved_mrids(self):
        refs = {r.to_mrid for reflist in self._unresolved_references.values() for r in reflist}
        for ref in refs:
            yield ref

    def get(self, mrid: str, type_: type = None, default=_GET_DEFAULT,
            generate_error: Callable[[str, str], str] = lambda mrid, typ: f"Failed to find {typ}[{mrid}]") -> IdentifiedObject:
        """
        Get an object associated with this service.

        `mrid` The mRID of the `iec61970.base.core.identified_object.IdentifiedObject` to retrieve.
        `type_` The `iec61970.base.core.identified_object.IdentifiedObject` subclass type of the object
                      with `mrid`. If None, will check all types stored in the service.
        `default` The default to return if `mrid` can't be found in the service.
        `generate_error` Function to call for an error message. Will be passed the mrid and _type (if set).
        Returns The `iec61970.base.core.identified_object.IdentifiedObject` associated with `mrid`, or default
                 if it is set.
        Raises `KeyError` if `mrid` was not found in the service with `_type` or if no objects of `_type` are
                 stored by the service and default was not set.
        """
        if not mrid:
            raise KeyError("You must specify an mRID to get. Empty/None is invalid.")

        if type_:
            try:
                return self._objectsByType[type_][mrid]
            except KeyError:
                for c, obj_map in self._objectsByType.items():
                    if issubclass(c, type_):
                        try:
                            return obj_map[mrid]
                        except KeyError:
                            pass
                if default is _GET_DEFAULT:
                    raise KeyError(generate_error(mrid, type_.__name__))
                else:
                    return default
        else:
            for object_map in self._objectsByType.values():
                if mrid in object_map:
                    return object_map[mrid]

            if default is _GET_DEFAULT:
                raise KeyError(generate_error(mrid, ""))
            return default

    def __getitem__(self, mrid):
        """
        Get an object associated with this service.
        Note that you should use `get` directly where the type of the desired object is known.
        `mrid` The mRID of the `iec61970.base.core.identified_object.IdentifiedObject` to retrieve.
        Returns The `iec61970.base.core.identified_object.IdentifiedObject` associated with `mrid`.
        Raises `KeyError` if `mrid` was not found in the service with `type`.
        """
        return self.get(mrid)

    def ensure_get(self, mrid: Optional[str], type_: type,
                   generate_error: Callable[[str, str], str] = lambda mrid, typ: f"Failed to find {typ}[{mrid}]"):
        return None if not mrid else self.get(mrid, type_, generate_error=generate_error)

    def add(self, identified_object: IdentifiedObject) -> bool:
        """
        Associate an object with this service.
        `identified_object` The object to associate with this service.
        Returns True if the object is associated with this service, False otherwise.
        """
        objs = self._objectsByType.get(identified_object.__class__, dict())
        if identified_object.mrid in objs:
            return False

        # Check other types and make sure this mRID is unique
        for obj_map in self._objectsByType.values():
            if identified_object.mrid in obj_map:
                return False

        unresolved_refs = self._unresolved_references.get(identified_object.mrid, None)
        if unresolved_refs:
            for ref in unresolved_refs:
                ref.resolver.resolve(ref.from_ref, identified_object)
            del self._unresolved_references[identified_object.mrid]

        objs[identified_object.mrid] = identified_object
        self._objectsByType[identified_object.__class__] = objs
        return True

    def resolve_or_defer_reference(self, bound_resolver: BoundReferenceResolver, to_mrid: str) -> bool:
        """
        Resolves a property reference between two types by looking up the `to_mrid` in the service and
        using the provided `bound_resolver` to resolve the reference relationships (including any reverse relationship).

        If the `to_mrid` object has not yet been added to the service, the reference resolution will be deferred until the
        object with `to_mrid` is added to the service, which will then use the resolver from the `bound_resolver` at that
        time to resolve the reference relationship.


        `bound_resolver`
        `to_mrid` The MRID of an object that is the subclass of the to_class of `bound_resolver`.
        Returns true if the reference was resolved, otherwise false if it has been deferred.
        """
        if not to_mrid:
            return True

        from_ = bound_resolver.from_obj
        resolver = bound_resolver.resolver
        reverse_resolver = bound_resolver.reverse_resolver
        try:
            to = self.get(to_mrid, resolver.to_class)
            resolver.resolve(from_, to)
            if reverse_resolver:
                reverse_resolver.resolve(to, from_)

                # Clean up any reverse unresolved references now that the reference has been resolved
                if from_.mrid in self._unresolved_references:
                    refs = self._unresolved_references[from_.mrid]
                    #
                    self._unresolved_references[from_.mrid] = [ref for ref in refs if
                                                               not ref.to_mrid == from_.mrid and not ref.resolver == reverse_resolver]

                    if not self._unresolved_references[from_.mrid]:
                        del self._unresolved_references[from_.mrid]
            return True
        except KeyError:
            urefs = self._unresolved_references.get(to_mrid, list())
            urefs.append(UnresolvedReference(from_ref=from_, to_mrid=to_mrid, resolver=resolver))
            #
            self._unresolved_references[to_mrid] = urefs
            return False

    def get_unresolved_reference_mrids(self, bound_resolver: BoundReferenceResolver) -> Set[str]:
        """
        Gets a set of MRIDs that are referenced by the from_obj held by `bound_resolver` that are unresolved.
        `bound_resolver` The `BoundReferenceResolver` to retrieve unresolved references for.
        Returns Set of mRIDs that have unresolved references.
        """
        return set(chain(*[[ref.to_mrid for ref in refs if ref.from_ref == bound_resolver.from_obj and ref.resolver == bound_resolver.resolver] for
                           refs in self._unresolved_references.values()]))

    def remove(self, identified_object: IdentifiedObject) -> bool:
        """
        Disassociate an object from this service.

        `identified_object` THe object to disassociate from the service.
        Raises `KeyError` if `identified_object` or its type was not present in the service.
        """
        del self._objectsByType[identified_object.__class__][identified_object.mrid]
        return True

    def objects(self, obj_type: Optional[type] = None, exc_types: Optional[List[type]] = None) -> Generator[ IdentifiedObject, None, None]:
        """
        Generator for the objects in this service of type `obj_type`.
        `obj_type` The type of object to yield. If this is a base class it will yield all subclasses.
        Returns Generator over
        """
        if obj_type is None:
            for typ, obj_map in self._objectsByType.items():
                if exc_types:
                    if typ in exc_types:
                        continue
                for obj in obj_map.values():
                    yield obj
            return
        else:
            try:
                for obj in self._objectsByType[obj_type].values():
                    yield obj
            except KeyError:
                for _type, object_map in self._objectsByType.items():
                    if issubclass(_type, obj_type):
                        for obj in object_map.values():
                            yield obj
