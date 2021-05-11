from _pytest.python_api import raises

from zepben.evolve import GrpcResult


def test_value_works_if_valid():
    assert GrpcResult(12).value == 12


def test_value_throws_if_invalid():
    exception = Exception()
    with raises(TypeError, match="You can only call value on a successful result."):
        assert GrpcResult(exception).value == exception


def test_thrown_works_if_invalid():
    exception = Exception()
    assert GrpcResult(exception).thrown == exception


def test_thrown_throws_if_valid():
    with raises(TypeError, match="You can only call thrown on an unsuccessful result."):
        assert GrpcResult(12).thrown == 12
