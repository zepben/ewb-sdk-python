#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from math import isnan
from types import MemberDescriptorType
from typing import get_type_hints, Dict, Type, Callable, Any, TypeVar, Optional, Union, List, Tuple

from zepben.evolve import BaseService, IdentifiedObject, Organisation, Document, OrganisationRole
from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.services.common.difference import ObjectDifference, Difference, ValueDifference, ReferenceDifference, CollectionDifference, IndexedDifference
from zepben.evolve.services.common.translator.service_differences import ServiceDifferences

T = TypeVar("T")


class BaseServiceComparator:

    def __init__(self):
        def _is_valid_compare_func(func_name, func):
            if not func_name.startswith("_compare_"):
                return False

            try:
                type_hints = get_type_hints(func)
                return ((len(type_hints) == 3)
                        and ("source" in type_hints)
                        and ("target" in type_hints)
                        and ("return" in type_hints)
                        and (type_hints["source"] == type_hints["target"])
                        and (issubclass(type_hints["return"], ObjectDifference))
                        )
            except TypeError:
                return False

        def _find_comparisons_for_type(type_of: Type):
            for k, v in type_of.__dict__.items():
                if _is_valid_compare_func(k, v):
                    self._compare_by_type[get_type_hints(v)["source"]] = v
            for base_of in type_of.__bases__:
                _find_comparisons_for_type(base_of)

        self._compare_by_type: Dict[Type, Callable[[Any, T, T], ObjectDifference]] = {}
        _find_comparisons_for_type(type(self))

    def compare_services(self, source: BaseService, target: BaseService, compare_name_types: bool = True) -> ServiceDifferences:
        """
        Run the compare with the specified optional checks

        :param source: The service to use as the source
        :param target: The service to use as the target
        :param compare_name_types: Optional parameter to suppress comparing name types

        :return: The differences detected between the source and the target
        """
        differences = ServiceDifferences(
            lambda mrid: source.get(mrid, default=None),
            lambda mrid: target.get(mrid, default=None),
            lambda name: source.get_name_type(name),
            lambda name: target.get_name_type(name)
        )

        for s in source.objects():
            t = target.get(s.mrid, default=None)
            if t:
                source_type = type(s)
                if source_type != type(t):
                    differences.add_to_missing_from_source(s.mrid)
                    differences.add_to_missing_from_target(s.mrid)
                else:
                    diff = self._try_compare(source_type, s, t)
                    if diff.differences:
                        differences.add_modifications(s.mrid, diff)
            else:
                differences.add_to_missing_from_target(s.mrid)

        for t in target.objects():
            if t.mrid not in source:
                differences.add_to_missing_from_source(t.mrid)

        if compare_name_types:
            for s in source.name_types:
                try:
                    t = target.get_name_type(s.name)
                    difference = self._compare_name_type(s, t)
                    if difference.differences:
                        differences.add_modifications(s.name, difference)
                except KeyError:
                    differences.add_to_missing_from_target(s.name)

            for t in target.name_types:
                try:
                    source.get_name_type(t.name)
                except KeyError:
                    differences.add_to_missing_from_source(t.name)

        return differences

    def compare_objects(self, source: T, target: T) -> ObjectDifference:
        """
        Compare the attributes of two objects. See :class:`ObjectDifference`.

        :param source: the source object to compare
        :param target: the target object to compare

        :return: The differences detected between the source and the target
        """
        source_type = type(source)
        target_type = type(target)

        if source_type != target_type:
            raise ValueError(f"source and target must be of the same type. {source_type.__name__} vs {target_type.__name__}")
        return self._try_compare(source_type, source, target)

    def _try_compare(self, source_type: Type, s: T, t: T) -> ObjectDifference:
        try:
            compare = self._compare_by_type[source_type]
        except KeyError:
            raise AssertionError(f"INTERNAL ERROR: Attempted to compare {source_type.__name__} which is not registered with the comparator.")

        return compare(self, s, t)

    def _compare_organisation(self, source: Organisation, target: Organisation) -> ObjectDifference:
        return self._compare_identified_object(ObjectDifference(source, target))

    def _compare_identified_object(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, IdentifiedObject.mrid, IdentifiedObject.name, IdentifiedObject.description)
        self._compare_names(diff, IdentifiedObject.names)
        return diff

    def _compare_name_type(self, source: NameType, target: NameType) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, NameType.description)

        def compare_names(s: Name, t: Name) -> bool:
            return s.name == t.name and s.type.name == t.type.name and s.identified_object.mrid == t.identified_object.mrid

        differences = CollectionDifference()

        for s_name in source.names:
            if not [t_name for t_name in target.names if compare_names(s_name, t_name)]:
                differences.missing_from_target.append(s_name)

        for t_name in target.names:
            if not [s_name for s_name in source.names if compare_names(s_name, t_name)]:
                differences.missing_from_source.append(t_name)

        if differences.missing_from_source or differences.missing_from_target:
            diff.differences[NameType.names.fget.__name__] = differences
        return diff

    def _compare_document(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, Document.title, Document.created_date_time, Document.author_name, Document.type, Document.status, Document.comment)
        return self._compare_identified_object(diff)

    def _compare_organisation_role(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_id_references(diff, OrganisationRole.organisation)
        return self._compare_identified_object(diff)

    def _compare_values(self, diff: ObjectDifference, *properties) -> ObjectDifference:
        for it in properties:
            if isinstance(it, property):
                self._add_if_different(diff, it.fget.__name__, self._calculate_values_diff(it, diff))
            else:
                self._add_if_different(diff, it.__name__, self._calculate_values_diff(it, diff))
        return diff

    def _compare_floats(self, diff: ObjectDifference, *properties) -> ObjectDifference:
        for it in properties:
            if isinstance(it, property):
                self._add_if_different(diff, it.fget.__name__, self._calculate_float_diff(it, diff))
            else:
                self._add_if_different(diff, it.__name__, self._calculate_float_diff(it, diff))
        return diff

    def _compare_id_references(self, diff: ObjectDifference, *properties) -> ObjectDifference:
        for it in properties:
            if isinstance(it, property):
                self._add_if_different(diff, it.fget.__name__, self._calculate_id_reference_diff(it, diff))
            else:
                self._add_if_different(diff, it.__name__, self._calculate_id_reference_diff(it, diff))
        return diff

    def _compare_names(self, diff: ObjectDifference, *properties) -> ObjectDifference:
        for it in properties:
            if isinstance(it, property):
                self._add_if_different(diff, it.fget.__name__, self.calculate_name_diff(it, diff))
            else:
                self._add_if_different(diff, it.__name__, self.calculate_name_diff(it, diff))
        return diff

    def _compare_id_reference_collections(self, diff: ObjectDifference, *properties) -> ObjectDifference:
        for it in properties:
            self._add_if_different(diff, it.fget.__name__, self._calculate_id_reference_collection_diff(it, diff))
        return diff

    def _compare_indexed_id_reference_collections(self, diff: ObjectDifference, *properties) -> ObjectDifference:
        for it in properties:
            self._add_if_different(diff, it.fget.__name__, self._calculate_indexed_id_reference_collection_diff(it, diff))
        return diff

    def _compare_indexed_value_collections(self, diff: ObjectDifference, *properties) -> ObjectDifference:
        for it in properties:
            self._add_if_different(diff, it.fget.__name__, self._calculate_indexed_value_collection_diff(it, diff))
        return diff

    @staticmethod
    def _add_if_different(diff: ObjectDifference, name: str, difference: Optional[Difference]):
        if difference:
            diff.differences[name] = difference

    @staticmethod
    def _calculate_values_diff(prop: Union[MemberDescriptorType, property], diff: ObjectDifference) -> Optional[ValueDifference]:
        if isinstance(prop, property):
            s_val = getattr(diff.source, prop.fget.__name__) if diff.source else None
            t_val = getattr(diff.target, prop.fget.__name__) if diff.target else None
        else:
            s_val = getattr(diff.source, prop.__name__) if diff.source else None
            t_val = getattr(diff.target, prop.__name__) if diff.target else None

        if (type(s_val) == float) or (type(t_val) == float):
            raise TypeError(f"Using wrong comparator for {prop}, use _calculate_float_diff instead.")

        if s_val == t_val:
            return None
        else:
            return ValueDifference(s_val, t_val)

    @staticmethod
    def _calculate_float_diff(prop: Union[MemberDescriptorType, property], diff: ObjectDifference) -> Optional[ValueDifference]:
        if isinstance(prop, property):
            s_val = getattr(diff.source, prop.fget.__name__) if diff.source else None
            t_val = getattr(diff.target, prop.fget.__name__) if diff.target else None
        else:
            s_val = getattr(diff.source, prop.__name__) if diff.source else None
            t_val = getattr(diff.target, prop.__name__) if diff.target else None

        if s_val == t_val:
            return None
        elif (s_val is not None) and (t_val is not None) and isnan(s_val) and isnan(t_val):
            return None
        else:
            return ValueDifference(s_val, t_val)

    @staticmethod
    def _calculate_id_reference_diff(prop: Union[MemberDescriptorType, property], diff: ObjectDifference) -> Optional[ReferenceDifference]:
        if isinstance(prop, property):
            s_ref = getattr(diff.source, prop.fget.__name__) if diff.source else None
            t_ref = getattr(diff.target, prop.fget.__name__) if diff.target else None
        else:
            s_ref = getattr(diff.source, prop.__name__) if diff.source else None
            t_ref = getattr(diff.target, prop.__name__) if diff.target else None

        if (s_ref is None) and (t_ref is None):
            return None
        elif (s_ref is not None) and (t_ref is not None) and (s_ref.mrid == t_ref.mrid):
            return None
        else:
            return ReferenceDifference(s_ref, t_ref)

    def calculate_name_diff(self, prop: property, diff: ObjectDifference) -> Optional[CollectionDifference]:
        differences = CollectionDifference()

        if isinstance(prop, property):
            source_collection = list(getattr(diff.source, prop.fget.__name__)) if diff.source else None
            target_collection = list(getattr(diff.target, prop.fget.__name__)) if diff.target else None
        else:
            source_collection = list(getattr(diff.source, prop.__name__)) if diff.source else None
            target_collection = list(getattr(diff.target, prop.__name__)) if diff.target else None

        source_name_type_names: List[Tuple[str, str]] = []
        for source_io in source_collection:
            source_name_type_names.append((source_io.type.name, source_io.name))
            if not next((io for io in target_collection if (io.name == source_io.name) and (io.type.name == source_io.type.name)), None):
                differences.missing_from_target.append(source_io)

        for target_io in target_collection:
            if not next((io for io in source_collection if (io.name == target_io.name) and (io.type.name == target_io.type.name)), None):
                differences.missing_from_source.append(target_io)

        return self._none_if_empty(differences)

    def _calculate_id_reference_collection_diff(self, prop: property, diff: ObjectDifference) -> Optional[CollectionDifference]:
        differences = CollectionDifference()
        source_collection = list(getattr(diff.source, prop.fget.__name__))
        target_collection = list(getattr(diff.target, prop.fget.__name__))

        source_mrids = set()
        for s_obj in source_collection:
            source_mrids.add(s_obj.mrid)
            t_obj = next((it for it in target_collection if it.mrid == s_obj.mrid), None)
            if t_obj is None:
                differences.missing_from_target.append(s_obj)

        for it in target_collection:
            if it.mrid not in source_mrids:
                differences.missing_from_source.append(it)

        return self._none_if_empty(differences)

    def _calculate_indexed_id_reference_collection_diff(self, prop: property, diff: ObjectDifference) -> Optional[CollectionDifference]:
        differences = CollectionDifference()
        source_list = list(getattr(diff.source, prop.fget.__name__))
        target_list = list(getattr(diff.target, prop.fget.__name__))

        for index, s_obj in enumerate(source_list):
            try:
                t_obj = target_list[index]
            except IndexError:
                t_obj = None

            if t_obj is None:
                differences.missing_from_target.append(IndexedDifference(index, ReferenceDifference(s_obj, None)))
            elif t_obj.mrid != s_obj.mrid:
                differences.modifications.append(IndexedDifference(index, ReferenceDifference(s_obj, t_obj)))

        for index in range(len(source_list), len(target_list)):
            differences.missing_from_source.append(IndexedDifference(index, ReferenceDifference(None, target_list[index])))

        return self._none_if_empty(differences)

    def _calculate_indexed_value_collection_diff(self, prop: property, diff: ObjectDifference) -> Optional[CollectionDifference]:
        differences = CollectionDifference()
        source_list = list(getattr(diff.source, prop.fget.__name__))
        target_list = list(getattr(diff.target, prop.fget.__name__))

        for index, source_value in enumerate(source_list):
            try:
                target_value = target_list[index]
            except IndexError:
                target_value = None

            if target_value is None:
                differences.missing_from_target.append(IndexedDifference(index, ValueDifference(source_value, None)))
            elif target_value != source_value:
                differences.modifications.append(IndexedDifference(index, ValueDifference(source_value, target_value)))

        for index in range(len(source_list), len(target_list)):
            differences.missing_from_source.append(IndexedDifference(index, ValueDifference(None, target_list[index])))

        return self._none_if_empty(differences)

    @staticmethod
    def _none_if_empty(diff: CollectionDifference):
        if not diff.missing_from_source and not diff.missing_from_target and not diff.modifications:
            return None
        else:
            return diff
