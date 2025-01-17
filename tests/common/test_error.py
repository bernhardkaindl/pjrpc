import pytest

import xjsonrpc


def test_error_serialization():
    error = xjsonrpc.exc.ServerError()

    actual_dict = error.to_json()
    expected_dict = {
        'code': -32000,
        'message': 'Server error',
    }

    assert actual_dict == expected_dict


def test_error_deserialization():
    data = {
        'code': -32000,
        'message': 'Server error',
    }

    error = xjsonrpc.exc.ServerError.from_json(data)

    assert error.code == -32000
    assert error.message == 'Server error'


def test_error_data_serialization():
    error = xjsonrpc.exc.MethodNotFoundError(data='method_name')

    actual_dict = error.to_json()
    expected_dict = {
        'code': -32601,
        'message': 'Method not found',
        'data': 'method_name',
    }

    assert actual_dict == expected_dict


def test_custom_error_data_serialization():
    error = xjsonrpc.exc.JsonRpcError(
        code=2001, message='Custom error', data='additional data'
    )

    actual_dict = error.to_json()
    expected_dict = {
        'code': 2001,
        'message': 'Custom error',
        'data': 'additional data',
    }

    assert actual_dict == expected_dict


def test_custom_error_data_deserialization():
    data = {
        'code': -32601,
        'message': 'Method not found',
        'data': 'method_name',
    }

    error = xjsonrpc.exc.JsonRpcError.from_json(data)

    assert error.code == -32601
    assert error.message == 'Method not found'
    assert error.data == 'method_name'


def test_error_deserialization_errors():
    xdeser = xjsonrpc.exc.DeserializationError

    with pytest.raises(xdeser, match="data must be of type dict"):
        xjsonrpc.exc.JsonRpcError.from_json([])

    with pytest.raises(xdeser, match="required field 'message' not found"):
        xjsonrpc.exc.JsonRpcError.from_json({'code': 1})

    with pytest.raises(xdeser, match="required field 'code' not found"):
        xjsonrpc.exc.JsonRpcError.from_json({'message': ""})

    with pytest.raises(xdeser, match="field 'code' must be of type integer"):
        xjsonrpc.exc.JsonRpcError.from_json({'code': "1", 'message': ""})

    with pytest.raises(xdeser, match="field 'message' must be of type string"):
        xjsonrpc.exc.JsonRpcError.from_json({'code': 1, 'message': 2})


def test_error_repr():
    assert (
        repr(xjsonrpc.exc.ServerError(data='data'))
        == "ServerError(code=-32000, message='Server error', data='data')"
    )
    assert str(xjsonrpc.exc.ServerError()) == "(-32000) Server error"


def test_custom_error_registration():
    data = {
        'code': 2000,
        'message': 'Custom error',
        'data': 'custom_data',
    }

    class CustomError(xjsonrpc.exc.JsonRpcError):
        code = 2000
        message = 'Custom error'

    error = xjsonrpc.exc.JsonRpcError.from_json(data)

    assert isinstance(error, CustomError)
    assert error.code == 2000
    assert error.message == 'Custom error'
    assert error.data == 'custom_data'
