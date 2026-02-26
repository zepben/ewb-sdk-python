#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from traceback import print_tb
from typing import TypeVar, Type, Set, Any, cast, Callable

from hypothesis import given
from hypothesis.strategies import SearchStrategy
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject

from zepben.ewb.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.ewb.database.sqlite.tables.iec61970.base.core.table_name_types import TableNameTypes
from zepben.ewb.database.sqlite.tables.iec61970.base.core.table_names import TableNames
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable
from zepben.ewb.database.sqlite.tables.table_metadata_data_sources import TableMetadataDataSources
from zepben.ewb.database.sqlite.tables.table_version import TableVersion
from zepben.ewb.model.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.ewb.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal
from zepben.ewb.services.common.base_service import BaseService
from zepben.ewb.services.common.base_service_comparator import BaseServiceComparator
from zepben.ewb.services.common.reference_resolvers import shunt_compensator_to_terminal_resolver, UnresolvedReference
from zepben.ewb.services.customer.customers import CustomerService
from zepben.ewb.services.diagram.diagrams import DiagramService
from zepben.ewb.services.network.network_service import NetworkService

T = TypeVar("T", bound=IdentifiedObject)

_excluded_base_tables: Set[Type[SqliteTable]] = {TableVersion, TableMetadataDataSources, TableNameTypes, TableNames}


def validate_service_translations(
    service_type: Type[NetworkService | CustomerService | DiagramService],
    comparator: BaseServiceComparator,
    database_tables: BaseDatabaseTables,
    excluded_tables: Set[Type[SqliteTable]],
    types_to_test: dict[str, SearchStrategy[Any]],
):
    expected_tables = {it.__class__ for it in database_tables.tables} - excluded_tables - _excluded_base_tables
    if len(types_to_test) != len(expected_tables):
        actual = {k.removeprefix("create_") for k in types_to_test.keys()}
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
        for desc, cim_builder in types_to_test.items():
            print(desc)
            processing = f"generating given {desc}"

            @given(cim_builder)
            def run_test(cim):
                nonlocal processing
                processing = f"blank {desc}"
                blank = type(cim)(mrid="blank")

                # Convert the blank object to protobuf and ensure it didn't get converted to an instance of PBIdentifiedObject,
                # which indicates a missing `to_pb` implementation or import.
                blank_as_pb = blank.to_pb()
                assert type(
                    blank_as_pb) is not PBIdentifiedObject, f"There is something wrong with {type(cim)}.to_pb. It is calling directly to the base class."

                # noinspection PyUnresolvedReferences
                translated_blank = service_type().add_from_pb(blank_as_pb)
                assert translated_blank is not None, f"{blank_as_pb}: Failed to add the translated protobuf object to the service."
                assert type(translated_blank) is type(cim), f"{translated_blank}: Converted object should be the same type as {cim}"

                result = comparator.compare_objects(blank, translated_blank)
                if result.differences:
                    diffs[f"blank {desc}"] = result

                processing = f"populated {desc}"
                _remove_unsent_references(cim)
                # outside _add_with_unresolved_references so weak references on `cim` cant be garbage collected before being compared.
                service = service_type()
                result = comparator.compare_objects(cim, _add_with_unresolved_references(service, cim))
                if result.differences:
                    diffs[f"populated {desc}"] = result

            run_test()
    except BaseException as e:
        print("###########################")
        print(f"Processing {processing}:")
        print(f"Exception [{type(e).__name__}: {e}")
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

    def resolve(unresolved_reference: UnresolvedReference):
        _, to_mrid, resolver, _ = unresolved_reference
        try:
            io = unresolved_reference.resolver.to_class(unresolved_reference.to_mrid)

            # Special case for the shunt compensator grounding terminal which must have phase N.
            if resolver is shunt_compensator_to_terminal_resolver:
                cast(Terminal, io).phases = PhaseCode.N

            service.add(io)
        except Exception as e:
            # If this fails you need to add a concrete type mapping to the abstractCreators map at the top of this class.
            raise TypeError(f"Failed to create unresolved reference for {resolver.to_class}.", e)

    def resolve_all(predicate: Callable[[UnresolvedReference], bool]):
        # Collect to a list to prevent hte underlying collection changing as we iterate.
        for it in [ref for ref in service.unresolved_references() if predicate(ref)]:
            resolve(it)

    #
    # NOTE: We need a special case to exclude any `ShuntCompensator.groundingTerminal` resolvers to ensure it is added after any other
    #       terminals, to prevent assigning incorrect sequence numbers when we create unresolved terminals. This is complicated by
    #       having a matching resolver being added in the `ConductingEquipment.terminals` that also needs to be delayed.
    #
    delay_ids = {it.to_mrid for it in service.unresolved_references() if it.resolver is shunt_compensator_to_terminal_resolver}
    if delay_ids:
        resolve_all(lambda it: it.to_mrid not in delay_ids)
        # Make sure we resolve the `grounding_terminal` reference before its matching the `terminals` one, otherwise we will end up with the wrong phases.
        resolve_all(lambda it: it.resolver is shunt_compensator_to_terminal_resolver)

    resolve_all(lambda _: True)

    return converted_cim
