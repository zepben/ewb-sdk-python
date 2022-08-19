### v0.30.0

##### Breaking Changes

* Renamed the following classes to be consistent with the JVM implementation:
  * `Traversal` to `BasicTraversal`
  * `BaseTraversal` to `Traversal`
  * `Tracker` to `BasicTracker`
  * `BaseTracker` to `Tracker`
* Renamed the following functions to be consistent with the JVM implementation:
  * `Traversal.trace` to `Traversal.run`

##### New Features

* None

##### Enhancements

* Improved performance for bus branch creation.

##### Fixes

* `PhaseStepTracker` now reports strict subsets of visited phases as visited.
* Base voltages are no longer pulled from switches when creating nodes in `BusBranchNetworkCreator`

##### Notes

* None.
