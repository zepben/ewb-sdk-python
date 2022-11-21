from unittest.mock import Mock
from unittest import mock

from zepben.evolve import GrpcChannelBuilder

base_gcb = Mock()
addressed_gcb = Mock()
secure_gcb = Mock()
authenticated_gcb = Mock()
insecure_channel = Mock()
secure_channel = Mock()
authenticated_channel = Mock()

base_gcb.for_address = Mock(return_value=addressed_gcb)
addressed_gcb.make_secure = Mock(return_value=secure_gcb)
secure_gcb.with_token_fetcher = Mock(return_value=authenticated_gcb)
addressed_gcb.build = Mock(return_value=insecure_channel)
secure_gcb.build = Mock(return_value=secure_channel)
authenticated_gcb.build = Mock(return_value=authenticated_channel)


@mock.patch("zepben.evolve.GrpcChannelBuilder", autospec=True)
def test_connect_insecure(mocked_gcb):
    mocked_gcb.return_value = base_gcb
    print(GrpcChannelBuilder())
