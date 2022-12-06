## [0.35.0]

### Breaking Changes
* Renamed the module for `GrpcChannelBuilder` from `channel_builder` to `grpc_channel_builder`.
* `GrpcChannelBuilder().make_secure` now takes filenames instead of bytestrings.
  The order of the parameters has also been changed: `private_key` now comes after `certificate_chain`.
  * This changes also applies to any TLS parameters in `connect_*` functions.
* `GrpcChannelBuilder().socket_address` has been renamed to `for_address`.
* `GrpcChannelBuilder().token_fetcher` has been renamed to `with_token_fetcher`.
* Refactored `AuthTokenPlugin` to a separate module.
* Removed deprecated `connect` and `connect_async` functions. They have been replaced with several simpler functions, e.g. `connect_with_password`.
* Changed `connect_with_secret` and `connect_with_password` parameters:
  * The address of the authentication config is now specified with a single parameter: `conf_address`.
  * Added optional parameters `verify_conf` and `verify_auth`, which are passed through to `requests.get` and `requests.put`
    when fetching the authentication config and requesting access tokens respectively.
  * `ca` is replaced with `ca_filename`, which can be set to the filename of a CA to use when verifying the certificate
    of the gRPC service.

### New Features
* Added support for current transformers and power transformers with the following classes in `zepben.evolve.cim.*`:
  * In `zepben.evolve.cim.iec61968.infiec61968.infassetinfo`:
    * `CurrentTransformerInfo`: Properties of current transformer asset.
    * `PotentialTransformerInfo`: Properties of potential transformer asset.
  * In `zepben.evolve.cim.iec61968.infiec61968.infcommon`:
    * `Ratio`: Fraction specified explicitly with a numerator and denominator, which can be used to calculate the quotient.
  * In `zepben.evolve.cim.iec61970.base.auxiliaryequipment`:
    * `CurrentTransformer`: Instrument transformer used to measure electrical qualities of the circuit that is being protected and/or monitored.
    * `PotentialTransformer`: Instrument transformer (also known as Voltage Transformer) used to measure electrical qualities of the circuit that
                              is being protected and/or monitored.
    * `PotentialTransformerKind`: The construction kind of the potential transformer. (Enum)
    * `Sensor`: This class describes devices that transform a measured quantity into signals that can be presented at displays,
                used in control or be recorded.
* Added `PowerTransformer().get_end_by_terminal`, which gets a `PowerTransformerEnd` by the `Terminal` it's connected to.

### Enhancements
* None.

### Fixes
* `StreetDetail.to_cim` now references the protobuf -> CIM translation function for the `StreetDetail` protobuf type.
* `PerLengthImpedance.to_cim` now references the protobuf -> CIM translation function for the `PerLengthImpedance` protobuf type.
* `ZepbenTokenFetcher` now includes the refresh token in token refresh requests.
* Fixed connectivity traces.
* Fixed bug where running a limited connected equipment trace with `maximum_steps=1`
  included equipment two steps away from the starting equipment if `feeder_direction` is set.
* Each stop condition of a traversal is now checked on each step, regardless if a previous one in the internal list has returned `True`.

### Notes
* None.
