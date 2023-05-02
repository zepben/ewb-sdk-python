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
  * `RecloseSequence`: A reclose sequence (open and close) is defined for each possible reclosure of a breaker.
  * `ProtectionKind`: The kind of protection being provided by this protection equipment.
  * `ProtectedSwitch().breaking_capacity`: The maximum fault current in amps a breaking device can break safely under prescribed conditions of use.
  * `ProtectedSwitch().reclose_sequences`: The collection of `RecloseSequence`s attached to the `ProtectedSwitch`.
  * `ProtectedSwitch().operated_by_protection_equipment`: The collection of `ProtectionEquipment` operating the `ProtectedSwitch`.
  * `Switch().rated_current`: The maximum continuous current carrying capacity in amps governed by the device material and construction.
                            The attribute shall be a positive value.
  * `Breaker().in_transit_time`: The transition time from open to close in seconds.
* Added `getCustomersForContainer` to `CustomerConsumerClient` which allows fetching all the `Customer`s for a given `EquipmentContainer`
* Added `getDiagramObjects` to `DiagramConsumerClient` which allows fetching all the `DiagramObject`s matching a given mRID.

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
* Stopped the NetworkConsumerClient from resolving the equipment of an EquipmentContainer when resolving references. Equipment for containers must always be explicitly requested by the client.

### Notes

* None.
