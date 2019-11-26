# Zepben cimbend (WIP) #
This library provides Zepben's CIM profile as a python module for simplified interaction with Zepben services. You can find an overview and diagrams of Zepben's profile [here](https://zepben.bitbucket.io/docs/cim/zepben/).

All classes exposed in `zepben.model` can be converted into protobuf messages and sent to/received from Zepben's gRPC services.

Note this project is still a work in progress and intended for development use only, and thus should be considered unstable. however the framework of `zepben.model` should mostly stay the same.

More extensive documentation can be found in the [docs](docs/README.md)

# Basic Usage #

## Installation ##
Requirements:
    Python 3.7+

This library depends on protobuf and gRPC for messaging. To set up for developing against this library, clone it first:

    git clone git@bitbucket.org:zepben/cimbend.git

Install as an editable install. Its recommended to install in a [Python virtualenv](https://virtualenv.pypa.io/en/stable/)
    cd cimbend
    pip install -e .



## Sending ##
The most basic usage is to import a class from the model, populate it, and then convert it to a protobuf message with the `to_pb()` function and call the desired service with the result.

Note that Zepben services may enforce requirements on the way you send data. In the following example an `ACLineSegment` is sent to a service that requires the `PerLengthSequenceImpedance` and `BaseVoltage` to be sent first. We will also send `Terminal`'s with the `ACLineSegment` so we can establish connectivity. Note that the `connectivity_node` is not sent separately, but is simply an ID. In this service (postbox), `ConnectivityNode's` are not sent and are always created server side.

Import the classes

    from zepben.model import Terminal, BaseVoltage, PerLengthSequenceImpedance, ACLineSegment, PhaseCode, OverheadWireInfo, WireMaterialKind
    from zepben.postbox import NetworkDataStub

Create the Stub for sending the objects [_see your service documentation for connecting and creating a channel_]:

    nds = NetworkDataStub(channel)
    
Create an instance of the type with your data:

    # Order of terminals matters, as it is used to index into other components. For example,
    # a terminal can be represented on a map with PositionPoint's that are also associated 
    # with an ACLineSegment, and each Terminal should share the same index as its 
    # corresponding PositionPoint.
    terms = []
    terms.append(Terminal(mrid="39f0109a-0846-4ed7-870a-76c01b7f757a", PhaseCode.ABC, connectivity_node="f7689f0d-e73d-4922-9109-7ff428699510"))
    terms.append(Terminal(mrid="45b3cb51-10a8-41a7-9021-82a0b5d30b78", PhaseCode.ABC, connectivity_node="2ac83e5e-3a98-4f03-b822-45d40eb02f30"))
    
    # Create and send dependencies.
    bv = BaseVoltage(mrid="ad033d84-6362-4bc1-aadc-eae18b1135d9", nom_volt=22000)
    plsi = PerLengthSequenceImpedance(mrid="ae670ba6-adee-45eb-a0ec-1174f3ba2ba4", r=10.0, x=100.0, r0=11.0, x0=101.0, bch=2.5435, b0ch=1.434)
    nds.createBaseVoltage(bv.to_pb())
    nds.createPerLengthSequenceImpedance(plsi.to_pb())
    
    # Create and send the ACLS
    acls = ACLineSegment(mrid="3f5ccd6d-dcd9-4b0a-a3e7-e98acf865562", plsi=plsi, length=1234, base_voltage=bv, inService=True, terminals=terms) 
    nds.createAcLineSegment(acls.to_pb())
    
## Receiving ##
When receiving data from a Zepben service, each class has a `from_pb()` function that will do the heavy lifting for you. When you receive a protobuf message, simply call the corresponding model class's `from_pb()` with the protobuf message. 
    
    from zepben.model import ACLineSegment
    
    def convert_acls(pb_acls):
        return ACLineSegment.from_pb(pb_acls)
        
See the specific service you are utilising for more detailed documentation on receiving messages.
