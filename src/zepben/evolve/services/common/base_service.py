#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from abc import ABCMeta
from collections import OrderedDict
from typing import Dict, Generator, Callable, Optional, List, Union, Sized, Set
from typing import TypeVar, Type

from dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.services.common.reference_resolvers import BoundReferenceResolver, UnresolvedReference

__all__ = ["BaseService"]

T = TypeVar("T", bound=IdentifiedObject)

_GET_DEFAULT = (1,)


@dataclass(slots=True)
class BaseService(object, metaclass=ABCMeta):
    name: str
    _objects_by_type: Dict[type, Dict[str, IdentifiedObject]] = OrderedDict()
    _name_types: Dict[str, NameType] = dict()
    _unresolved_references_to: Dict[str, Set[UnresolvedReference]] = OrderedDict()
    """
    A dictionary of references between mRID's that as yet have not been resolved - typically when transferring services between systems.
    The key is the to_mrid of the `UnresolvedReference`s, and the value is a list of `UnresolvedReference`s for that specific object.
    For example, if an AcLineSegment with mRID 'acls1' is present in the service, but the service is missing its `location` with mRID 'location-l1' 
    and `perLengthSequenceImpedance` with mRID 'plsi-1', the following key value pairs would be present:
    {
        "plsi-1": [
            UnresolvedReference(from_ref=AcLineSegment('acls1'),
                                to_mrid='plsi-1',
                                 resolver=ReferenceResolver(from_class=AcLineSegment, to_class=PerLengthSequenceImpedance, resolve=...), ...)
        ],
        "location-l1": [
            UnresolvedReference(from_ref=AcLineSegment('acls1'),
                                to_mrid='location-l1',
                                resolver=ReferenceResolver(from_class=AcLineSegment, to_class=Location, resolve=...), ...)
        ]
    }
    
    `resolve` in `ReferenceResolver` will be the function used to populate the relationship between the `IdentifiedObject`s either when 
    `resolveOrDeferReference() is called if the other side of the reference exists in the service, or otherwise when the second object is added to the service.
    """

    _unresolved_references_from: Dict[str, Set[UnresolvedReference]] = OrderedDict()
    """ 
    An index of the unresolved references by their `from_ref.mrid`. For the above example this will be a dictionary of the form:
    {
        "acls1": [
            UnresolvedReference(from_ref=AcLineSegment('acls1'),
                                to_mrid='location-l1',
                                resolver=ReferenceResolver(from_class=AcLineSegment, to_class=Location, resolve=...), ...),
            UnresolvedReference(from_ref=AcLineSegment('acls1'),
                                to_mrid='plsi-1',
                                resolver=ReferenceResolver(from_class=AcLineSegment, to_class=PerLengthSequenceImpedance, resolve=...), ...)
        ]
    }
    """

    def __contains__(self, mrid: str) -> bool:
        """
        Check if `mrid` has any associated object.

        `mrid` The mRID to search for.
        Returns True if there is an object associated with the specified `mrid`, False otherwise.
        """
        for type_map in self._objects_by_type.values():
            if mrid in type_map:
                return True
        return False

    def __str__(self):
        return f"{self.__class__.__name__}{f' {self.name}' if self.name else ''}"

    def has_unresolved_references(self, mrid: str = None) -> bool:
        """
        Check if there are `UnresolvedReference`s in the service
                                                                                                                                 
        `mrid` The mRID to check for `UnresolvedReference`s. If None, will check if any unresolved references exist in the service.
                                                                                                                                 
        Returns True if at least one reference exists.
        """
        return len(self._unresolved_references_to) > 0 if mrid is None else mrid in self._unresolved_references_to

    def len_of(self, t: type = None) -> int:
        """
        Get the len of objects of type `t` in the service.
        `t` The type of object to get the len of. If None (default), will get the len of all objects in the service.
        """
        if t is None:
            return sum([len(vals) for vals in self._objects_by_type.values()])
        else:
            try:
                return len(self._objects_by_type[t].values())
            except KeyError:
                count = 0
                for c, obj_map in self._objects_by_type.items():
                    if issubclass(c, t):
                        try:
                            count += len(self._objects_by_type[c].values())
                        except KeyError:
                            pass
                return count

    def num_unresolved_references(self, mrid: str = None):
        """
        Get the total number of unresolved references in this service.
        `mRID` The mRID to check the number of [UnresolvedReference]s for. If None, will default to number of all unresolved references in the service.
        Returns The number of `UnresolvedReference`s.
        """
        if mrid is None:
            return sum([len(r) for r in self._unresolved_references_to.copy().values()])
        elif mrid in self._unresolved_references_to:
            return len(self._unresolved_references_to[mrid])
        else:
            return 0

    def unresolved_references(self) -> Generator[UnresolvedReference, None, None]:
        """
        Returns a generator over all the `UnresolvedReferences` that are known to this service. This should typically be avoided when resolving references in
        favour of `get_unresolved_reference_mrids_by_resolver()`, `get_unresolved_reference_mrids_from()`, and `get_unresolved_reference_mrids_to()`
        """
        for unresolved_refs in self._unresolved_references_to.copy().values():
            for ur in unresolved_refs:
                yield ur

    def get(self, mrid: str, type_: Type[T] = IdentifiedObject, default=_GET_DEFAULT,
            generate_error: Callable[[str, str], str] = lambda mrid, typ: f"Failed to find {typ}[{mrid}]") -> T:
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

        # This can be written much simpler than below but we want to avoid throwing any exceptions in this high frequency function
        if type_ != IdentifiedObject:
            objs = self._objects_by_type.get(type_)
            if objs:
                obj = objs.get(mrid)
                if obj:
                    return obj

        for c, objs in self._objects_by_type.items():
            obj = objs.get(mrid)
            if obj:
                if isinstance(obj, type_):
                    return obj
                else:
                    raise TypeError(f"Invalid type for {mrid}. Found {type(obj).__name__}, expected {type_.__name__}.")

        if default is _GET_DEFAULT:
            raise KeyError(generate_error(mrid, type_.__name__))
        else:
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

    def add(self, identified_object: IdentifiedObject) -> bool:
        """
        Associate an object with this service.
        `identified_object` The object to associate with this service.
        Returns True if the object is associated with this service, False otherwise.
        """
        mrid = identified_object.mrid
        if not mrid:
            return False
        # TODO: Only allow supported types

        objs = self._objects_by_type.get(identified_object.__class__, dict())
        if mrid in objs:
            return objs[mrid] is identified_object

        # Check other types and make sure this mRID is unique
        for obj_map in self._objects_by_type.values():
            if mrid in obj_map:
                return False

        unresolved_refs = self._unresolved_references_to.get(mrid, None)
        if unresolved_refs:
            for ref in unresolved_refs:
                ref.resolver.resolve(ref.from_ref, identified_object)
                if ref.reverse_resolver:
                    ref.reverse_resolver.resolve(identified_object, ref.from_ref)
                self._unresolved_references_from[ref.from_ref.mrid].remove(ref)
                if not self._unresolved_references_from[ref.from_ref.mrid]:
                    del self._unresolved_references_from[ref.from_ref.mrid]
            del self._unresolved_references_to[mrid]

        objs[mrid] = identified_object
        self._objects_by_type[identified_object.__class__] = objs
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
        to_mrid = to_mrid
        from_ = bound_resolver.from_obj
        resolver = bound_resolver.resolver
        reverse_resolver = bound_resolver.reverse_resolver
        try:
            # If to_mrid is present in the service, we resolve any references immediately.
            # noinspection PyTypeChecker
            to = self.get(to_mrid, resolver.to_class)
            resolver.resolve(from_, to)
            if reverse_resolver:
                reverse_resolver.resolve(to, from_)

                # Clean up any reverse resolvers now that the reference has been resolved
                if from_.mrid in self._unresolved_references_to:
                    # noinspection PyArgumentList
                    to_remove = UnresolvedReference(from_ref=to, to_mrid=from_.mrid, resolver=reverse_resolver)
                    self._unresolved_references_to[from_.mrid].remove(to_remove)
                    self._unresolved_references_from[to_remove.from_ref.mrid].remove(to_remove)
                    if not self._unresolved_references_from[to_remove.from_ref.mrid]:
                        del self._unresolved_references_from[to_remove.from_ref.mrid]
                    if not self._unresolved_references_to[from_.mrid]:
                        del self._unresolved_references_to[from_.mrid]

            return True
        except KeyError:
            # to_mrid didn't exist in the service, populate the reference caches for resolution when it is added.
            urefs = self._unresolved_references_to.get(to_mrid, set())
            # noinspection PyArgumentList
            uref = UnresolvedReference(from_ref=from_, to_mrid=to_mrid, resolver=resolver, reverse_resolver=reverse_resolver)
            urefs.add(uref)
            self._unresolved_references_to[to_mrid] = urefs
            rev_urefs = self._unresolved_references_from.get(from_.mrid, set())
            rev_urefs.add(uref)
            self._unresolved_references_from[from_.mrid] = rev_urefs
            return False

    def get_unresolved_reference_mrids_by_resolver(self,
                                                   bound_resolvers: Union[BoundReferenceResolver, Sized[BoundReferenceResolver]]) -> Generator[str, None, None]:
        """
        Gets a set of MRIDs that are referenced by the from_obj held by `bound_resolver` that are unresolved.
        `bound_resolver` The `BoundReferenceResolver` to retrieve unresolved references for.
        Returns Set of mRIDs that have unresolved references.
        """
        seen = set()
        try:
            len(bound_resolvers)
            resolvers = bound_resolvers
        except TypeError:
            resolvers = [bound_resolvers]

        for resolver in resolvers:
            if resolver.from_obj.mrid not in self._unresolved_references_from:
                continue
            for ref in self._unresolved_references_from[resolver.from_obj.mrid]:
                if ref.to_mrid not in seen and ref.resolver == resolver.resolver:
                    seen.add(ref.to_mrid)
                    yield ref.to_mrid

    def get_unresolved_references_from(self, mrid: str) -> Generator[UnresolvedReference, None, None]:
        """
        Get the `UnresolvedReference`s that `mrid` has to other objects.
        `mrid` The mRID to get unresolved references for.
        Returns a generator over the `UnresolvedReference`s that need to be resolved for `mrid`.
        """
        if mrid in self._unresolved_references_from:
            for ref in self._unresolved_references_from[mrid]:
                yield ref

    def get_unresolved_references_to(self, mrid: str) -> Generator[UnresolvedReference, None, None]:
        """
        Get the UnresolvedReferences that other objects have to `mrid`.
        `mrid` The mRID to fetch unresolved references for that are pointing to it.
        Returns a generator over the `UnresolvedReference`s that need to be resolved for `mrid`.
        """
        if mrid in self._unresolved_references_to:
            for ref in self._unresolved_references_to[mrid]:
                yield ref

    def remove(self, identified_object: IdentifiedObject) -> bool:
        """
        Disassociate an object from this service.

        `identified_object` THe object to disassociate from the service.
        Raises `KeyError` if `identified_object` or its type was not present in the service.
        """
        del self._objects_by_type[identified_object.__class__][identified_object.mrid]
        return True

    def objects(self, obj_type: Optional[Type[T]] = None, exc_types: Optional[List[type]] = None) -> Generator[T, None, None]:
        """
        Generator for the objects in this service of type `obj_type`.
        `obj_type` The type of object to yield. If this is a base class it will yield all subclasses.
        Returns Generator over
        """
        if obj_type is None:
            for typ, obj_map in self._objects_by_type.items():
                if exc_types:
                    if typ in exc_types:
                        continue
                for obj in obj_map.values():
                    yield obj
            return
        else:
            try:
                for obj in self._objects_by_type[obj_type].values():
                    yield obj
            except KeyError:
                for _type, object_map in self._objects_by_type.items():
                    if issubclass(_type, obj_type):
                        for obj in object_map.values():
                            yield obj

    @property
    def name_types(self) -> Generator[NameType, None, None]:
        """Associates the provided [nameType] with this service."""
        for name_type in self._name_types.values():
            yield name_type

    def add_name_type(self, name_type: NameType) -> bool:
        """
        Associates the provided `name_type` with this service.
        param `name_type` the `NameType` to add to this service
        return true if the object is associated with this service, false if an object already exists in the service with
        the same name.
        """
        if name_type.name in self._name_types:
            return False
        else:
            self._name_types[name_type.name] = name_type
            return True

    def get_name_type(self, name: str) -> NameType:
        """
        Gets the `NameType` for the provided type name associated with this service.
        :raises KeyError: if `name` doesn't exist in this service.
        """
        return self._name_types[name]
