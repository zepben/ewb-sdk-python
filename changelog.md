# Zepben Python SDK
## [0.48.0] - UNRELEASED
### Breaking Changes
* Updated to new Tracing API. All old traces will need to be re-written with the new API.
* `AcLineSegment` supports adding a maximum of 2 terminals. Mid-span terminals are no longer supported and models should migrate to using `Clamp`.
* `Clamp` supports only adding a single terminal.
* `FeederDirectionStateOperations` have been reworked to take `NetworkStateOperators` as a parameter.
* `RemoveDirection` has been removed. It did not work reliably with dual fed networks with loops. You now need to clear direction using the new `ClearDirection`
  and reapply directions where appropriate using `SetDirection`.
* `Cut` supports adding a maximum of 2 terminals.
* `NetworkTraceTracker` now uses a `set` to track visited objects, if you were using unhashable objects this will need to be addressed.
* Added a new `debug_logging` and `name` parameters to the constructor of the following traces. The helper functions in `Tracing` also have these parameters,
  which defaults to `None` and `network_trace`, meaning anyone using these wrappers will be unaffected by the change:
  * `AssignToFeeders`
  * `AssignToLvFeeders`
  * `ClearDirection`
  * `FindSwerEquipment`
  * `PhaseInferrer`
  * `RemovePhases`
  * `SetDirection`
  * `SetPhases`
* `NetworkStateOperators` has a new abstract `description`. If you are creating custom operators you will need to add it.

### New Features
* Added `ClearDirection` that clears feeder directions.

### Enhancements
* Tracing models with `Cut` and `Clamp` are now supported via the new tracing API.
* Added support to `TestNetworkBuilder` for:
  * `with_clamp` - Adds a clamp to the previously added `AcLineSegment`
  * `with_cut` - Adds a cut to the previously added `AcLineSegment`
  * `connect_to` - Connects the previously added item, rather than having to specify it again in `connect`.
  * You can now add sites to the `TestNetworkBuilder` via `addSite`.
  * You can now add busbar sections natively with `from_busbar_section` and `to_busbar_section`
  * The prefix for generated mRIDs for "other" equipment can be specified with the `default_mrid_prefix` argument in `from_other` and `to_other`.
* When processing feeder assignments, all LV feeders belonging to a dist substation site will now be considered energized when the site is energized by a
  feeder.

### Fixes
* When finding `LvFeeders` in the `Site` we will now exclude `LvFeeders` that start with an open `Switch`
* `AssignToFeeder` and `AssignToLvFeeder` will no longer trace from start terminals that belong to open switches
* The follow fixes were added to Traversal and NetworkTrace:
  * `can_stop_on_start_item` now works for branching traversals.
  * Traversal start items are added to the queue before traversal starts, so that the start items honour the queue type order.
  * Stop conditions on the `NetworkTrace` now are checked based on a step type, like `QueueCondition` does, rather than by checking `can_action_item`.
  * `Cut` and `Clamp` are now correctly supported in `SetDirection` and `DirectionCondition`.
  * `NetworkTrace` now handles starting on `Cut` , `Clamp`, and `AcLineSegment` and their terminals in a explicit / sensible way.
  * `NetworkTracePathProvider` now correctly handles next paths when starting on a `Clamp` terminal.
* `NetworkTrace`/`Traversal` now correctly respects `can_stop_on_start_item` when providing multiple start items.
* `AssignToFeeders`/`AssignToLvFeeders` now finds back-fed equipment correctly
* `AssignToFeeders` and `AssignToLvFeeders` will now associate `PowerElectronicUnits` with their `powerElectronicsConnection` `Feeder`/`LvFeeder`.

### Notes
* None.

## [0.47.1] - 2025-05-14
### Fixes
* Only resolve PowerSystemResource -> Asset relationship in one direction when calling `get_equipment_container` to stop deadlock.
* MultiObjectResult now exposes result types inheriting from IdentifiedObject to allow better type completion

## [0.47.0] - 2025-05-08
### Fixes
* Downgrade protobuf and gRPC deps to fix SyncNetworkConsumerClient

## [0.46.0] - 2025-04-24
### Breaking Changes
* None.

### New Features
* Added relationships between `Asset` and `PowerSystemResource` which enables linking `Equipment` to `Pole`:
  * `Asset.powerSystemResources`
  * `PowerSystemResource.assets`

### Enhancements
* None.

### Fixes
* None.

### Notes
* None.

## [0.45.0] - 2025-03-27
### Breaking Changes
* None.

### New Features
* Added support for the following `CurrentStateEvent` types:
  * `AddCutEvent`.
  * `RemoveCutEvent`.
  * `AddJumperEvent`.
  * `RemoveJumperEvent`.

### Enhancements
* `QueryNetworkStateClient.reportBatchStatus` can be used to send status responses for batches returned from the service via
  `QueryNetworkStateClient.getCurrentStates`.

### Fixes
* Specify typing_extensions as a dependency to fix support for Python 3.9 and 3.10

### Notes
* None.

## [0.44.0] - 2025-01-24
### Breaking Changes
* `GrpcChannelBuilder.build()` now accepts a `timeout_seconds` argument. This is the timeout used for each connection attempt so the total amount of time the
  connection test may take to fail can be greater than `timeout_seconds`.

### New Features
* Added the following new CIM classes:
  * `Clamp`: A Clamp is a galvanic connection at a line segment where other equipment is connected. A Clamp does not cut the line segment. A Clamp is
    ConductingEquipment and has one Terminal with an associated ConnectivityNode. Any other ConductingEquipment can be connected to the Clamp ConnectivityNode.
    __NOT CURRENTLY FULLY SUPPORTED BY TRACING__
  * `Cut`: A cut separates a line segment into two parts. The cut appears as a switch inserted between these two parts and connects them together. As the cut is
    normally open there is no galvanic connection between the two line segment parts. But it is possible to close the cut to get galvanic connection. The cut
    terminals are oriented towards the line segment terminals with the same sequence number. Hence the cut terminal with sequence number equal to 1 is oriented
    to the line segment's terminal with sequence number equal to 1. The cut terminals also act as connection points for jumpers and other equipment, e.g. a
    mobile generator. To enable this, connectivity nodes are placed at the cut terminals. Once the connectivity nodes are in place any conducting equipment can
    be connected at them.
    __NOT CURRENTLY FULLY SUPPORTED BY TRACING__
* Added FeederDirection.CONNECTOR, to be used by BusbarSections for their direction to differentiate from BOTH.

### Enhancements
* Updated `NetworkConsumerClient`'s `get_equipment_for_container/s`,  `get_equipment_container`, `get_equipment_for_loop` and `get_all_loops`
  to allow requesting normal, current or all equipments.

### Fixes
* GrpcChannelBuilder's initial connectivity test no longer fails due to a lack of permissions on a subset of services.

### Notes
* `Cut` and `Clamp` have been added to the model, but no processing for them has been added to the tracing, so results will not be what you expect.

## [0.43.1] - 2025-01-06
### Fixes
* SinglePhaseKind will now be processed correctly when translating from protobuf.

## [0.43.0] - 2025-01-05
### Breaking Changes
* Renamed `UpdateNetworkStateClient.SetCurrentStatesRequest` to `CurrentStateEventBatch`. You will need to update any uses, but the class members are the same.
* Removed `ProcessingPaused` current state response message as this functionality won't be supported.
* `QueryNetworkStateClient.get_current_states` now returns a `CurrentStateEventBatch` rather than just the events themselves.
* `QueryNetworkStateService.on_get_current_states` must now return a stream of `CurrentStateEventBatch` rather than just the events themselves.
* `AcLineSegment.per_length_sequence_impedance` has been corrected to `per_length_impedance`. This has been done in a non-breaking way, however the public
  resolver `Resolvers.per_length_sequence_impedance` is now `Resolvers.per_length_impedance`, correctly reflecting the CIM relationship.
* Removed `get_current_equipment_for_feeder` implementation for `NetworkConsumerClient` as its functionality is now incorporated in
  `get_equipment_for_container`.

### New Features
* Added `BatchNotProcessed` current state response. This is used to indicate a batch has been ignored, rather than just returning a `BatchSuccessful`.
* `QueryNetworkStateService` now supports `reportBatchStatus`, which requires two new constructor callbacks:
  * `on_current_states_status` - A callback triggered when the response status of an event returned via `on_get_current_states` is received from the client.
  * `on_processing_error` - A function that takes a message and optional cause. Called when `on_current_states_status` raises an exception, or the
    `SetCurrentStatesResponse` is for an unknown event status.
* Added `PanDemandResponseFunction`, a new class which contains `EndDeviceFunctionKind` and the identity of the `ControlledAppliance` of this function.
* Added `BatteryControl`, a new class which describes behaviour specific to controlling a `BatteryUnit`.
* Added `StaticVarCompensator` a new class representing a facility for providing variable and controllable shunt reactive power.
* Added `ControlledAppliance` a new class representing the identity of the appliance controlled by a specific `EndDeviceFunction`.
* Added `PerLengthPhaseImpedance` a new class used for representing the impedance of individual wires on an AcLineSegment.
* Added `PhaseImpedanceData` a data class with a link to `PerLengthPhaseImpedance`, for capturing the phase impedance data of an individual wire.
* Added new enums:
  * `BatteryControlMode`
  * `EndDeviceFunctionKind`
  * `SVCControlMode`

### Enhancements
* All `StateEventFailure` classes now have a `message` included to give more context to the error.
* Added `ct_primary` and `min_target_deadband` to `RegulatingContrl`.
* Added collection of `BatteryControl` to `BatteryUnit`
* Added collection of `EndDeviceFunctionKind` to `EndDevice`
* Added an unordered collection comparator.
* Added the energized relationship for the current state of network between `Feeder` and `LvFeeder`.

### Fixes
* None.

### Notes
* None.

## [0.42.0] - 2024-12-02
### Breaking Changes
* Database readers and writes for each `BaseService` no longer accept a `MetadataCollection`, and will instead use the collection of the provided service.
* `BaseService` and `MetadataCollection` are no longer dataclassy dataclasses. This will only affect you if you were making use of the auto generated
  constructors to pass initial values (which didn't always work as expected anyway)
* Network state services for updating and querying network state events via gRPC.
* Client functionality for updating and querying network states via gRPC service stub.

### New Features
* `BaseService` now contains a `MetadataCollection` to tightly couple the metadata to the associated service.
* Added `Services`, a new class which contains a copy of each `BaseService` supported by the SDK.
* Added a new connection method `connect_with_token` which allows you to connect to the EWB using an access token.

### Enhancements
* None.

### Fixes
* None.

### Notes
* None.

## [0.41.2] - 2024-12-02
### Fixes
* Don't use typing_extensions for Optional import (fixes import of library on Python >3.12)

## [0.41.1] - 2024-10-23
### Breaking Changes
* Restrict installation to supported Python versions 3.9 -> 3.12.

## [0.41.0] - 2024-10-21
### Breaking Changes
* None.

### New Features
* Data Model change:
  * Add `phaseCode` variable to `UsagePoint`
  * Added new classes:
    * `Curve`
    * `CurveData`
    * `EarthFaultCompensator`
    * `GroundingImpedance`
    * `PetersenCoil`
    * `ReactiveCapabilityCurve`
    * `RotatingMachine`
    * `SynchronousMachine`
* Added `designTemperature` and `designRating` to `Conductor` to capture limitations in the conductor based on the network design and physical surrounds of the
  conductor.
* Added `specialNeed` to `Customer` to capture any special needs of the customer, e.g. life support.

### Enhancements
* None.

### Fixes
* None.

### Notes
* None.

## [0.37.4] - 2024-10-02
### Notes
* Update to support requests up to version 3.0.0 (exclusive)
* Update to corresponding zepben.auth library for requests support

## [0.40.0] - 2024-09-20
### Breaking Changes
* The database has been split into three databases, which will change the imports of most related classes:
  1. The existing database containing the network model (`*-network-model.sqlite`) with classes in the `network` package.
  2. A new database containing the customer information (`*-customers.sqlite`) with classes in the `customer` package.
  3. A new database containing the diagrams (`*-diagrams.sqlite`) with classes in the `diagram` package.
* The database split has resulted in the database classes also being split, e.g. `DatabaseReader` is now `NetworkDatabaseReader`, `CustomerDatabaseReader` and `
  DiagramDatabaseReader`.
* Database table classes now return a `Generator` rather than a `List` or their index collections. This will have no impact if you are just looping over the
  result, but it will have an impact if you have inherited your own tables.
* `Equipment` to `EquipmentContainer` links for LV feeders are no longer written to the database, they should never have been.
* Converted the following classes to use `@dataclass` from `dataclasses` instead of `dataclassy`:
  * `PositionPoint`
  * `TownDetail`
  * `StreetDetail`
  * `StreetAddress`
  * `Name`
  * `DiagramObjectPoint`
  * `RelaySetting`
  * `TransformerEndRatedS`
  * `ResistanceReactance`
  * `DataSource`
* All private collections inside our CIM objects that index objects by mrid now raise `KeyError` rather than `ValueError` if you try and remove an object from
  an empty collection.
* Rationalised accessors for the private collections inside our CIM objects, which has added and/or removed some functions. If you were using one of the removed
  functions, there should be another that can give close/equivalent operation. The most notable change is the accessors should now be throwing exceptions
  correctly, rather than returning `None` in some circumstances and throwing in others.
  * `Location`:
    * `get_point` now throws when provided an invalid `sequence_number` rather than returning `None`.
    * Updated error message for providing an incorrect `sequence_number` to `insert_point`.
  * `RelayInfo`:
    * `get_delay` and `remove_delay_at` now throw when provided an invalid `index` rather than returning `None`.
    * Updated error message for providing an incorrect `index` to `add_delay`.
  * `Sensor`:
    * Type information for `get_relay_function` has been updated to indicate the return value is not optional, as the function throws if the `mrid` is unknown.
  * `ConductingEquipment`:
    * Updated error message for providing a `Terminal` with an incorrect `sequence_number` to `add_terminal`.
  * `IdentifiedObject`:
    * `get_name` now throws when provided an invalid `name_type` or `name` rather than returning `None`.
    * `get_names` now throws when provided an invalid `name_type` rather than returning `None` if it had no names, or an `EmptyList` if it had names, but none
      of the requested type.
  * `DiagramObject`:
    * Updated error message for providing an incorrect `sequence_number` to `insert_point`.
  * `ProtectionRelayFunction`:
    * Updated error message for providing an incorrect `sequence_number` to `add_threshold`.
    * Type information for `get_threshold` has been updated to indicate the return value is not optional, as the function throws if the `sequence_number` is
      unknown.
    * Type information for `remove_threshold` has been updated to indicate the `threshold` to remove is not optional.
    * Updated error message for providing an incorrect `index` to `add_time_limit`.
    * `remove_time_limit_by_time_limit` was renamed to `remove_time_limit`.
    * `remove_time_limit` was renamed to `remove_time_limit_at` and now throws when provided an invalid `index` rather than returning `None`.
    * Type information for the following functions have been updated to indicate the return value is not optional, as the functions throw if the `mrid` is
      unknown:
      * `get_sensor`
      * `get_protected_switch`
      * `get_scheme`
  * `ProtectionRelayScheme`:
    * Type information for `get_function` has been updated to indicate the return value is not optional, as the function throws if the `mrid` is unknown.
  * `ProtectionRelaySystem`:
    * Type information for `get_scheme` has been updated to indicate the return value is not optional, as the function throws if the `mrid` is unknown.
  * `PowerTransformerEnd`:
    * Updated error message for providing a `PowerTransformerEnd` with an incorrect `end_number` to `add_end`.
    * `get_rating_by_rated_s` has been removed.
    * `get_rating_by_cooling_type` has been renamed to `get_rating` and now throws when provided an invalid `cooling_type` rather than returning `None`.
    * The parameters for `add_rating` have been reordered, and `cooling_type` now defaults to `UNKNOWN_COOLING_TYPE`.
    * `add_transformer_end_rated_s` now takes a copy of the provided `transformer_end_rated_s` rather than adding the object directly into the collection.
    * `remove_rating_by_cooling_type` now throws when provided an invalid `cooling_type` rather than returning `None`.
  * `ProtectedSwitch`:
    * Type information for `get_relay_function` has been updated to indicate the return value is not optional, as the function throws if the `mrid` is unknown.
  * `RegulatingControl`:
    * Type information for `get_regulating_cond_eq` has been updated to indicate the return value is not optional, as the function throws if the `mrid` is
      unknown.

### New Features
* Support zepben.auth 0.12.0 which brings support for auth against EWB servers backed by EntraID.

### Enhancements
* Added the following accessors/helpers to our CIM objects:
  * `Location.for_each_point`
  * `RelayInfo.for_each_point`
  * `IdentifiedObject.has_name`
  * `DiagramObject.for_each_point`
  * `DiagramObject.remove_point_by_sequence_number`
  * `ProtectionRelayFunction.for_each_threshold`
  * `ProtectionRelayFunction.remove_threshold_at`
  * `ProtectionRelayFunction.for_each_time_limit`
* Added missing `num_controls` field to `PowerSystemResource`.

### Fixes
* Added missing type information to the following `NameType` functions: `get_or_add_name`, `remove_name` and `remove_names`

### Notes
* Updated to support zepben.protobuf 0.27.0. This has actually been supported since 0.38.0, however the released version was not captured in the dependencies.

## [0.39.0] - 2024-06-24
### Breaking Changes
* None.

### New Features
* Added `EwbDataFilePaths` class for working with the EWB various database files

### Enhancements
* Added feature list to documentation.

### Fixes
* Updated zepben.auth to 0.11.1 to fix incorrect audience processing when requesting tokens with Entra.

### Notes
* None.


## [0.38.0] - 2024-05-14

### Breaking Changes

* This is the last release using an artifact name of `zepben.evolve`, future releases will be made as `zepben.ewb`.
* `connect_with_secret()` and `connect_with_password()` will no longer create a `ZepbenTokenFetcher` directly from kwargs.
* `IdentifiedObject.addName` has been refactored to take in a `str` and a `NameType`. This is doing the same thing under the hood as previous `add_name()`
  function,
  but simplifies the input by lowering the amount of objects that needed to be created prior to adding names.
  Example usage change:
  `obj.add_name(nameType, "name", obj))` or `obj.add_name(nameType.getOrAddName("name", obj))` becomes `obj.add_name("name", nameType)`
* `add_name()`/`remove_name()` related function for both `IdentifiedObject` and `NameType` will now also perform the same function on the other object type.
  i.e. Removing a name from the identified object will remove it from the name type and vice versa. Same interaction is also applied to adding a name.
* Removed `ProtectionEquipment`.
* Change of inheritance: `CurrentRelay` &rarr; `ProtectionEquipment`.
  becomes `CurrentRelay` &rarr; `ProtectionRelayFunction`.
* Removed symmetric relation `ProtectionEquipment` &harr; `ProtectedSwitch`.
* Renamed `CurrentRelayInfo` to `RelayInfo`.
  * The override `CurrentRelay.relay_info` has been moved from `CurrentRelay` to its new parent class, `ProtectionRelayFunction`.
  * Renamed `RelayInfo.remove_delay` to `RelayInfo.remove_delay_at`. The original method name has been repurposed to remove a delay by its value rather than its
    index.
* Reworked values for enumerable type `ProtectionKind`.

### New Features

* Added support for passing the grpc channel configuration options to the `GrpcChannelBuilder`.
* Added `get_names(IdentifiedObject)` to `NameType` to retrieve all names associated with the `NameType` that belongs to an `IdentifiedObject`.
* Added `get_names(NameType)` and `get_names(String)` to `IdentifiedObject` so user can retrieve all names for a given `NameType` of the `IdentifiedObject`
* Added new classes and fields to support advanced modelling of protection relays:
  * `SeriesCompensator`: A series capacitor or reactor or an AC transmission line without charging susceptance.
  * `Ground`: A point where the system is grounded used for connecting conducting equipment to ground.
  * `GroundDisconnector`: A manually operated or motor operated mechanical switching device used for isolating a circuit
    or equipment from ground.
  * `ProtectionRelayScheme`: A scheme that a group of relay functions implement. For example, typically schemes are
    primary and secondary, or main and failsafe.
  * `ProtectionRelayFunction`: A function that a relay implements to protect equipment.
  * `ProtectionRelaySystem`: A relay system for controlling `ProtectedSwitch`es.
  * `RelaySetting`: The threshold settings for a given relay.
  * `VoltageRelay`: A device that detects when the voltage in an AC circuit reaches a preset voltage.
  * `DistanceRelay`: A protective device used in power systems that measures the impedance of a transmission line to
    determine the distance to a fault, and initiates circuit breaker tripping to isolate the faulty
    section and safeguard the power system.
  * `RelayInfo.reclose_fast`: True if reclose_delays are associated with a fast Curve, False otherwise.
  * `RegulatingControl.rated_current`: The rated current of associated CT in amps for a RegulatingControl.

### Enhancements

* `GrpcChannelBuilder` tests the connectivity of newly created channels before returning them to the user. This is done by calling `getMetadata()` against all
  known services, the channel is returned after the first successful response. Any connectivity errors will be propagated to the user. If no connectivity errors
  are encountered but no successful response is received from the known services, a `GrpcConnectionException` is thrown.

### Fixes

* `SetDirection` now traces through non-substation transformers.
* `Feeder.normal_head_terminal` can now be freely updated when the `Feeder` has no equipment assigned to it.
* `PotentialTransformer` now recognised as a valid identified object type when deserializing gRPC messages.

### Notes

* Default grpc channel message size is now 20MB.

## [0.37.0] - 2023-11-14

### Breaking Changes

* Updated to evolve-grpc 0.26.0.

### New Features

* PowerTransformerEnd now supports multiple ratings based on cooling types attached to the transformer. Use new `add_rating` and `get_rating` methods.
  * See notes section for deprecation information of `rated_s`.
* Added new classes:
  * TapChangerControl
  * EvChargingUnit
  * RegulatingControl
* Added new fields:
  * Equipment.commissioned_date
  * UsagePoint
    * rated_power
    * approved_inverter_capacity
  * ProtectionEquipment
    * directable
    * power_direction
  * CurrentRelayInfo.reclose_delays
  * DER register fields on PowerElectronicsConnection
* Added new enums
  * PowerDirectionKind
  * RegulatingControlModeKind
  * TransformerCoolingType
* Added support for `getMetadata()` gRPC calls on `CustomerConsumerClient`, `DiagramConsumerClient`, and `NetworkConsumerClient`.

### Enhancements

* Update docusaurus and its configuration.

### Fixes

* None.

### Notes

* Setting PowerTransformerEnd.rated_s directly has been deprecated. You should now use `add_rating` and `get_rating` to set a `rated_s` alongside a defined
  `TransformerCoolingType` if one is known. By default the `coolingType` will be `UNKNOWN`.

## [0.36.0] - 2023-09-29

### Breaking Changes

* None.

### New Features

* Support using Azure Entra ID as an auth provider
* Added support for connecting to EWB utilising Azure managed identities. Use the new function `connect_with_identity()`

### Enhancements

* None.

### Fixes

* None.

### Notes

* None.
