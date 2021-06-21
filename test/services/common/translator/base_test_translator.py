#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from traceback import print_exc
from typing import TypeVar, Type

from zepben.evolve import IdentifiedObject, BaseService, BaseServiceComparator, EquipmentContainer, OperationalRestriction, Feeder, ConnectivityNode

T = TypeVar("T", bound=IdentifiedObject)


def validate_service_translations(service_type: Type[BaseService], comparator: BaseServiceComparator, **kwargs):
    print()
    diffs = {}
    processing = ""
    try:
        for desc, cim in kwargs.items():
            processing = f"blank {desc}"
            blank = type(cim)()
            # noinspection PyUnresolvedReferences
            result = comparator.compare_objects(blank, service_type().add_from_pb(blank.to_pb()))
            if result.differences:
                diffs[f"blank {desc}"] = result

            processing = f"populated {desc}"
            _remove_unsent_references(cim)
            # noinspection PyUnresolvedReferences
            result = comparator.compare_objects(cim, _add_with_unresolved_references(service_type(), cim))
            if result.differences:
                diffs[f"populated {desc}"] = result
    except BaseException as e:
        print("###########################")
        print(f"Processing {processing}:")
        print(f"Exception [{type(e).__name__}: {e}")
        print_exc()
        print("---------------------------")
        print(diffs)
        print("###########################")
        raise e
    else:
        if diffs:
            print(diffs)
        assert not diffs


def _remove_unsent_references(cim: T):
    if isinstance(cim, EquipmentContainer):
        cim.clear_equipment()

    if isinstance(cim, OperationalRestriction):
        cim.clear_equipment()

    if isinstance(cim, Feeder):
        cim.clear_current_equipment()

    if isinstance(cim, ConnectivityNode):
        cim.clear_terminals()


def _add_with_unresolved_references(service: BaseService, cim: T) -> T:
    # We need to convert the populated item before we check the differences so we can complete the unresolved references.
    # noinspection PyUnresolvedReferences
    converted_cim = service.add_from_pb(cim.to_pb())
    for ref in service.unresolved_references():
        try:
            service.add(ref.resolver.to_class(ref.to_mrid))
        except Exception as e:
            # If this fails you need to add a concrete type mapping to the abstractCreators map at the top of this class.
            assert False, f"Failed to create unresolved reference for {ref.resolver.to_class.__name__}. {e}"

    return converted_cim
