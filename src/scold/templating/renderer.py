from collections.abc import Callable
from pathlib import Path
from typing import Any

import caseconverter
from loguru import logger
from mako.template import Template
from pydantic import DirectoryPath, FilePath

from scold.config.types import FileNamingType
from scold.utils.exception import ScoldException


class ScoldMissingTemplateException(ScoldException): ...


class ScoldMultipleTemplatesException(ScoldException): ...


TEMPLATE_GLOB = "__template*"

NAMING_TRANSFORMERS: dict[FileNamingType, Callable[[str], str]] = {
    FileNamingType.SNAKE_CASE: caseconverter.snakecase,
}


def render_single_template(
    template_path: FilePath,
    out_path: FilePath,
    vars: dict[str, Any],
) -> None:
    templ = Template(filename=str(template_path.resolve()))
    data = templ.render(**vars)
    open_opts = "w" if isinstance(data, str) else "wb"
    with out_path.open(open_opts) as out_file:
        _ = out_file.write(data)


def render_object(
    object_dir: DirectoryPath,
    object_vars: dict[str, Any],
    object_name: str,
    object_naming_type: FileNamingType,
) -> None:
    template_path: Path | None = None
    is_template_directory: bool = False
    for path in object_dir.glob(
        # checks directory or file case
        TEMPLATE_GLOB,
    ):
        if template_path:
            raise ScoldMultipleTemplatesException(
                f"Found more than one path matching template glob '{TEMPLATE_GLOB}'"
                + f"\n- {template_path}"
                + f"\n- {path}"
            )
        template_path = path
        if path.is_dir():
            is_template_directory = True
    if not template_path:
        raise ScoldMissingTemplateException(
            f"No template file/folder found matching glob '{TEMPLATE_GLOB}' in {object_dir}"
        )

    template_files: list[Path] = []
    if is_template_directory:
        template_files.extend(template_path.glob("*"))
    else:
        template_files.append(template_path)

    transformed_name = NAMING_TRANSFORMERS[object_naming_type](object_name)
    output_dir = object_dir
    if is_template_directory:
        output_dir = output_dir / transformed_name
        output_dir.mkdir(exist_ok=True)
    for template_file in template_files:
        out_path: Path
        if is_template_directory:
            out_path = output_dir / template_file.name
        else:
            out_path = output_dir / (transformed_name + template_file.suffix)
        logger.trace(f"Rendering template {template_file} at {out_path}")
        render_single_template(
            template_path=template_file,
            out_path=out_path,
            vars=object_vars,
        )
