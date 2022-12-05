## [0.35.0]

### Breaking Changes
* None.

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

### Notes
* None.
