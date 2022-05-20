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
* `SetDirection` now correctly checks for feeders head terminals.
* `TestNetworkBuilder` now assigns equipment to feeders if there are any feeders present.

##### Notes

* None.
