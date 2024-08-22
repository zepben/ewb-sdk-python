#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from traceback import print_tb, format_tb
from typing import TypeVar, Type, Set

from zepben.evolve import IdentifiedObject, BaseService, BaseServiceComparator, EquipmentContainer, OperationalRestriction, ConnectivityNode, TableVersion, \
    TableMetadataDataSources, TableNameTypes, TableNames, SqliteTable
from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject

T = TypeVar("T", bound=IdentifiedObject)

_excluded_base_tables: Set[Type[SqliteTable]] = {TableVersion, TableMetadataDataSources, TableNameTypes, TableNames}


def validate_service_translations(
    service_type: Type[BaseService],
    comparator: BaseServiceComparator,
    database_tables: BaseDatabaseTables,
    excluded_tables: Set[Type[SqliteTable]],
    **kwargs
):
    expected_tables = {it.__class__ for it in database_tables.tables} - excluded_tables - _excluded_base_tables
    if len(kwargs) != len(expected_tables):
        actual = {k.removeprefix("create_") for k, v in kwargs.items()}
        expected = {it().name for it in expected_tables}

        # create variant without the last two letters to cater for `s` and `es` plurals in the logging.
        actual_with_s = {it + "s" for it in actual}
        actual_with_es = {it + "es" for it in actual}

        # create variant with an extra `s` and `es` for plurals in the logging.
        expected_without_last = {it[:-1] for it in expected}
        expected_without_last_two = {it[:-2] for it in expected}

        assert False, (
            # NOTE: There may be a mismatch in the text produced for things that are pluralised with `es`. These are not the problem,
            # ignore them and go look elsewhere for the problem.
            "The number of items being validated did not match the number of items writen to the database. Did you forget to validate an item, " +
            "or to exclude the table if it was an association or array data?" +
            _format_validation_error("Unexpected", actual - expected - expected_without_last - expected_without_last_two) +
            _format_validation_error("Missing", expected - actual - actual_with_s - actual_with_es)
        )

    print()
    diffs = {}
    processing = ""
    try:
        for desc, cim in kwargs.items():
            processing = f"blank {desc}"
            blank = type(cim)()

            # Convert the blank object to protobuf and ensure it didn't get converted to an instance of PBIdentifiedObject,
            # which indicates a missing `to_pb` implementation or import.
            blank_as_pb = blank.to_pb()
            assert type(blank_as_pb) is not PBIdentifiedObject, f"There is something wrong with {type(cim)}.to_pb. It is calling directly to the base class."

            # noinspection PyUnresolvedReferences
            translated_blank = service_type().add_from_pb(blank_as_pb)
            assert translated_blank is not None, f"{blank_as_pb}: Failed to add the translated protobuf object to the service."
            assert type(translated_blank) is type(cim), f"{translated_blank}: Converted object should be the same type as {cim}"

            result = comparator.compare_objects(blank, translated_blank)
            if result.differences:
                diffs[f"blank {desc}"] = result

            processing = f"populated {desc}"
            _remove_unsent_references(cim)
            # noinspection PyUnresolvedReferences
            service = service_type()  # outside _add_with_unresolved_references so weak references on `cim` cant be garbage collected before being compared.
            result = comparator.compare_objects(cim, _add_with_unresolved_references(service, cim))
            if result.differences:
                diffs[f"populated {desc}"] = result
    except BaseException as e:
        print("###########################")
        print(f"Processing {processing}:")
        print(f"Exception [{type(e).__name__}: {e}")
        test = format_tb(e.__traceback__)
        print_tb(e.__traceback__)
        print("---------------------------")
        print(diffs)
        print("###########################")
        raise e
    else:
        if diffs:
            print(diffs)
        assert not diffs


def _format_validation_error(description: str, classes: Set[str]) -> str:
    return f"\n{description}: {classes}\n" if classes else ""


def _remove_unsent_references(cim: T):
    if isinstance(cim, EquipmentContainer):
        cim.clear_equipment()
        cim.clear_current_equipment()

    if isinstance(cim, OperationalRestriction):
        cim.clear_equipment()

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
