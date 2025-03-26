#### Release History

| Version          | Released            |
|------------------|---------------------|
|[0.45.0](#v0450)| `26 March 2025` |
|[0.44.0](#v0440)| `24 January 2025` |
|[0.43.1](#v0431)| `06 January 2025` |
|[0.43.0](#v0430)| `05 January 2025` |
|[0.42.0](#v0420)| `02 December 2024` |
|[0.41.2](#v0412)| `25 October 2024` |
|[0.41.1](#v0411)| `23 October 2024` |
|[0.41.0](#v0410)| `21 October 2024` |
|[0.40.0](#v0400)| `20 September 2024` |
|[0.39.0](#v0390)| `23 June 2024` |
|[0.38.0](#v0380)| `14 May 2024` |
|[0.37.4](#v0374)| `02 October 2024` |
|[0.37.3](#v0373)| `25 March 2024` |
|[0.37.2](#v0372)| `16 January 2024` |
|[0.37.1](#v0371)| `16 January 2024` |
|[0.37.0](#v0370)| `14 November 2023` |
|[0.36.0](#v0360)| `29 September 2023` |
|[0.35.0](#v0350)| `06 September 2023` |
|[0.34.0](#v0340)| `24 October 2022` |
|[0.33.0](#v0330)| `24 October 2022` |
|[0.32.0](#v0320)| `29 August 2022` |
| [0.29.0](#v0290) | `14 June 2022`      |
| [0.28.0](#v0280) | `07 June 2022`      |
| [0.27.0](#v0270) | `03 March 2022`     |
| [0.26.0](#v0260) | `07 December 2021`  |
| [0.25.0](#v0250) | `23 September 2021` |
| [0.24.0](#v0240) | `20 August 2021`    |
| [0.23.0](#v0230) | `16 August 2021`    |
| [0.22.0](#v0220) | `12 February 2021`  |
| [0.21.0](#v0210) | `17 December 2020`  |
| [0.20.0](#v0200) | `14 December 2020`  |
| [0.19.0](#v0190) | `14 December 2020`  |
| [0.18.0](#v0180) | `14 December 2020`  |
| [0.17.0](#v0170) | `11 December 2020`  |
| [0.16.0](#v0160) | `11 December 2020`  |
| [0.15.0](#v0150) | `27 November 2020`  |
| [0.14.0](#v0140) | `27 November 2020`  |
| [0.13.0](#v0130) | `17 November 2020`  |
| [0.12.0](#v0120) | `17 November 2020`  |
| [0.11.0](#v0110) | `04 November 2020`  |
| [0.10.0](#v0100) | `02 November 2020`  |
| [0.9.0](#v090)   | `02 November 2020`  |
| [0.8.0](#v080)   | `30 October 2020`   |
| [0.7.0](#v070)   | `30 October 2020`   |
| [0.6.0](#v060)   | `29 October 2020`   |
| [0.5.0](#v050)   | `29 October 2020`   |

---

NOTE: This library is not yet stable, and breaking changes should be expected until
a 1.0.0 release.

---

## [0.45.0]

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

---

## [0.44.0]

### Breaking Changes
* None.

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
* None.

### Notes
* `Cut` and `Clamp` have been added to the model, but no processing for them has been added to the tracing, so results will not be what you expect.

---

## [0.43.1]

### Fixes
* SinglePhaseKind will now be processed correctly when translating from protobuf.

---

## [0.43.0]

### Breaking Changes
* Renamed `UpdateNetworkStateClient.SetCurrentStatesRequest` to `CurrentStateEventBatch`. You will need to update any uses, but the class members are the same.
* Removed `ProcessingPaused` current state response message as this functionality won't be supported.
* `QueryNetworkStateClient.get_current_states` now returns a `CurrentStateEventBatch` rather than just the events themselves.
* `QueryNetworkStateService.on_get_current_states` must now return a stream of `CurrentStateEventBatch` rather than just the events themselves.
* `AcLineSegment.per_length_sequence_impedance` has been corrected to `per_length_impedance`. This has been done in a non-breaking way, however the public 
  resolver `Resolvers.per_length_sequence_impedance` is now `Resolvers.per_length_impedance`, correctly reflecting the CIM relationship.
* Removed `get_current_equipment_for_feeder` implementation for `NetworkConsumerClient` as its functionality is now incorporated in `get_equipment_for_container`.

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
* Updated `NetworkConsumerClient` `get_equipment_for_container/s` to allow requesting normal, current or all equipments.

### Fixes
* None.

### Notes
* None.

---

## [0.42.0]

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

---

## [0.41.2]

### Fixes
* Don't use typing_extensions for Optional import (fixes import of library on Python >3.12)

---

## [0.41.1]

### Breaking Changes
* Restrict installation to supported Python versions 3.9 -> 3.12.

---

## [0.41.0]

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

---

## [0.37.4]

### Notes
* Update to support requests up to version 3.0.0 (exclusive)
* Update to corresponding zepben.auth library for requests support

---


## [0.40.0]

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

---

## [0.39.0]

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

---

## [0.38.0]


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

---

## [0.37.0]

### Breaking Changes
* * Updated to evolve-grpc 0.26.0.

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

### Enhancements
* Update docusaurus and its configuration.

### Fixes
* None.

### Notes
* Setting PowerTransformerEnd.rated_s directly has been deprecated. You should now use `add_rating` and `get_rating` to set a `rated_s` alongside a defined 
  `TransformerCoolingType` if one is known. By default the `coolingType` will be `UNKNOWN`.

---

## [0.36.0]

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

---

## [0.35.0]


### Breaking Changes

* Renamed the module for `GrpcChannelBuilder` from `channel_builder` to `grpc_channel_builder`.
* `GrpcChannelBuilder().make_secure` now takes filenames instead of bytestrings.
  The order of the parameters has also been changed: `private_key` now comes after `certificate_chain`.
    * This changes also applies to any TLS parameters in `connect_*` functions.
* `GrpcChannelBuilder().socket_address` has been renamed to `for_address`.
* `GrpcChannelBuilder().token_fetcher` has been renamed to `with_token_fetcher`.
* Refactored `AuthTokenPlugin` to a separate module.
* Removed deprecated `connect` and `connect_async` functions. They have been replaced with several simpler functions, e.g. `connect_with_password`.
* Changed `connect_with_secret` and `connect_with_password` parameters:
    * The address of the authentication config is now specified with a single parameter: `conf_address`.
    * Added optional parameters `verify_conf` and `verify_auth`, which are passed through to `requests.get` and `requests.put`
      when fetching the authentication config and requesting access tokens respectively.
    * `ca` is replaced with `ca_filename`, which can be set to the filename of a CA to use when verifying the certificate
      of the gRPC service.
* Refactored `TreeNode` class to its own submodule: `zepben.evolve.services.network.tracing.tree.tree_node`.
* Renamed `FeederDirection.has` to `FeederDirection.__contains__`, which can be used via its operator version `in`. e.g. `BOTH.has(DOWNSTREAM)` can be replaced
  with `BOTH.__contains__(DOWNSTREAM)` or `DOWNSTREAM in BOTH`
* Removed deprecated function `NetworkConsumerClient.get_feeder`.
* Refactored the following `Switch` descendant classes to their own submodules in `zepben.evolve.model.cim.iec61970.base.wires`:
    * `Breaker` moved to `breaker`
    * `Disconnector` moved to `disconnector`
    * `Fuse` moved to `fuse`
    * `Jumper` moved to `jumper`
    * `LoadBreakSwitch` moved to `load_break_switch`
    * `ProtectedSwitch` moved to `protected_switch`
    * `Recloser` moved to `recloser`

  Note that `from zepben.evolve import <ClassName>` will still work as usual for all of the above classes.
* `DatabaseReader().load` is now an asynchronous function.
* The addition of the `mrid` and `connectivity_node_mrid` arguments to the `TestNetworkBuilder` functions has changed the position of the `action` argument. If
  you are using positional arguments you will need to add `action=` before your actions if you do not specify your own mRIDs.
* `SetDirection.run(NetworkService)` will no longer set directions for feeders with a head terminal on an open switch. It is expected these feeders are either
  placeholder feeders with no meaningful equipment, or are energised from another feeder which will set the directions from the other end.

### New Features

* Added support for current transformers and power transformers with the following classes in `zepben.evolve.cim.*`:
    * In `zepben.evolve.cim.iec61968.infiec61968.infassetinfo`:
        * `CurrentTransformerInfo`: Properties of current transformer asset.
        * `PotentialTransformerInfo`: Properties of potential transformer asset.
    * In `zepben.evolve.cim.iec61968.infiec61968.infcommon`:
        * `Ratio`: Fraction specified explicitly with a numerator and denominator, which can be used to calculate the quotient.
    * In `zepben.evolve.cim.iec61970.base.auxiliaryequipment`:
        * `CurrentTransformer`: Instrument transformer used to measure electrical qualities of the circuit that is being protected and/or monitored.
        * `PotentialTransformer`: Instrument transformer (also known as Voltage Transformer) used to measure electrical qualities of the circuit that
          is being protected and/or monitored.
        * `PotentialTransformerKind`: The construction kind of the potential transformer. (Enum)
        * `Sensor`: This class describes devices that transform a measured quantity into signals that can be presented at displays,
          used in control or be recorded.
* Added `PowerTransformer().get_end_by_terminal`, which gets a `PowerTransformerEnd` by the `Terminal` it's connected to.
* Added the following functions to `connected_equipment_trace.py` for creating traces that work on `ConductingEquipment`, and ignore phase connectivity, instead
  considering things to be connected if they share a `ConnectivityNode`:
    * `new_normal_downstream_equipment_trace`: Creates a trace that traverses in the downstream direction using the normal state of the network.
    * `new_normal_upstream_equipment_trace`: Creates a trace that traverses in the upstream direction using the normal state of the network.
    * `new_current_downstream_equipment_trace`: Creates a trace that traverses in the downstream direction using the current state of the network.
    * `new_current_upstream_equipment_trace`: Creates a trace that traverses in the upstream direction using the current state of the network.
* Added support for protection equipment with the following classes, enums, and fields:
    * `SwitchInfo`: Switch datasheet information.
    * `ProtectionEquipment`: An electrical device designed to respond to input conditions in a prescribed manner and after specified conditions are met to cause
      contact operation or similar abrupt change in associated electric control circuits, or simply to display the detected condition.
    * `CurrentRelay`: A device that checks current flow values in any direction or designated direction.
    * `CurrentRelayInfo`: Current relay datasheet information.
    * `ProtectionKind`: The kind of protection being provided by this protection equipment.
    * `ProtectedSwitch().breaking_capacity`: The maximum fault current in amps a breaking device can break safely under prescribed conditions of use.
    * `ProtectedSwitch().operated_by_protection_equipment`: The collection of `ProtectionEquipment` operating the `ProtectedSwitch`.
    * `Switch().rated_current`: The maximum continuous current carrying capacity in amps governed by the device material and construction.
      The attribute shall be a positive value.
    * `Breaker().in_transit_time`: The transition time from open to close in seconds.
* Added `getCustomersForContainer` to `CustomerConsumerClient` which allows fetching all the `Customer`s for a given `EquipmentContainer`
* Added `getDiagramObjects` to `DiagramConsumerClient` which allows fetching all the `DiagramObject`s matching a given mRID.
* `Traversal` has two new helper methods:
    * `if_not_stopping`: Adds a step action that is only called if the traversal is not stopping on the item.
    * `if_stopping`: Adds a step action that is only called if the traversal is stopping on the item.

### Enhancements

* `tracker` is now a field in `Traversal`, rather than its subclasses.
* The constructor for `BranchRecursiveTraversal` now defaults the `process_queue` field to `depth_first()`.
* `TreeNode` is now more closely aligned with its Kotlin version:
    * `TreeNode().parent` is now a read-only property.
    * `TreeNode().children` has been added as a read-only property that yields each child node.
    * `TreeNode().sort_weight` has been added as a read-only property that returns the sort weight of the node.
* All `Tracker` classes can now be copied using the `copy` method.
* Added `FeederDirection.__not__` operator function.
* Performance enhancement for `connected_equipment_trace.py` when traversing elements with single terminals.
* Added support for LV2 transformers.
* Improved logging when saving a database.
* The `TestNetworkBuilder` has been enhanced with the following features:
    * You can now set the ID's without having to create a customer 'other' creator.
    * Added Kotlin wrappers for `.fromOther` and `.toOther` that allow you to pass a class type rather than a creator. e.g. `.toOther<Fuse>()` instead
      of `.toOther(::Fuse)` or `.toOther( { Fuse(it) } )`.
    * Added inbuilt support for `PowerElectronicsConnection` and `EnergyConsumer`
    * The `to*` and `connect` functions can specify the connectivity node mRID to use. This will only be used if the terminals are not already connected.
* Added `+` and `-` operators to `PhaseCode` and `SinglePhaseKind`.

### Fixes

* `StreetDetail.to_cim` now references the protobuf -> CIM translation function for the `StreetDetail` protobuf type.
* `PerLengthImpedance.to_cim` now references the protobuf -> CIM translation function for the `PerLengthImpedance` protobuf type.
* `ZepbenTokenFetcher` now includes the refresh token in token refresh requests.
* Fixed connectivity traces.
* Fixed bug where running a limited connected equipment trace with `maximum_steps=1`
  included equipment two steps away from the starting equipment if `feeder_direction` is set.
* Each stop condition of a traversal is now checked on each step, regardless if a previous one in the internal list has returned `True`.
* Add `normal_upstream_trace`, `current_upstream_trace`, and `phase_inferrer` to `__all__` in `zepben.evolve.services.network.tracing.tracing`.
* Added missing `run` method for `DownstreamTree`.
* Added missing `TreeNodeTracker`.
* Classes in the `zepben.evolve.services.network.tracing.tree.*` submodules may now be imported `from zepben.evolve`.
* Add `normal_upstream_trace`, `current_upstream_trace`, and `phase_inferrer` to `__all__` in `zepben.evolve.services.network.tracing.tracing`.
* Stopped the NetworkConsumerClient from resolving the equipment of an EquipmentContainer when resolving references. Equipment for containers must always be
  explicitly requested by the client.
* Asking for the traced phases as a phase code when there are no nominal phases no longer throws.
* Feeder directions are now stopped at substation transformers in the same way as assigning equipment incase the feeder has no breaker, or the start point is
  not inline.

### Notes

* None.

---

## [0.34.0]

This is a re-release to ensure we're using a released version of zepben.protobuf.
There is no notable difference to 0.33.0.

---

## [0.33.0]

### Breaking Changes
* Renamed the following classes to be consistent with the JVM implementation:
  * `Traversal` to `BasicTraversal`
  * `BaseTraversal` to `Traversal`
  * `Tracker` to `BasicTracker`
  * `BaseTracker` to `Tracker`
* Renamed the following functions to be consistent with the JVM implementation:
  * `Traversal.trace` to `Traversal.run`
  * `Terminal.get_other_terminals` to `Terminal.other_terminals`
* Replaced `Equipment().current_feeders` with `Equipment().current_containers`, which yields `EquipmentContainer`'s instead `Feeder`'s.
* Changed the `AssignToFeeders` trace to stop at and exclude LV equipment, which should now be added to the new `LvFeeder` object.
* In the `services.network.tracing.tracing` module, renamed `assign_equipment_container_to_feeders` to `assign_equipment_to_feeders`.
* Database versions prior to v43 are no longer supported.

### New Features

* Added `LvFeeder`, a branch of LV network starting at a distribution substation and continuing until the end of the LV network.
* Added the following optional arguments to `NetworkConsumerClient().get_equipment(_for)_container(s)`:
  * `include_energizing_containers`: Specifies whether to include equipment from containers energizing the ones listed in
    `mrids`. This is of the enum type `IncludedEnergizingContainers`, which has three possible values:
    * `EXCLUDE_ENERGIZING_CONTAINERS`: No additional effect (default).
    * `INCLUDE_ENERGIZING_FEEDERS`: Include HV/MV feeders that power LV feeders listed in `mrids`.
    * `INCLUDE_ENERGIZING_SUBSTATIONS`: In addition to `INCLUDE_ENERGIZING_FEEDERS`, include substations that
      energize a HV/MV feeder listed in `mrids` or included via `INCLUDE_ENERGIZING_FEEDERS`.
  * `include_energized_containers`: Specifies whether to include equipment from containers energized by the ones listed in
    `mrids`. This is of the enum type `IncludedEnergizedContainers`, which has three possible values:
    * `EXCLUDE_ENERGIZED_CONTAINERS`: No additional effect (default).
    * `INCLUDE_ENERGIZED_FEEDERS`: Include HV/MV feeders powered by substations listed in `mrids`.
    * `INCLUDE_ENERGIZED_LV_FEEDERS`: In addition to `INCLUDE_ENERGIZED_FEEDERS`, include LV feeders that
      are energizes by a HV/MV feeder listed in `mrids` or included via `INCLUDE_ENERGIZED_FEEDERS`.
* Added the method `NetworkConsumerClient().get_equipment_for_containers`, which is similar to
  `NetworkConsumerClient().get_equipment_for_container` but acts on multiple containers.
* Added `FindSwerEquipment` class which can be used for finding the SWER equipment in a `NetworkService` or `Feeder`.

### Enhancements
* None.

### Fixes
* `PhaseCode.num_phases` now correctly returns the number of single phases in a phase code.
* Fixed issue where `PowerTransformer().ends` was sometimes incorrectly ordered after Protobuf-to-CIM translation.

### Notes
* None.

---

### v0.32.0

##### Breaking Changes

* Renamed the following classes to be consistent with the JVM implementation:
  * `Traversal` to `BasicTraversal`
  * `BaseTraversal` to `Traversal`
  * `Tracker` to `BasicTracker`
  * `BaseTracker` to `Tracker`
* Renamed the following functions to be consistent with the JVM implementation:
  * `Traversal.trace` to `Traversal.run`
  * `Terminal.get_other_terminals` to `Terminal.other_terminals`

##### New Features

* None

##### Enhancements

* Improved performance for bus branch creation.
* Added the following functions to be consistent with the JVM implementation:
  * `Terminal.connected_terminals`

##### Fixes

* `PhaseStepTracker` now reports strict subsets of visited phases as visited.
* Base voltages are no longer pulled from switches when creating nodes in `BusBranchNetworkCreator`

##### Notes

* None.

---

### v0.29.0

##### Breaking Changes

* None

##### New Features

* None

##### Enhancements

* Updated zepben.protobuf which includes version 1.46.3 of grpcio and grpcio-tools,
  plus version 4.21.1 of protobuf, enabling support for M1 macs and significant
  performance improvements.

##### Fixes

* None

##### Notes

* None.

---

### v0.28.0

##### Breaking Changes

* `queue_next` functions now take an item and a `Traversal`, and they now hold the responsibility of adding the next items to the traversal's queue.
* Removed `get_connectivity` and `get_connected_equipment` from `connectivity_result.py`. Use `connected_terminals` and `connected_equipment` instead.
* Moved `PhaseSelector` definition to `types.py`.

##### New Features

* Allow specification of timeout for CimConsumerClients
* Added the following traces to process a `NetworkService`, which can be accessed via the `tracing` package:
  * `SetPhases`
  * `RemovePhases`
  * `SetDirection`
  * `RemoveDirection`
  * `PhaseInferrer`
* Added new `connect_tls()` helper function for connecting to TLS secured EWB with no auth.
* Added new `connect_with_secret()` helper function for connecting to a secure EWB server with a client id and secret.

##### Enhancements

* BusBranchNetworkCreator logic updated so that the factory methods for topological_branches, equivalent_branches, and power_transformers get the topological
  nodes passed in as arguments sorted by feeder_direction.

##### Fixes

* `connect_with_password()` now works
* `SetPhases` now supports setting backwards through XN/XY transformers.
* `TestNetworkBuilder` now assigns equipment to feeders if there are any feeders present.

##### Notes

* None.

---

### v0.27.0

##### Breaking Changes
* Removed CIM gRPC producers.
* Added support for `EquivalentBranches` in `BusBranchNetworkCreator`.
* `TownDetail` fields are now nullable.
* Simplified `connect` and `connect_async` by refactoring optional settings (e.g. password authentication) to other functions.
  These functions are now deprecated.
* Use asyncio for gRPC from the newest update of `grpcio` and `grpcio-tool`.
* Renamed `PhaseDirection` to `FeederDirection`:
  * `IN` renamed to `UPSTREAM`
  * `OUT` renamed to `DOWNSTREAM`
* Separated feeder direction from phase.
  * Direction has been removed from `TracedPhases` and is now accessed directly off the `Terminal`.
  * Direction has been removed from `PhaseStatus` and is now accessed via `DirectionStatus`.
* Renamed `NetworkService.add_connectivitynode` to `NetworkService.add_connectivity_node`

##### New Features
* Implemented database module for persisting to sqlite database.
* Added `PhaseCodes`:
  - `s1`
  - `s2`
* Added `SinglePhaseKinds`:
  - `s1`
  - `s1N`
  - `s12`
  - `s12N`
  - `s2`
  - `s2N`
* Added the following CIM classes/enums:
  * `TransformerConstructionKind`
  * `TransformerFunctionKind`
  * `StreetDetail`
* Added the following `PowerTransformer` fields:
  * `construction_kind: TransformerConstructionKind`
  * `function: TransformerFunctionKind`
* Added the following `StreetAddress` fields:
  * `po_box: str`
  * `street_detail: Optional[StreetDetail]`
* Added the following `EnergySource` fields:
  * `is_external_grid: bool`
  * `r_min: Optional[float]`
  * `rn_min: Optional[float]`
  * `r0_min: Optional[float]`
  * `x_min: Optional[float]`
  * `xn_min: Optional[float]`
  * `x0_min: Optional[float]`
  * `r_max: Optional[float]`
  * `rn_max: Optional[float]`
  * `r0_max: Optional[float]`
  * `x_max: Optional[float]`
  * `xn_max: Optional[float]`
  * `x0_max: Optional[float]`
* Added `TestNetworkBuilder` which can be used to create simple test networks.

##### Enhancements
* Reworked phase connectivity to better handle unknown primary phases (X/Y).
* You can now get a `PhaseCode` representation from traced phases if it is valid.

##### Fixes
* Updated gRPC to fix support for latest LetsEncrypt certificates.

##### Notes
* None.

---

### v0.26.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.25.0

##### Breaking Changes
* Added `secure` flag to `connect()` and `connect_async()` that defaults to False. This flag needs to be True when a secure connection is required or credentials are used.

##### New Features
* Added CIM class `ShuntCompensatorInfo`

##### Enhancements
* None.

##### Fixes
* Fixed bug that would cause bus-branch creation mappings to be shared between bus-branch creation result instances.
* `connect()` and `connect_async()` will now use the OS CA bundle by default if no `ca` is specified.

##### Notes
* None.

---

### v0.24.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.23.0

##### Breaking Changes

* `Location.points` no longer provides an enumerated generator over PositionPoints.
* `NetworkHierarchy` has been updated to use CIM classes.
* `get_feeder` has been deprecated. Prefer the use of the more generic `get_equipment_container`.
* `get_identified_object` now returns a `ValueError` error if the requested object does not exist rather than a `null` successful result.
* Renamed `get_terminals_for_connectivitynode` to `get_terminals_for_connectivity_node` in `NetworkConsumerClient`.
* Renamed `value` to `objects` in `MultiObjectResult`.
* All `CimConsumerClient` implementations have been changed to control a single service rather than one per call.
* All SDK methods that retrieve objects with references will now request the network hierarchy first to provide a consistent result, regardless of call order.
* Changed `DiagramObject.style` to be a string and removed `DiagramObjectStyle` enum.
* Updated to use v0.15.0 gRPC protocols.

##### New Features

* Added the following CIM classes:
    * `BusbarSection`
    * `EquivalentBranch`
    * `EquivalentEquipment`
    * `Name`
    * `NameType`
    * `NoLoadTest`
    * `LoadBreakSwitch`
    * `OpenCircuitTest`
    * `ShortCircuitTest`
    * `TransformerEndInfo`
    * `TransformerStarImpedance`
    * `TransformerTankInfo`
    * `TransformerTest`
* Example simple bus branch network added in `zepben.evolve.examples.simple_bus_branch`.
* Helper factory methods for AcLineSegment, Junction (Bus), PowerTransformer, EnergySource, and EnergyConsumer added to `NetworkService` and available
  through `zepben.evolve.services.network.network_extensions`.
* Added utility function to generate bus-branch models from a NetworkService.
* Passing token for authorization of connection to authenticated gRPC server.
* Added API calls for getting loops.
* Added `isVirtual` and `connectionCategory` to `UsagePoint`

##### Enhancements

* [tests] cim_creators.py created with similar hypothesis derived functionality to pb_creators, and can be used to quickly build fake data for testing.
* `NetworkHierarchy` now contains circuits and loops.
* You can now pass object instances rather than just mRID's to service functions used to populate those objects (e.g. `get_equipment_for_container`).

##### Fixes

* `get_identified_objects` now adds unknown mRIDs to the failed collection.
* Fixed typing issues on all services.
* Circuits now correctly link to loops when received via gRPC.

##### Notes

* None.

---

### v0.22.0

##### Breaking Changes
* ConnectivityResult __init__ signature has slight changes to simplify use.
* Removed NetworkProtoToCim. Use NetworkService.add_from_pb directly instead.
* UUID is no longer a supported type for `IdentifiedObject.mRID`, use a string representation instead.
* `get_unresolved_reference_mrids` has now been replaced by `get_unresolved_references_from` and `get_unresolved_references_to`, which return `UnresolvedReference`s

##### New Features
* AssignToFeeders and AssociatedTerminalTrace are now available for use.
* PowerTransformerInfo class added. A PowerTransformer may have a PowerTransformerInfo as its asset_info.
* `BaseService` now has two mappings over `UnresolvedReference`, via the to_mrid and the from objects mrid, and two functions have been added: 
    - `get_unresolved_references_from(mrid)`: Allows fetching all UnresolvedReferences from `mrid`
    - `get_unresolved_references_to(mrid)`: Allows fetching all UnresolvedReferences pointing to `mrid`
* NetworkConsumerClient has 4 new functions:
    - For fetching equipment for an EquipmentContainer
            
          get_equipment_for_container(service: NetworkService, mrid: str)         
    - For fetching current equipment for a Feeder
      
          get_current_equipment_for_feeder(service: NetworkService, mrid: str)
    - For fetching equipment for an OperationalRestriction
      
          get_equipment_for_restriction(service: NetworkService, mrid: str)
    - For fetching terminals for a ConnectivityNode
      
          get_terminals_for_connectivity_node(service: NetworkService, mrid: str)
* `NetworkConsumerClient.get_feeder()` now resolves all references, and thus you can expect to receive a Feeder with all equipment and their associations populated.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.21.0

##### Breaking Changes
* Re-ordered the internal modules. If you were previously importing from something other than the top-level module (zepben.evolve), 
  it's likely these imports will no longer work. You should change all your imports to only import from zepben.evolve.

##### New Features
* Added MeasurementProducerClient for streaming measurements. Currently experimental and API will definitely change.

##### Enhancements
* Added PowerTransformerInfo class to be used as asset_info for PowerTransformers.

##### Fixes
* None.

##### Notes
* None.

---

### v0.20.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.19.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.18.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* CimProducerClient and subclasses now works as expected - error_handlers are now able to be passed in.

##### Notes
* None.

---

### v0.17.0

##### Breaking Changes

* Renamed top level package from `zepben.cimbend` to `zepben.evolve`

---

### v0.16.0

##### Breaking Changes

* connect and connect_async no longer yield a [Sync]WorkbenchConnection, which has been deprecated,
  and now yield a gRPC Channel, which can be used to create the new consumer/producer clients listed below.

##### New Features

* The gRPC api now matches evolve-sdk-jvm (with some additions). Notably, there are
  consumer clients and producer clients, and each have an asyncio compatible version
  and a synchronous version (prefixed with Sync). Each version exposes the same API.

  New consumer client classes:
  - `NetworkConsumerClient` and `SyncNetworkConsumerClient`
  - `CustomerConsumerClient` and `SyncCustomerConsumerClient`
  - `DiagramConsumerClient` and `SyncDiagramConsumerClient`

  New producer client classes:
  - `NetworkProducerClient` and `SyncNetworkProducerClient`
  - `CustomerProducerClient` and `SyncCustomerProducerClient`
  - `DiagramProducerClient` and `SyncDiagramProducerClient`
  - `ProducerClient` - A wrapper around the above 3 clients to support sending to each service simultaneously.

##### Enhancements

* Aligned with evolve-sdk-jvm.

##### Fixes

* Lots.

##### Notes

* Some tracing functionality is still missing compared to the jvm sdk.

---

### v0.15.0

##### Breaking Changes
* connect() and connect_async() now return a gRPC `Channel` rather than a [Sync]WorkbenchConnection which is now deprecated.
Instead you should use this `Channel` to create a subclass of the `CimConsumerClient` or `CimProducerClient`. (see new features).
    
##### New Features
* Consumer and Producer gRPC streaming APIs have been enhanced. All gRPC based streaming should be done through the following classes:
    - `NetworkConsumerClient`
    - `NetworkProducerClient`
    - `DiagramConsumerClient`
    - `DiagramProducerClient`
    - `CustomerConsumerClient`
    - `CustomerProducerClient`
All consumers implement `get_identified_object()` and `get_identified_objects()`
NetworkConsumerClient also has `get_network_hierarchy()`, `get_feeder()`, `retrieve_network()`. See their pydoc for more info.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.14.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.13.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.12.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.11.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.10.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.9.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.8.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.7.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.6.0

##### Breaking Changes
* None.

##### New Features
* None.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.

---

### v0.5.0

Initial github release of the evolve protobuf and gRPC definitions.
