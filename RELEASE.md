#### Release History

| Version | Released |
| --- | --- |
|[0.17.0](#v0170)| `11 December 2020` |
|[0.16.0](#v0160)| `11 December 2020` |

---

NOTE: This library is not yet stable, and breaking changes should be expected until a 1.0.0 release.

---

### v0.17.0

##### Breaking Changes

* Renamed top level package from `zepben.cimbend` to `zepben.evolve`

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

