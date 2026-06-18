# AGENTS.md - ewb-sdk-python

## Repository Purpose

This is the Python SDK for the Energy Workbench (EWB) platform. It provides an object-oriented (OO) Python model of the CIM (Common Information Model) power system data model, bidirectional translation between that OO model and protobuf messages, and SQLite persistence. The protobuf schema is defined in the sibling repository `~/git/ewb-grpc` and the generated Python protobuf stubs come from the `zepben.protobuf` PyPI package (a dependency).

## Directory Structure

```
src/zepben/ewb/
├── __init__.py                        # Top-level exports (wildcard imports in specific order)
├── util.py                            # Shared utilities (nlen, ngen, safe_remove, require, etc.)
├── dataclassy/                        # Forked from biqqles/dataclassy v0.6.2
│   ├── decorator.py                   # @dataclass decorator
│   ├── dataclass.py                   # DataClassMeta metaclass
│   └── functions.py                   # fields, values, as_dict, as_tuple, replace
├── model/
│   └── cim/                           # OO CIM model classes
│       ├── iec61970/                  # IEC 61970-301 transmission model
│       │   ├── base/
│       │   │   ├── core/              # Identifiable, Equipment, Substation, Terminal, etc.
│       │   │   ├── wires/             # AcLineSegment, Breaker, PowerTransformer, etc.
│       │   │   ├── auxiliaryequipment/
│       │   │   ├── generation/production/
│       │   │   ├── meas/
│       │   │   ├── scada/
│       │   │   ├── protection/
│       │   │   ├── equivalents/
│       │   │   └── diagramlayout/
│       │   └── infiec61970/
│       ├── iec61968/                  # IEC 61968 distribution model
│       │   ├── common/
│       │   ├── customers/
│       │   ├── assetinfo/
│       │   ├── assets/
│       │   ├── metering/
│       │   ├── operations/
│       │   └── infiec61968/
│       └── extensions/                # Zepben-specific extensions (ZBEX)
│           ├── iec61968/
│           └── iec61970/base/
├── database/
│   ├── sql/                           # SQL abstraction layer
│   │   ├── column.py                  # Column, Nullable
│   │   └── sql_table.py               # SqlTable base
│   ├── sqlite/
│   │   ├── common/
│   │   │   ├── base_cim_reader.py     # BaseCimReader - shared read helpers
│   │   │   ├── base_cim_writer.py     # BaseCimWriter - shared write helpers
│   │   │   ├── base_database_tables.py # BaseDatabaseTables - table registry
│   │   │   ├── base_entry_writer.py    # BaseEntryWriter - execute helper
│   │   │   └── reader_exceptions.py
│   │   ├── network/
│   │   │   ├── network_cim_reader.py  # NetworkCimReader (3400+ lines)
│   │   │   ├── network_cim_writer.py  # NetworkCimWriter (2700+ lines)
│   │   │   └── network_database_tables.py
│   │   ├── extensions/
│   │   │   ├── prepared_statement.py  # PreparedStatement (JVM-style)
│   │   │   └── result_set.py          # ResultSet wrapper
│   │   └── tables/                    # SQLite table definitions
│   │       ├── sqlite_table.py        # SqliteTable base
│   │       ├── iec61970/              # Matches model hierarchy
│   │       ├── iec61968/
│   │       ├── extensions/
│   │       └── associations/          # Junction tables
├── services/
│   ├── common/
│   │   ├── base_service.py            # BaseService - object registry by type+mRID
│   │   ├── reference_resolvers.py     # Reference resolver functions + BoundReferenceResolver
│   │   ├── resolver.py                # Re-exports from reference_resolvers
│   │   ├── translator/
│   │   │   ├── base_cim2proto.py      # Base CIM-to-proto functions + @bind_to_pb
│   │   │   ├── base_proto2cim.py      # Base proto-to-CIM functions + @bind_to_cim
│   │   │   └── util.py                # mrid_or_empty, int_or_none, float_or_none, etc.
│   │   └── enum_mapper.py             # EnumMapper class for enum conversion
│   ├── network/
│   │   ├── network_service.py         # NetworkService - extends BaseService
│   │   └── translator/
│   │       ├── network_cim2proto.py   # Network-specific CIM-to-proto (1983 lines)
│   │       ├── network_proto2cim.py   # Network-specific proto-to-CIM (2339 lines)
│   │       └── network_enum_mappers.py # EnumMapper instances
│   ├── customer/
│   │   ├── customers.py
│   │   ├── translator/
│   │   │   ├── customer_cim2proto.py
│   │   │   └── customer_proto2cim.py
│   │   └── customer_service_comparator.py
│   ├── diagram/
│   │   ├── diagrams.py
│   │   ├── translator/
│   │   │   ├── diagram_cim2proto.py
│   │   │   └── diagram_proto2cim.py
│   │   └── diagram_service_comparator.py
│   ├── measurement/
│   │   ├── measurements.py
│   │   ├── translator/
│   │   │   ├── measurement_cim2proto.py
│   │   │   └── measurement_proto2cim.py
│   │   └── measurement_service_comparator.py
│   └── network/
│       └── network_service_comparator.py
└── streaming/                         # gRPC streaming layer (not covered here)
```

## Key Dependencies

- **`zepben.protobuf`** (PyPI) - Generated protobuf stubs from `~/git/ewb-grpc`. Never edit these files.
- **`dataclassy`** (vendored in `src/zepben/ewb/dataclassy/`) - Forked from `biqqles/dataclassy` v0.6.2. Provides `@dataclass(slots=True)` decorator.
- **`typing_extensions`**, **`requests`**, **`PyJWT`**, **`urllib3`**

## Development Environment

### Setup

```bash
# Create and activate a virtualenv
python3 -m venv ~/.venvs/ewb-sdk
source ~/.venvs/ewb-sdk/bin/activate

# Install the SDK in editable mode with test dependencies
cd /home/hermes/git/ewb-sdk-python
pip install -e ".[test]"
```

The editable install (`-e`) means all changes to `src/` are immediately visible — no rebuild needed.

### Local Protobuf Stubs

The SDK depends on `zepben.protobuf` from PyPI, but for active development you should use the local copy generated from `~/git/ewb-grpc`:

```bash
pip uninstall -y zepben.protobuf
pip install -e ~/git/ewb-grpc/python
```

This means proto schema changes in `ewb-grpc` take effect immediately without touching PyPI. When you're ready to ship, revert to the PyPI version and bump the version in `pyproject.toml`.

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=zepben.ewb

# Run a specific test file
pytest test/cim/test_ac_line_segment.py

# Run with tox (tests against multiple Python versions)
tox
```

The `tox.ini` has `pythonpath = ./src ./test` so pytest resolves imports from the local source tree.

### Typical Data Model Change Workflow

1. Edit `.proto` files in `~/git/ewb-grpc/proto/`
2. Regenerate the Python stubs (whatever build process `ewb-grpc` uses)
3. The local `pip install -e` picks up the new stubs automatically
4. Update the Python SDK side: model classes, table definitions, reader/writer, translator functions, resolvers, exports
5. Run `pytest` to verify nothing broke
6. When done, update `zepben.protobuf` dependency version in `pyproject.toml` back to a released version

### Key Gotchas

- The `__init__.py` import order is deliberately arranged to avoid cyclic imports — don't move lines around
- Collections are `None` when empty, not `[]` — this is a hard convention throughout the codebase
- Table column `query_index` is 1-based (used by `ResultSet.get_*()` methods)
- `@bind_to_pb` and `@bind_to_cim` monkey-patch protobuf message classes as methods
- Collections use `Optional[List[Type]] | None = None` — empty means `None`, not `[]`
- `add_`, `remove_`, `clear_` methods return `self` for fluent chaining

## The CIM Model (model/cim/)

### Class Hierarchy

The OO model mirrors the CIM inheritance hierarchy. The core chain is:

```
Identifiable (mrid: str)
  └── PowerSystemResource (name, description)
        ├── ConnectivityNodeContainer
        │     └── EquipmentContainer
        │           ├── Substation, Feeder, AssetContainer, etc.
        │           └── Equipment
        │                 └── ConductingEquipment
        │                       ├── Switch
        │                       │     └── ProtectedSwitch
        │                       │           └── Breaker, Disconnector, etc.
        │                       ├── Transformer (PowerTransformer, RotatingMachine, etc.)
        │                       └── Conductor
        │                             ├── AcLineSegment
        │                             ├── Line, Jumper, etc.
        │                             └── EnergyConnection
        │                                   ├── EnergyConsumer, EnergySource
        │                                   └── EnergyConnection
        └── Equipment
              └── ...
```

Each protobuf message uses single-letter abbreviations for embedded parent classes (e.g., `io` for IdentifiedObject, `psr` for PowerSystemResource, `ec` for EquipmentContainer, `eq` for Equipment, `ce` for ConductingEquipment, `cd` for Conductor). The Python model mirrors this with actual inheritance.

### How CIM Classes Are Defined

CIM model classes use the vendored `@dataclass(slots=True)` decorator from `dataclassy`. Key conventions:

1. **Every class has `mrid: str`** inherited from `Identifiable`.

2. **Collections use nullable lists** - A field like `_normal_energized_feeders: Optional[List[Feeder]] = None` means "empty" when `None`, not when it's an empty list. This is a critical convention:
   ```python
   _cuts: list['Cut'] | None = None
   _clamps: list['Clamp'] | None = None
   _phases: list['AcLineSegmentPhase'] | None = None
   ```

3. **Collection accessors follow a strict pattern** for each collection field `_foo`:
   - `@property def foo(self) -> Generator[Foo, None, None]:` returning `ngen(self._foo)`
   - `def num_foo(self) -> int:` returning `nlen(self._foo)`
   - `def get_foo(self, mrid: str) -> Foo:` using `get_by_mrid(self._foo, mrid)`
   - `def add_foo(self, foo: Foo) -> Self:` with validation and fluent return
   - `def remove_foo(self, foo: Foo) -> Self:` using `safe_remove(self._foo, foo)`
   - `def clear_foo(self) -> Self:` setting `self._foo = None`

4. **Fluent API** - All `add_`, `remove_`, `clear_` methods return `self` for chaining.

5. **Reference validation** - Use `self._validate_reference(other, self.get_foo, "A Foo")` in `add_foo` to check for duplicates. This is defined in `Identifiable._validate_reference()`.

6. **Back-reference setting** - In `add_foo`, set the back-reference on the child:
   ```python
   if not clamp.ac_line_segment:
       clamp.ac_line_segment = self
   require(clamp.ac_line_segment is self, lambda: f"Clamp {clamp} references another AcLineSegment...")
   ```

7. **TYPE_CHECKING imports** - Import types used only in type annotations inside `if TYPE_CHECKING:` blocks to avoid circular imports.

8. **`__init__.py` files are empty stubs** - They only declare `__all__`. All model classes are exported via the top-level `src/zepben/ewb/__init__.py`.

### Adding a New CIM Class

1. Create the class file under `model/cim/<iec61970|iec61968|extensions>/<path>/<class_name>.py`
2. Inherit from the correct parent in the CIM hierarchy
3. Use `@dataclass(slots=True)` decorator
4. Define fields with type annotations and default values
5. For collections: use `Optional[List[Type]] | None = None` pattern
6. Add all accessor methods (property, num, get, add, remove, clear)
7. Add back-reference setting in `add_` methods
8. Use `@dataclass(slots=True)` with `slots=True` for memory efficiency
9. Add the export to `src/zepben/ewb/__init__.py` in the correct section

## Database Layer (database/)

### Table Definitions

Each CIM class maps to a SQLite table. Table definitions live in `database/sqlite/tables/` mirroring the model hierarchy.

**Pattern for table definitions:**

```python
class TableAcLineSegments(TableConductors):  # Inherits from parent table

    def __init__(self):
        super().__init__()
        self.per_length_impedance_mrid: Column = self._create_column("per_length_impedance_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "ac_line_segments"
```

- Tables inherit from parent tables to share columns (e.g., `TableAcLineSegments` inherits from `TableConductors` which inherits from `TableEquipment` which inherits from `TableIdentifiedObjects`)
- Each table defines `Column` objects with `(column_name, sql_type, nullable)`
- The `name` property returns the lowercase table name
- `unique_index_columns` and `non_unique_index_columns` properties define indexes
- Column `query_index` properties return 1-based indices for use in `ResultSet.get_*()` calls

### NetworkCimReader Pattern

`NetworkCimReader` extends `BaseCimReader`. Each method follows this pattern:

```python
def load_<class>(self, table: TableXxx, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
    """
    Create a <Class> and populate its fields from TableXxx.
    """
    obj = Class(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
    obj.field1 = result_set.get_string(table.field1.query_index, on_none=None)
    obj.field2 = result_set.get_int(table.field2.query_index)
    # Handle enums:
    obj.enum_field = EnumType[result_set.get_string(table.enum_field.query_index)]
    # Handle references:
    obj.parent = self._ensure_get(result_set.get_string(table.parent_mrid.query_index, on_none=None), ParentClass)
    return self._load_parent_class(obj, table, result_set) and self._add_or_throw(obj)
```

Key conventions:
- Methods take `table`, `result_set`, and `set_identifier` parameters
- Use `result_set.get_*()` with `query_index` for column access (1-based)
- Use `on_none=None` for nullable fields
- Enums are constructed from string names: `EnumType[result_set.get_string(...)]`
- References use `self._ensure_get(mrid, Type)` which returns `None` for empty mrids
- Parent class loading calls the parent's `_load_*` method and chains with `and`
- Leaf classes call `self._add_or_throw(obj)` to register with the service

### NetworkCimWriter Pattern

`NetworkCimWriter` extends `BaseCimWriter`. Two patterns exist:

**Pattern 1 - `@db_wrapper` decorator (simple cases):**

```python
@db_wrapper(TableRelayInfo)
def save_relay_info(self, relay_info: RelayInfo, table, insert) -> bool:
    # table and insert are injected by the decorator
    insert.add_value(table.field.query_index, value)
    return self._save_parent_class(table, insert, relay_info, "relay info")
```

**Pattern 2 - Direct table/insert access (complex cases):**

```python
def save_loop(self, loop: Loop) -> bool:
    table = self._database_tables.get_table(TableLoops)
    insert = self._database_tables.get_insert(TableLoops)
    # ... save associations ...
    return status and self._save_identified_object(table, insert, loop, "loop")
```

Key conventions:
- Use `insert.add_value(table.column.query_index, value)` for binding
- Use `self._mrid_or_none(obj)` for nullable references
- Parent class saving chains: `return self._save_parent(table, insert, obj, "description")`
- `_save_identified_object` handles mrid, name, description from the base class
- `_try_execute_single_update(insert, description)` executes and logs failures
- Association tables use `_save_*_association` methods with relationship type constants

### Database Tables Registry

`BaseDatabaseTables` (and `NetworkDatabaseTables`) manages table registration:
- Override `_included_tables` property to yield all tables
- Call `prepare_insert_statements(connection)` before writing
- Tables are accessed via `get_table(TableType)` and `get_insert(TableType)`
- Always call `super()._included_tables` when extending

## Translation Layer (services/common/translator/ and services/*/translator/)

### CIM-to-Proto Translation (cim2proto)

Functions are decorated with `@bind_to_pb` which attaches the function as a `to_pb` method on the protobuf message class:

```python
@bind_to_pb
def ac_line_segment_to_pb(cim: AcLineSegment) -> PBAcLineSegment:
    return PBAcLineSegment(
        cd=conductor_to_pb(cim),
        **set_or_null(
            nominalU=cim.nominal_u,
            length=cim.length,
        ),
        perLengthImpedance=per_length_impedance_to_pb(cim.per_length_impedance),
    )
```

Key conventions:
- `@bind_to_pb` is the outermost decorator (attaches to protobuf class)
- Function takes a single CIM object and returns the protobuf message
- Use `conductor_to_pb(cim)` for parent class embedding (not `cim` directly)
- Use `set_or_null(field=value)` for optional scalar fields
- Use `_map_<enum>.to_pb(cim.enum_field)` for enum conversion
- Use `mrid_or_empty(obj)` for nullable mRID references (returns "" if None)
- Use `[str(io.mrid) for io in cim.collection]` for repeated mRID references
- Use `from_nullable_float(value)` for nullable floats
- Each service has its own `*_cim2proto.py` (network, customer, diagram, measurement)

### Proto-to-CIM Translation (proto2cim)

Functions are decorated with `@bind_to_cim` (outermost) and `@add_to_service_or_none` (innermost for leaf classes):

```python
@bind_to_cim
@add_to_service_or_none
def ac_line_segment_to_cim(pb: PBAcLineSegment, service: NetworkService) -> Optional[AcLineSegment]:
    cim = AcLineSegment(mrid=pb.mrid())
    conductor_to_cim(pb.cd, cim, service)
    cim.nominal_u = get_nullable(pb, 'nominalU')
    cim.length = get_nullable(pb, 'length')
    # Handle references:
    service.resolve_or_defer_reference(resolver.per_length_impedance(cim), pb.perLengthImpedanceMRID)
    return cim
```

Key conventions:
- `@bind_to_cim` is outermost, `@add_to_service_or_none` is innermost (leaf classes only)
- Constructor takes `mrid=pb.mrid()` as the only positional arg
- Parent class: call `parent_to_cim(pb.parent_field, cim, service)` (not as constructor arg)
- Optional scalars: `get_nullable(pb, 'camelCaseFieldName')`
- Enums: `EnumType(pb.enumField)` - protobuf sends int, Python enum constructor handles it
- References: `service.resolve_or_defer_reference(resolver.<field>(cim), pb.<field>MRID)`
- Repeated mRIDs: iterate `pb.<field>MRIDs` and resolve each
- `@add_to_service_or_none` is NOT used on base/intermediate classes (only leaf classes that get added to service)
- Each service has its own `*_proto2cim.py`

### Enum Mapping

Enums are mapped in `network_enum_mappers.py` (and similar files for other services):

```python
_map_phase_code = EnumMapper(PhaseCode, PBPhaseCode)
```

Usage:
- CIM to proto: `_map_phase_code.to_pb(cim.phase_code)` - returns protobuf enum number
- Proto to CIM: `PhaseCode(pb.phaseCode)` - Python enum constructor takes the int number

### Resolver Functions

The `resolver.py` module provides factory functions for creating `BoundReferenceResolver` instances:

```python
service.resolve_or_defer_reference(resolver.per_length_impedance(cim), pb.perLengthImpedanceMRID)
```

Each resolver function takes the "from" object and returns a `BoundReferenceResolver`. The reverse resolver is included for bidirectional relationships. The resolver factory functions are defined in `reference_resolvers.py` and re-exported via `resolver.py`.

## Service Classes (BaseService / NetworkService)

### BaseService

`BaseService` is the object registry for all CIM objects. Key features:

- **Storage**: `_objects_by_type: Dict[type, Dict[str, Identifiable]]` - objects indexed by type and mRID
- **Lookup**: `service.get(mrid, Type)` - finds object by mRID, optionally filtering by type
- **Add**: `service.add(obj)` - adds object, resolves deferred references automatically
- **Contains**: `mrid in service` or `obj in service`
- **Iterate**: `service.objects(Type)` - generator over all objects of a type (includes subclasses)
- **Unresolved references**: `_unresolved_references_to` and `_unresolved_references_from` track references where the target hasn't been loaded yet. When the target is added via `service.add()`, references are automatically resolved.
- **Name types**: `service.add_name_type()` and `service.get_name_type()` manage NameType registry

### NetworkService

Extends `BaseService` with:
- **Connectivity nodes**: Auto-generated CNs via `add_connectivity_node(mrid)`. Pre-populates `_objects_by_type[ConnectivityNode]` in `__init__`.
- **Connectivity**: `connect(terminal, to)` and `connect_terminals(t1, t2)` with `ProcessStatus` return
- **Measurements**: `_measurements: Dict[str, List[Measurement]]` indexed by mRID, with `add_measurement()` and `remove_measurement()`
- **Properties**: `feeder_start_points`, `lv_feeder_start_points`, `aux_equipment_by_terminal`
- **Primary sources**: `get_primary_sources()` returns external grid EnergySources

### DiagramService

Extends `BaseService` with additional indexing for `DiagramObject`s:
- `_diagram_objects_by_diagram_mrid`: indexed by diagram mRID
- `_diagram_objects_by_identified_object_mrid`: indexed by identifiedObjectMRID
- `_diagram_object_indexes`: general index list
- `get_diagram_objects(mrid)` - returns list of DiagramObjects matching the mRID
- `add_diagram_object()` and custom `remove()` that also manage indexes

### MeasurementService (Special Case)

**MeasurementService does NOT inherit from BaseService.** It is a standalone class with its own simple list-based storage:
- `_measurements: List[MeasurementValue]`
- `add()`, `remove()`, `len_of()`, `objects()` methods
- It does NOT use the BaseService object registry, reference resolution, or name type system.
- Proto-to-CIM functions for measurements (`measurement_proto2cim.py`) call `service.add(cim)` directly rather than relying on `@add_to_service_or_none`.

## Non-Conventional Patterns (Important!)

### 1. Nullable Collections = None, Not Empty List

Collections are `None` when empty, not `[]`. Always check with `if self._foo is None` or use `nlen()` for safe length:

```python
def num_cuts(self):
    return nlen(self._cuts)  # Returns 0 if None

def clear_cuts(self):
    self._cuts = None  # NOT self._cuts = []
```

### 2. @bind_to_pb / @bind_to_cim Monkey-Patching

The `@bind_to_pb` and `@bind_to_cim` decorators attach functions to protobuf message classes as methods. This means you can call `pb_message.to_pb()` directly on a protobuf instance. Similarly, `@add_to_service_or_none` wraps the function to auto-add the result to the service.

### 3. Wildcard Imports in __init__.py

The top-level `__init__.py` uses `from module import *` in a **specific order** to prevent cyclic dependency errors. The order comment says:
> "We need to disable the IntelliJ formatter to prevent it messing with the import order of these files, several of which need to be imported in a specific order to prevent unresolved dependency errors."

When adding new exports, place them in the correct section and order.

### 4. @db_wrapper Decorator

The `@db_wrapper(TableType)` decorator injects `table` and `insert` parameters into save methods. When using it, the method signature becomes `def save_xxx(self, obj, table, insert) -> bool` even though callers only pass `obj`.

### 5. Column query_index is 1-Based

`ResultSet.get_*()` methods use 1-based indexing via `column.query_index`. This differs from Python's typical 0-based indexing. The index is set when the column is created in the table definition.

### 6. ResultSet.get_instant() Timestamp Parsing

Timestamps in the database use `Z` for UTC and may have more than 6 decimal places. The `get_instant()` method strips the `Z` and truncates to 26 characters:
```python
datetime.fromisoformat(value.rstrip('Z')[:26])
```

### 7. Enum short_name Override

Some enums (like `UnitSymbol`) override `short_name` to provide a different key for enum mapping. The `EnumMapper` uses `enum.short_name` (not `enum.name`) when extracting the key.

### 8. _validate_reference by Field

For relationships where the child stores a non-mRID field (e.g., `cut.ac_line_segment` is an object reference, not just an mRID), use `_validate_reference_by_field(other, field, getter, field_name)`.

## File Conventions

### Header

Every file starts with the MPL 2.0 license header:

```python
#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
```

Copyright year may vary per file (check when adding new files; use the current year).

### Module Exports

Every module declares `__all__ = ["ClassName1", "ClassName2", ...]` listing public exports. Private functions/classes should NOT be in `__all__`.

### Type Hints

Use `from __future__ import annotations` at the top of every file. This enables forward references without quoting. Use `TYPE_CHECKING` imports for types used only in annotations.

### Docstrings

Use Google-style docstrings with `:param`, `:return`, `:raises` tags. Match the style of existing functions in the same file.

## Protobuf Package (External)

The protobuf stubs come from the `zepben.protobuf` PyPI package, which is generated from the proto files in `~/git/ewb-grpc`. **Never edit generated protobuf files** (`*_pb2.py`). When the proto schema changes:
1. Update the proto files in `~/git/ewb-grpc`
2. Rebuild the protobuf package
3. Update the `zepben.protobuf` dependency version in `pyproject.toml`

## Adding New Code

### Adding a New CIM Class

1. Create the class in `model/cim/<path>/<class>.py`
2. Add exports to `src/zepben/ewb/__init__.py`
3. Create the table definition in `database/sqlite/tables/<path>/table_<class>.py`
4. Add table to `NetworkDatabaseTables._included_tables`
5. Add `load_<class>` to `NetworkCimReader`
6. Add `save_<class>` to `NetworkCimWriter`
7. Add `*_to_pb` function to `network_cim2proto.py`
8. Add `*_to_cim` function to `network_proto2cim.py`
9. Add enum mapper entry to `network_enum_mappers.py` if needed
10. Add resolver function to `reference_resolvers.py` if needed
11. Add resolver factory to `resolver.py` `__all__`

### Adding to a Service (Customer/Diagram/Measurement)

Follow the same pattern as network but in the corresponding `services/<service>/translator/` files. Each service has its own proto2cim/cim2proto translators that handle only the types relevant to that service.
