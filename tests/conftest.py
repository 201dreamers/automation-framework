from pytest import fixture, mark

from src.connectors import ConnectionType, NoSuchConnectionTypeError
from src.device_lib.device_lib import DeviceLib


# #####
# Hooks
# #####

def pytest_addoption(parser):
    """Configures the command line options"""
    parser.addoption(
        "--connection",
        action="store",
        help="Connection type",
        default="ssh"
    )
    parser.addoption(
        "--device",
        action="store",
        help="Device name"
    )


def pytest_collection_modifyitems(session, config, items):
    """Determines which tests need to be skipped based on
    * Connection
    """
    connection = config.getoption("--connection").lower()

    for item in items:
        markers = tuple(item.iter_markers())

        for marker in markers:
            # Skip by connection
            if "_only" in marker.name and connection not in marker.name:
                item.add_marker(
                    mark.skip(reason=f"Test requires {connection} connection"))


# ########
# Fixtures
# ########

@fixture(scope="session")
def device_name(request):
    return request.config.getoption("--device")


@fixture(scope="session")
def connection_type(request):
    connection = request.config.getoption("--connection")

    if connection.lower() == "ssh":
        connetion_type = ConnectionType.SSH
    elif connection.lower() == "serial":
        connetion_type = ConnectionType.SERIAL
    else:
        raise NoSuchConnectionTypeError(connection)

    return connetion_type


@fixture(scope="session")
def device_lib(connection_type, device_name):
    device_lib = DeviceLib(connection_type, device_name)
    yield device_lib
    device_lib.connection.close_connection()
