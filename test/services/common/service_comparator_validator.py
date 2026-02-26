#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from types import MemberDescriptorType
from typing import Optional, Any, Callable, TypeVar, Union, Type, Set

from zepben.ewb import (IdentifiedObject, TIdentifiedObject, ObjectDifference, BaseService, CollectionDifference,
                        Difference, ReferenceDifference, ValueDifference, IndexedDifference)
from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType
from zepben.ewb.services.network.network_service_comparator import NetworkServiceComparatorOptions

TService = TypeVar("TService", bound=BaseService)
C = TypeVar("C")
R = TypeVar("R")
Property = Union[MemberDescriptorType, property]


#
# NOTE: The callables below that use `...` do so to work around bugs in the type checking of both the IDE and mypy.
#       Ideally they should have `add: Callable[[TIdentifiedObject, R], Any]`.
#


class ServiceComparatorValidator(object):
    create_service: Callable[[], TService]
    create_comparator: Callable[[NetworkServiceComparatorOptions], C]

    def __init__(self, create_service: Callable[[], BaseService], create_comparator: Callable[[NetworkServiceComparatorOptions], C]):
        self.create_service = create_service
        self.create_comparator = create_comparator

    def validate_name_types(
        self,
        source: NameType,
        target: NameType,
        expect_modification: Optional[ObjectDifference] = None,
        expect_missing_from_target: Optional[NameType] = None,
        expect_missing_from_source: Optional[NameType] = None,
        options: NetworkServiceComparatorOptions = NetworkServiceComparatorOptions()
    ):
        source_service = self.create_service()
        target_service = self.create_service()

        source_service.add_name_type(source)
        target_service.add_name_type(target)

        diff = self.create_comparator(options).compare_services(source_service, target_service)

        if expect_modification:
            assert [x[1] for x in diff.modifications()] == [expect_modification]
        else:
            assert not list(diff.modifications())

        if expect_missing_from_target:
            assert list(diff.missing_from_target()) == [expect_missing_from_target.name]
        else:
            assert not list(diff.missing_from_target())

        if expect_missing_from_source:
            assert list(diff.missing_from_source()) == [expect_missing_from_source.name]
        else:
            assert not list(diff.missing_from_source())

    def validate_compare(
        self,
        source: Any,
        target: Any,
        expect_modification: Optional[ObjectDifference] = None,
        options: NetworkServiceComparatorOptions = NetworkServiceComparatorOptions(),
        options_stop_compare: bool = False,
        expected_differences: Set[str] = None
    ):
        if not expect_modification:
            expect_modification = ObjectDifference(source, target)

        diff = self.create_comparator(NetworkServiceComparatorOptions()).compare_objects(source, target)
        if expected_differences:
            diff.differences = {k: v for (k, v) in diff.differences.items() if k not in expected_differences}

        assert diff == expect_modification, f"Actual:\n{diff}\n    vs\nExpected:\n{expect_modification}"

        if options_stop_compare:
            no_diff_expected = self.create_comparator(options).compare_objects(source, target)
            assert no_diff_expected == ObjectDifference(source, target)

    def validate_property(
        self,
        prop: Any,  # should be Property but it types are not interpreted correctly so it gives a lot of errors.
        creator: Type[TIdentifiedObject],
        create_value: Callable[[TIdentifiedObject], R],
        create_other_value: Callable[[TIdentifiedObject], R],
        options: NetworkServiceComparatorOptions = NetworkServiceComparatorOptions(),
        options_stop_compare: bool = False,
        expected_differences: Set[str] = None
    ):
        subject = creator("mRID")
        matching = creator("mRID")
        modified = creator("mRID")

        _set_prop(subject, prop, create_value(subject))
        _set_prop(matching, prop, create_value(matching))
        _set_prop(modified, prop, create_other_value(modified))

        self.validate_compare(subject, matching, options=options, options_stop_compare=options_stop_compare)

        diff = ObjectDifference(subject, modified, {
            _prop_name(prop): self._get_value_or_reference_difference(_get_prop(subject, prop), _get_prop(modified, prop))
        })

        self._validate_expected(diff, options, options_stop_compare, expected_differences)

    def validate_val_property(
        self,
        prop: Any,  # should be Property but it types are not interpreted correctly so it gives a lot of errors.
        creator: Any,  # should be Optional[Type[TIdentifiedObject] | Callable[[str], TIdentifiedObject]] but that doesn't work,
        change_state: Callable[[TIdentifiedObject, R], None],
        other_change_state: Callable[[TIdentifiedObject, R], None],
        options: NetworkServiceComparatorOptions = NetworkServiceComparatorOptions(),
        options_stop_compare: bool = False,
        expected_differences: Set[str] = None
    ):
        subject = creator("mRID")
        matching = creator("mRID")
        modified = creator("mRID")

        change_state(subject, _get_prop(subject, prop))
        change_state(matching, _get_prop(matching, prop))
        other_change_state(modified, _get_prop(modified, prop))

        self.validate_compare(subject, matching, options=options, options_stop_compare=options_stop_compare)

        diff = ObjectDifference(subject, modified, {
            _prop_name(prop): self._get_value_or_reference_difference(_get_prop(subject, prop), _get_prop(modified, prop))
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences)

    def validate_collection(
        self,
        prop: Property,
        add_to_collection: Callable[..., Any],
        creator: Type[TIdentifiedObject],
        create_item: Callable[[TIdentifiedObject], R],
        create_other_item: Callable[[TIdentifiedObject], R],
        options: NetworkServiceComparatorOptions = NetworkServiceComparatorOptions(),
        options_stop_compare: bool = False,
        expected_differences: Set[str] = None
    ):
        source_empty = creator("mRID")
        target_empty = creator("mRID")
        in_source = creator("mRID")
        in_target = creator("mRID")
        in_target_difference = creator("mRID")

        add_to_collection(in_source, create_item(in_source))
        add_to_collection(in_target, create_item(in_target))
        add_to_collection(in_target_difference, create_other_item(in_target_difference))

        self.validate_compare(source_empty, target_empty, options=options, options_stop_compare=options_stop_compare)
        self.validate_compare(in_source, in_target, options=options, options_stop_compare=options_stop_compare)

        diff = ObjectDifference(in_source, target_empty, {
            _prop_name(prop): CollectionDifference(missing_from_target=[next(_get_prop(in_source, prop))])
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences=expected_differences)

        diff = ObjectDifference(source_empty, in_target, {
            _prop_name(prop): CollectionDifference(missing_from_source=[next(_get_prop(in_target, prop))])
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences=expected_differences)

        diff = ObjectDifference(in_source, in_target_difference, {
            _prop_name(prop): CollectionDifference(
                missing_from_source=[next(_get_prop(in_target_difference, prop))],
                missing_from_target=[next(_get_prop(in_source, prop))]
            )
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences)

    def validate_name_collection(
        self,
        creator: [[str], TIdentifiedObject],
        options: NetworkServiceComparatorOptions = NetworkServiceComparatorOptions(),
        options_stop_compare: bool = False,
        expected_differences: Set[str] = None
    ):
        source_empty: IdentifiedObject = creator("mRID")
        target_empty: IdentifiedObject = creator("mRID")
        in_source: IdentifiedObject = creator("mRID")
        in_target: IdentifiedObject = creator("mRID")
        in_target_difference: IdentifiedObject = creator("mRID")

        # noinspection PyArgumentList
        name_type = NameType("type")

        in_source.add_name(name_type, "name1")
        in_target.add_name(name_type, "name1")
        in_target_difference.add_name(name_type, "name2")

        self.validate_compare(source_empty, target_empty, options=options, options_stop_compare=options_stop_compare)
        self.validate_compare(in_source, in_target, options=options, options_stop_compare=options_stop_compare)

        diff = ObjectDifference(in_source, target_empty, {
            _prop_name(IdentifiedObject.names): CollectionDifference(missing_from_target=[next(_get_prop(in_source, IdentifiedObject.names))])
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences=expected_differences)

        diff = ObjectDifference(source_empty, in_target, {
            _prop_name(IdentifiedObject.names): CollectionDifference(missing_from_source=[next(_get_prop(in_target, IdentifiedObject.names))])
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences=expected_differences)

        diff = ObjectDifference(in_source, in_target_difference, {
            _prop_name(IdentifiedObject.names): CollectionDifference(
                missing_from_source=[next(_get_prop(in_target_difference, IdentifiedObject.names))],
                missing_from_target=[next(_get_prop(in_source, IdentifiedObject.names))]
            )
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences)

    def validate_indexed_collection(
        self,
        prop: Property,
        add_to_collection: Callable[..., Any],
        creator: [[str], TIdentifiedObject],
        create_item: Callable[[TIdentifiedObject], R],
        create_other_item: Callable[[TIdentifiedObject], R],
        options: NetworkServiceComparatorOptions = NetworkServiceComparatorOptions(),
        options_stop_compare: bool = False,
        expected_differences: Set[str] = None
    ):
        source_empty = creator("mRID")
        target_empty = creator("mRID")
        in_source = creator("mRID")
        in_target = creator("mRID")
        target_different = creator("mRID")

        add_to_collection(in_source, create_item(in_source))
        add_to_collection(in_target, create_item(in_target))
        add_to_collection(target_different, create_other_item(target_different))

        self.validate_compare(source_empty, target_empty, options=options, options_stop_compare=options_stop_compare)
        self.validate_compare(in_source, in_target, options=options, options_stop_compare=options_stop_compare)

        def get_item(obj) -> Optional[Any]:
            return next(_get_prop(obj, prop), None)

        diff = ObjectDifference(in_source, target_empty, {
            _prop_name(prop): CollectionDifference(missing_from_target=[
                IndexedDifference(0, self._get_value_or_reference_difference(get_item(in_source), None))
            ])
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences=expected_differences)

        diff = ObjectDifference(source_empty, in_target, {
            _prop_name(prop): CollectionDifference(missing_from_source=[
                IndexedDifference(0, self._get_value_or_reference_difference(None, get_item(in_target)))
            ])
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences=expected_differences)

        diff = ObjectDifference(in_source, target_different, {
            _prop_name(prop): CollectionDifference(modifications=[
                IndexedDifference(0, self._get_value_or_reference_difference(get_item(in_source), get_item(target_different)))
            ])
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences=expected_differences)

    K = TypeVar('K')
    R = TypeVar('R')

    def validate_unordered_collection(
        self,
        prop: Property,
        add_to_collection: Callable[..., Any],
        creator: [[str], TIdentifiedObject],
        create_item_1: Callable[[K], R],
        create_item_2: Callable[[K], R],
        create_diff_item_1: Callable[[K], R],
        options: NetworkServiceComparatorOptions = NetworkServiceComparatorOptions(),
        options_stop_compare: bool = False,
        expected_differences: Set[str] = None
    ):
        source_empty = creator("mRID")
        target_empty = creator("mRID")
        self.validate_compare(source_empty, target_empty, options=options, options_stop_compare=options_stop_compare)

        in_source = creator("mRID")
        item1 = create_item_1(in_source)
        add_to_collection(in_source, item1)

        item2 = create_item_2(in_source)
        add_to_collection(in_source, item2)

        in_target_same_order = creator("mRID")
        item1 = create_item_1(in_target_same_order)
        add_to_collection(in_target_same_order, item1)

        item2 = create_item_2(in_target_same_order)
        add_to_collection(in_target_same_order, item2)

        self.validate_compare(in_source, in_target_same_order, options=options, options_stop_compare=options_stop_compare)

        in_target_diff_order = creator("mRID")
        item2 = create_item_2(in_target_diff_order)
        add_to_collection(in_target_diff_order, item2)

        item1 = create_item_1(in_target_diff_order)
        add_to_collection(in_target_diff_order, item1)

        self.validate_compare(in_source, in_target_diff_order, options=options, options_stop_compare=options_stop_compare)

        def get_item_1(it):
            return list(_get_prop(it, prop))[0]

        def get_item_2(it):
            return list(_get_prop(it, prop))[-1]

        diff = ObjectDifference(in_source, target_empty, {
            _prop_name(prop): CollectionDifference(missing_from_target=[
                self._get_value_or_reference_difference(get_item_1(in_source), None),
                self._get_value_or_reference_difference(get_item_2(in_source), None)
            ])
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences=expected_differences)

        diff = ObjectDifference(source_empty, in_target_same_order, {
            _prop_name(prop): CollectionDifference(missing_from_source=[
                self._get_value_or_reference_difference(None, get_item_1(in_target_same_order)),
                self._get_value_or_reference_difference(None, get_item_2(in_target_same_order))
            ])
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences=expected_differences)

        target_different = creator("mRID")
        item1 = create_diff_item_1(target_different)
        add_to_collection(target_different, item1)

        item2 = create_item_2(target_different)
        add_to_collection(target_different, item2)

        diff = ObjectDifference(in_source, target_different, {
            _prop_name(prop): CollectionDifference(modifications=[
                self._get_value_or_reference_difference(get_item_1(in_source), get_item_1(target_different)),
            ])
        })
        self._validate_expected(diff, options, options_stop_compare, expected_differences=expected_differences)

    @staticmethod
    def _get_value_or_reference_difference(source: Optional[R], target: Optional[R]) -> Difference:
        if isinstance(source, IdentifiedObject) or isinstance(target, IdentifiedObject):
            return ReferenceDifference(source, target)
        else:
            return ValueDifference(source, target)

    def _validate_expected(self, diff: ObjectDifference, options: NetworkServiceComparatorOptions, options_stop_compare: bool = False,
                           expected_differences: Set[str] = None):
        self.validate_compare(diff.source, diff.target, expect_modification=diff, options=options, options_stop_compare=options_stop_compare,
                              expected_differences=expected_differences)


def _prop_name(prop: Property) -> str:
    if isinstance(prop, property):
        return prop.fget.__name__
    else:
        return prop.__name__


def _get_prop(it: Any, prop: Property) -> Any:
    if isinstance(prop, property):
        return getattr(it, prop.fget.__name__)
    else:
        return getattr(it, prop.__name__)


def _set_prop(it: Any, prop: Property, value: Any):
    if isinstance(prop, property):
        return setattr(it, prop.fset.__name__, value)
    else:
        return setattr(it, prop.__name__, value)
