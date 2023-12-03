from pytest import fixture, mark, param

from src.connectors import ConnectionType
from src.device_lib.device_lib import DeviceLib


@fixture(scope="function", autouse=True)
def device_lib(request, device_name):
    connection_type = request.node.callspec.params.get("connection_type_under_test")
    device_lib = DeviceLib(connection_type, device_name)
    yield device_lib
    device_lib.connection.close_connection()


@mark.parametrize(
    "connection_type_under_test",
    (param(ConnectionType.SSH, marks=mark.ssh_only),
     param(ConnectionType.SERIAL, marks=mark.serial_only))
)
def test_connection(device_lib, connection_type_under_test):
    assert device_lib.connection.is_connected()
    device_lib.beep()
