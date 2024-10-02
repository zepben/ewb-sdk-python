# Zepben Python SDK
## [0.37.4] - UNRELEASED
### Notes
* Update to support requests up to version 3.0.0 (exclusive)
* Update to corresponding zepben.auth library for requests support

## [0.37.3] - 2024-10-02
### Breaking Changes
* None.

### New Features
* None.

### Enhancements
* None.

### Fixes
* `PotentialTransformer` now recognised as a valid identified object type when deserializing gRPC messages.

### Notes
* None.

## [0.37.2] - 2024-03-25
### Breaking Changes
* None.

### New Features
* Added support for passing the grpc channel configuration options to the `GrpcChannelBuilder`.

### Enhancements
* None.

### Fixes
* None.

### Notes
* Default grpc channel message size is now 20MB.

## [0.37.1] - 2024-01-16
### Fixes
* Use zepben.auth 0.11.1.

## [0.37.0] - 2024-01-16
### Breaking Changes
* * Updated to evolve-grpc 0.26.0.

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
