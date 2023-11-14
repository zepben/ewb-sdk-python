#### Release History

| Version          | Released            |
|------------------|---------------------|
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
