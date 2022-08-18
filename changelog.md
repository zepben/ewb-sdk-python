### v0.30.0

##### Breaking Changes

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

##### New Features

* Added `LvFeeder`, a branch of LV network starting at a distribution substation and continuing until the end of the LV network.

##### Enhancements

* Improved performance for bus branch creation.
* Added the following functions to be consistent with the JVM implementation:
  * `Terminal.connected_terminals`

##### Fixes

* `PhaseStepTracker` now reports strict subsets of visited phases as visited.
* Base voltages are no longer pulled from switches when creating nodes in `BusBranchNetworkCreator`

##### Notes

* None.
