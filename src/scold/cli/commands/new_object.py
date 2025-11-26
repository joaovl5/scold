from pathlib import Path
import pprint
from typing import Any
from loguru import logger
from rich import print as rprint
import questionary

from scold.config.reader import find_scold_config
from scold.config.types import OBJECT_NAME_FIELD, ObjectVar, VarType
from scold.templating.renderer import render_object
from scold.utils.exception import ScoldException

from mako.template import Template


class ScoldObjectMissingException(ScoldException): ...


class ScoldDirectoryMissingException(ScoldException): ...


def handle_object_var(var: ObjectVar) -> Any:
    match var.type:
        case VarType.TEXT:
            prompt = questionary.text(
                message=var.desc or var.field,
            )
            if var.default:
                prompt.default = var.default

            return prompt.ask()
        case VarType.BOOL:
            prompt = questionary.confirm(
                message=var.desc or var.field,
            )
            if var.default:
                prompt.default = var.default

            return prompt.ask()
        case VarType.GROUP:
            if not var.group:  # should NEVER happen
                raise ScoldException("var.group wasn't defined")
            group_start = f"----[{var.desc or var.field}]----"
            rprint(f"[white bold]{group_start}[/]")
            data = {
                sub_var.field: handle_object_var(
                    var=sub_var,
                )
                for sub_var in var.group
            }
            rprint(f"[white bold]{'-' * len(group_start)}[/]")
            return data


def handle_new_object(object_name: str) -> None:
    logger.trace("Attempting to find config...")
    config = find_scold_config(
        current_dir=Path.cwd(),
    )
    logger.trace("Found config...")

    # handle config options

    project_settings = config.project
    object_settings = config.objects.get(object_name)
    if not object_settings:
        raise ScoldObjectMissingException(
            f"Object '{object_name}' not found in config file"
        )
    object_dir = project_settings.root_dir / object_settings.dir
    if not object_dir.exists():
        raise ScoldDirectoryMissingException(
            f"Directory for object '{object_name}' doesn't exist: {object_dir}"
        )
    if not object_dir.is_dir():
        raise ScoldDirectoryMissingException(
            f"For object '{object_name}', expected directory at '{object_dir}', but path is file"
        )

    object_vars: dict[str, Any] = {}
    for var in object_settings.vars:
        object_vars[var.field] = handle_object_var(var=var)

    object_instance_name = object_vars[OBJECT_NAME_FIELD]

    render_object(
        object_dir=object_dir,
        object_vars=object_vars,
        object_name=object_instance_name,
        object_naming_type=project_settings.default_file_naming,
    )

    pprint.pp(object_vars)
