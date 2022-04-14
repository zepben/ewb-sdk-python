##### Breaking Changes
* `queue_next` functions now take an item and a `Traversal`, and they now hold the responsibility of adding the next items to the traversal's queue.

##### New Features
* Allow specification of timeout for CimConsumerClients
* Added convenience classes `SetPhases` and `RemovePhases` to set and remove phases on a `NetworkService`.
* Added new connect_tls helper function for connecting to TLS secured EWB with no auth.

##### Enhancements
* None.

##### Fixes
* `connect_with_password()` now works

##### Notes
* None.
