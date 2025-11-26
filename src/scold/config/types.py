from decimal import ExtendedContext
from enum import Enum
from pathlib import Path
from typing import Any, Self
from pydantic import BaseModel, DirectoryPath, Field, model_validator

OBJECT_NAME_FIELD = "object_name"


class FileNamingType(Enum):
    SNAKE_CASE = "snake_case"


class VarType(Enum):
    TEXT = "text"
    BOOL = "bool"
    GROUP = "group"


class ProjectSettings(BaseModel):
    root_dir: DirectoryPath
    default_file_naming: FileNamingType


class ObjectVar(BaseModel):
    field: str
    desc: str | None = None
    type: VarType | None = None  # when has property "group", type=group is autoset
    group: list["ObjectVar"] | None = None
    default: Any | None = None  # pyright: ignore[reportExplicitAny]
    # todo - validate defaults

    @model_validator(mode="before")
    @classmethod
    def _handle_preprocess(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "group" in data:
                data["type"] = VarType.GROUP
                return data
            if "type" not in data:
                raise TypeError("Missing 'type' field")
        return data


class ObjectSettings(BaseModel):
    dir: Path
    vars: list[ObjectVar] = Field(default_factory=list)

    @model_validator(mode="after")
    def _handle_postprocess(self) -> Self:
        has_type_name = False
        for var in self.vars:
            if var.field == OBJECT_NAME_FIELD:
                has_type_name = True
        if not has_type_name:
            raise TypeError(
                f"At least one variable in object should be '{OBJECT_NAME_FIELD}'"
            )
        return self


class ScoldConfigFile(BaseModel):
    project: ProjectSettings
    objects: dict[str, ObjectSettings] = Field(default_factory=dict)
