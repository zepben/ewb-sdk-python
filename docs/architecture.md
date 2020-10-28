# Architecture #
cimbend provides a Common Information Model profile that can be used with Zepben's services. 
Aside from the model the library also provides the concept of a NetworkService that can be used with the model for storing and processing electricity networks.

This document describes design decisions related to the network and functionality built on top of it, and interacting with the network via the CIM model.

# Adding to the network #
Clients can create a network and add CIM objects to the network via the `BaseService.add` and `BaseService.add_from_pb` method. 
This is the only supported way to add objects to the network, and requires a protobuf message attributed to one of the maps in the destined service or the 
corresponding `zepben.cimbend` type. In normal cases you should be building your network directly from Zepben's services, which will always provide protobuf 
objects and do all the heavy lifting for you. 

Classes extending `BaseService` have been designed as write-once classes. If you re-add an object that already exists in the network, the existing object will 
always be overwritten. Objects are still mutable despite this, so when updates are made from an external source, it is intended that overwrites are not 
performed and instead specific fields are updated through API calls.

# Construction and verification #
## Using protobuf helpers ##
When utilising a `BaseService` type and calling `add` with protobuf messages, the `from_pb` function will be called, which will convert all underlying fields to `zepben.model` CIM classes before adding it to the network. As part of this any field that references another object in the network (i.e, a field taking an MRID) will be retrieved from the network if the field is set. If the field is set and the retrieval fails, `from_pb` will throw an exception. However, if the field is not set, it will be ignored and the added object will have no reference to the underlying field. Keep this in mind when building your network, as this will determine what attributes are available for your object, and you can expect AttributeError's to be raised when you haven't set all fields appropriately.

# Weak references #
`ConnectivityNode`'s are always referenced weakly from `Terminal` to stop a single piece of equipment keeping the entire network in memory through the `ConnectivityNode`'s terminals.

