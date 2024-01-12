# Zepben Python SDK

## [0.38.0] - UNRELEASED

### Breaking Changes

* `connect_with_secret()` and `connect_with_password()` will no longer create a `ZepbenTokenFetcher` directly from kwargs.
* `IdentifiedObject.addName` has been refactored to take in a `str` and a `NameType`. This is doing the same thing under the hood as previous `add_name()`
  function,
  but simplifies the input by lowering the amount of objects that needed to be created prior to adding names.
  Example usage change:
  `obj.add_name(nameType, "name", obj))` or `obj.add_name(nameType.getOrAddName("name", obj))` becomes `obj.add_name("name", nameType)`
* `add_name()`/`remove_name()` related function for both `IdentifiedObject` and `NameType` will now also perform the same function on the other object type.
  i.e. Removing a name from the identified object will remove it from the name type and vice versa. Same interaction is also applied to adding a name.

### New Features

* Added support for `getMetadata()` gRPC calls on `CustomerConsumerClient`, `DiagramConsumerClient`, and `NetworkConsumerClient`.
* Added support for passing the grpc channel configuration options to the `GrpcChannelBuilder`.
* Added `get_names(IdentifiedObject)` to `NameType` to retrieve all names associated with the `NameType` that belongs to an `IdentifiedObject`.
* Added `get_names(NameType)` and `get_names(String)` to `IdentifiedObject` so user can retrieve all names for a given `NameType` of the `IdentifiedObject`

### Enhancements

* `GrpcChannelBuilder` tests the connectivity of newly created channels before returning them to the user. This is done by calling `getMetadata()` against all
  known services, the channel is returned after the first successful response. Any connectivity errors will be propagated to the user. If no connectivity errors
  are encountered but no successful response is received from the known services, a `GrpcConnectionException` is thrown.

### Fixes

* `SetDirection` now traces through non-substation transformers.
* `Feeder.normal_head_terminal` can now be freely updated when the `Feeder` has no equipment assigned to it.
* `PotentialTransformer` now recognised as a valid identified object type when deserializing gRPC messages.

### Notes
<<<<<<< HEAD
* Default grpc channel message size is now 20MB.
=======

* None.
>>>>>>> c3b75b8e (Name rejig python equivalent)

## [0.37.0] - 2023-11-14

### Breaking Changes

* Updated to evolve-grpc 0.26.0.

### New Features

* PowerTransformerEnd now supports multiple ratings based on cooling types attached to the transformer. Use new `add_rating` and `get_rating` methods.
    * See notes section for deprecation information of `rated_s`.
* Added new classes:
    * TapChangerControl
    * EvChargingUnit
    * RegulatingControl
* Added new fields:
    * Equipment.commissioned_date
    * UsagePoint
        * rated_power
        * approved_inverter_capacity
    * ProtectionEquipment
        * directable
        * power_direction
    * CurrentRelayInfo.reclose_delays
    * DER register fields on PowerElectronicsConnection
* Added new enums
    * PowerDirectionKind
    * RegulatingControlModeKind
    * TransformerCoolingType
* Added support for `getMetadata()` gRPC calls on `CustomerConsumerClient`, `DiagramConsumerClient`, and `NetworkConsumerClient`.

### Enhancements

* Update docusaurus and its configuration.

### Fixes

* None.

### Notes

* Setting PowerTransformerEnd.rated_s directly has been deprecated. You should now use `add_rating` and `get_rating` to set a `rated_s` alongside a defined
  `TransformerCoolingType` if one is known. By default the `coolingType` will be `UNKNOWN`.

## [0.36.0] - 2023-09-29

### Breaking Changes

* None.

### New Features

* Support using Azure Entra ID as an auth provider
* Added support for connecting to EWB utilising Azure managed identities. Use the new function `connect_with_identity()`

### Enhancements

* None.

### Fixes

* None.

### Notes

* None.
