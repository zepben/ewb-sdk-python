##### Breaking Changes

* `queue_next` functions now take an item and a `Traversal`, and they now hold the responsibility of adding the next items to the traversal's queue.
* Removed `get_connectivity` and `get_connected_equipment` from `connectivity_result.py`. Use `connected_terminals` and `connected_equipment` instead.
* Moved `PhaseSelector` definition to `types.py`.

##### New Features

* Allow specification of timeout for CimConsumerClients
* Added convenience classes `SetPhases` and `RemovePhases` to set and remove phases on a `NetworkService`.
* Added new `connect_tls()` helper function for connecting to TLS secured EWB with no auth.
* Added new `connect_with_secret()` helper function for connecting to a secure EWB server with a client id and secret.
* Added convenience classes `SetDirection` and `RemoveDirection` to set and remove feeder directions on a `NetworkService`.

##### Enhancements

* BusBranchNetworkCreator logic updated so that the factory methods for topological_branches, equivalent_branches, and power_transformers get the topological
  nodes passed in as arguments sorted by feeder_direction.

##### Fixes

* `connect_with_password()` now works
* `SetPhases` now supports setting backwards through XN/XY transformers.

##### Notes

* None.
