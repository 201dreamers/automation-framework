from collections.abc import Callable
from enum import Enum
from sys import stderr, stdout

from loguru import logger


class LoggerName(Enum):
    STDOUT = "stdout"
    STDERR = "stderr"


class LogLevel(Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def create_filter(name: LoggerName) -> Callable[[dict], bool]:
    """Creates filter which allows to bind a different logger with
    parameter `name`
    """
    def filter(record: dict):
        return record["extra"].get("name") == name
    return filter


DEFAULT_LOG_FORMAT = "{time} {level: <8} | {message}"
DEFAULT_LOG_LEVEL = LogLevel.INFO

# 2 loggers that can be used in tests. This will allow to create 3 separate
# categories in allure report (one is general logger by default)
logger.configure(
    handlers=[
        {
            "sink": stdout,
            "level": DEFAULT_LOG_LEVEL.value,
            "format": DEFAULT_LOG_FORMAT,
            "filter": create_filter(LoggerName.STDOUT)
        },
        {
            "sink": stderr,
            "level": DEFAULT_LOG_LEVEL.value,
            "format": DEFAULT_LOG_FORMAT,
            "filter": create_filter(LoggerName.STDERR)
        }
    ]
)


stdout_logger = logger.bind(name=LoggerName.STDOUT)
stderr_logger = logger.bind(name=LoggerName.STDERR)
