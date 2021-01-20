#### Release History

| Version | Released |
| --- | --- |
|[0.21.0](#v0210)| `17 December 2020` |
|[0.20.0](#v0200)| `14 December 2020` |
|[0.19.0](#v0190)| `14 December 2020` |
|[0.18.0](#v0180)| `14 December 2020` |
|[0.17.0](#v0170)| `11 December 2020` |
|[0.16.0](#v0160)| `11 December 2020` |
|[0.15.0](#v0150)| `27 November 2020` |
|[0.14.0](#v0140)| `27 November 2020` |
|[0.13.0](#v0130)| `17 November 2020` |
|[0.12.0](#v0120)| `17 November 2020` |
|[0.11.0](#v0110)| `04 November 2020` |
|[0.10.0](#v0100)| `02 November 2020` |
|[0.9.0](#v090)| `02 November 2020` |
|[0.8.0](#v080)| `30 October 2020` |
|[0.7.0](#v070)| `30 October 2020` |
|[0.6.0](#v060)| `29 October 2020` |
| [0.5.0](#v050) | `29 October 2020` |

---

NOTE: This library is not yet stable, and breaking changes should be expected until
a 1.0.0 release.

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
