from zepben.model import EquipmentContainer, MetricsStore


def retrieve_network(rpc, *args, **kwargs):
    """
    Given an RPC call that returns a stream of Equipment, this will stream the equipment into a new EquipmentContainer
    and return that container.

    :param rpc: The RPC call to be executed.
    :param *args: args to be passed to the RPC call
    :param **kwargs: kwargs to be passed to the RPC call
    :return: A :class:`zepben.model.network.EquipmentContainer` containing the streamed network.
    """
    network = EquipmentContainer(MetricsStore())
    stream_response = rpc(*args, **kwargs)
    for eq_msg in stream_response:
        if eq_msg.HasField("es"):
            network.add_pb_energy_source(eq_msg.es)
        elif eq_msg.HasField("ec"):
            network.add_pb_energy_consumer(eq_msg.ec)
        elif eq_msg.HasField("pt"):
            network.add_pb_transformer(eq_msg.pt)
        elif eq_msg.HasField("acls"):
            network.add_pb_aclinesegment(eq_msg.acls)
        elif eq_msg.HasField("br"):
            network.add_pb_breaker(eq_msg.br)
        elif eq_msg.HasField("bv"):
            network.add_pb_base_voltage(eq_msg.bv)
        elif eq_msg.HasField("ai"):
            network.add_pb_asset_info(eq_msg.ai)
        elif eq_msg.HasField("si"):
            network.add_pb_per_length_sequence_impedance(eq_msg.si)
        elif eq_msg.HasField("up"):
            network.add_pb_usage_point(eq_msg.up)
        elif eq_msg.HasField("mt"):
            network.add_pb_meter(eq_msg.mt)
    return network
