### v0.25.0

##### Breaking Changes
* Added `secure` flag to `connect()` and `connect_async()` that defaults to False. This flag needs to be True when a secure connection is required or credentials are used.

##### New Features
* Added CIM class `ShuntCompensatorInfo`

##### Enhancements
* None.

##### Fixes
* Fixed bug that would cause bus-branch creation mappings to be shared between bus-branch creation result instances.
* `connect()` and `connect_async()` will now use the OS CA bundle by default if no `ca` is specified.

##### Notes
* None.
