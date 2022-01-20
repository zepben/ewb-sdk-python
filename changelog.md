### v0.27.0

##### Breaking Changes
* Removed CIM gRPC producers.
* Added support for EquivalentBranches in BusBranchNetworkCreator.

##### New Features
* Implemented database module for persisting to sqlite database.
* Added PhaseCodes:
  - s1
  - s2
* Added SinglePhaseKinds:
  - s1
  - s1N
  - s12
  - s12N
  - s2
  - s2N
* Added the following CIM classes/enums:
  * `TransformerConstructionKind`
  * `TransformerFunctionKind`
  * `StreetDetail`
* Added the following `PowerTransformer` fields:
  * `construction_kind: TransformerConstructionKind`
  * `function: TransformerFunctionKind`
* Added the following `StreetAddress` fields:
  * `po_box: str`
  * `street_detail: Optional[StreetDetail]`

##### Enhancements
* None.

##### Fixes
* Updated gRPC to fix support for latest LetsEncrypt certificates.

##### Notes
* None.
