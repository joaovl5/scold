import sys
from loguru import logger


def setup_logger() -> None:
    logger.remove()
    _ = logger.add(
        sink=sys.stderr,
        level="TRACE",
    )
