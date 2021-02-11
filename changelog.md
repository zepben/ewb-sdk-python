### v0.22.0

##### Breaking Changes
* ConnectivityResult __init__ signature has slight changes to simplify use.
* Removed NetworkProtoToCim. Use NetworkService.add_from_pb directly instead.
* UUID is no longer a supported type for `IdentifiedObject.mRID`, use a string representation instead.
* `get_unresolved_reference_mrids` has now been replaced by `get_unresolved_references_from` and `get_unresolved_references_to`, which return `UnresolvedReference`s

##### New Features
* AssignToFeeders and AssociatedTerminalTrace are now available for use.
* PowerTransformerInfo class added. A PowerTransformer may have a PowerTransformerInfo as its asset_info.
* `BaseService` now has two mappings over `UnresolvedReference`, via the to_mrid and the from objects mrid, and two functions have been added: 
    - `get_unresolved_references_from(mrid)`: Allows fetching all UnresolvedReferences from `mrid`
    - `get_unresolved_references_to(mrid)`: Allows fetching all UnresolvedReferences pointing to `mrid`
* NetworkConsumerClient has 4 new functions:
    - For fetching equipment for an EquipmentContainer
            
          get_equipment_for_container(service: NetworkService, mrid: str)         
    - For fetching current equipment for a Feeder
      
          get_current_equipment_for_feeder(service: NetworkService, mrid: str)
    - For fetching equipment for an OperationalRestriction
      
          get_equipment_for_restriction(service: NetworkService, mrid: str)
    - For fetching terminals for a ConnectivityNode
      
          get_terminals_for_connectivitynode(service: NetworkService, mrid: str)
* `NetworkConsumerClient.get_feeder()` now resolves all references, and thus you can expect to receive a Feeder with all equipment and their associations populated.

##### Enhancements
* None.

##### Fixes
* None.

##### Notes
* None.
