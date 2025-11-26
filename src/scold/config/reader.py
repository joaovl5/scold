import tomllib

from pydantic import DirectoryPath, FilePath, ValidationError

from scold.config.types import ScoldConfigFile
from scold.utils.exception import ScoldException

SCOLD_FILE_NAME = "scold.toml"


class ScoldConfigReaderException(ScoldException): ...


class ScoldNoConfigFoundException(ScoldConfigReaderException): ...


class ScoldConfigFormatError(ScoldConfigReaderException):
    def __init__(
        self,
        error: ValidationError | tomllib.TOMLDecodeError,
        message: str | None = None,
        *args: object,
        **kwargs: object,
    ) -> None:
        self.error: ValidationError | tomllib.TOMLDecodeError = error
        super().__init__(message, *args, **kwargs)


def find_scold_config(current_dir: DirectoryPath) -> ScoldConfigFile:
    config: ScoldConfigFile | None = None
    # attempt to find nearest root scold.toml
    while config is None:
        scold_cfg_path = current_dir / SCOLD_FILE_NAME
        if not (scold_cfg_path.exists()):
            if current_dir.parent == current_dir:  # we're in filesystem root
                raise ScoldNoConfigFoundException(
                    "No config found up to root of filesystem"
                )
            current_dir = current_dir.parent
            continue
        try:
            config = read_scold_config(toml_path=scold_cfg_path)
        except (ValidationError, tomllib.TOMLDecodeError) as e:
            raise ScoldConfigFormatError(
                error=e,
                message=f"Config found at {scold_cfg_path} has one or more validation errors",
            )
    return config


def read_scold_config(toml_path: FilePath) -> ScoldConfigFile:
    with toml_path.open("rb") as file:
        toml_data = tomllib.load(file)
    return ScoldConfigFile.model_validate(toml_data)
