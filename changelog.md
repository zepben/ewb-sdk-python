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
