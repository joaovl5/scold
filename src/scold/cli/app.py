from typing import Final

from cyclopts import App
from loguru import logger

from scold.utils.exception import ScoldException
from scold.utils.logger import setup_logger


app: Final[App] = App(
    name="scold",
)

setup_logger()


@app.command(name="new")
def new_object(object_name: str) -> None:
    from scold.cli.commands.new_object import handle_new_object

    try:
        handle_new_object(object_name=object_name)
    except ScoldException as e:
        logger.exception(e.message)
        if hasattr(e, "error"):
            logger.error(f"Nested error: {getattr(e, 'error')}")


if __name__ == "__main__":
    app()
