# Sending data using cimbend #
The `to_pb()` and `from_pb(*args, **kwargs)` functions for each class in the model allow simplified conversion between model objects and their equivalent protobuf objects.

`from_pb()` will often require you to pass in some extra arguments to gather dependencies. The most frequent of these is `network: Network`, so relevant dependencies can be fetched from the network. In some cases dependencies are hard, and `from_pb()` will propagate some form of `MissingReferenceException` if the network does not contain the required dependency. See the relevant documentation in `from_pb()` for these cases. 

Where a Protobuf message contains a `oneof` field, as per Protobuf rules only the field that has been explicitly set will be utilised. See AssetInfo example below.

Other than the above described dependency checks, `from_pb()` will not perform any other data checks, and if a field in a Protobuf message provided to `from_pb()` is not set, it will receive the [Protobuf default value](https://developers.google.com/protocol-buffers/docs/proto3#default) for that field type.

Example: Network doesn't contain dependency and it's required. Include "empty" example (i.e no MRID was provided)

    
Example: Unset message fields receiving default values with `from_pb()`

Example: Sending an AssetInfo 

