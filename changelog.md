### v0.33.0

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
* Added the following optional arguments to `NetworkConsumerClient().get_equipment_for_container`:
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

##### Enhancements
* None.

##### Fixes
* `PhaseCode.num_phases` now correctly returns the number of single phases in a phase code.

##### Notes
* None.
