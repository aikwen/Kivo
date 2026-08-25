import tomllib
from pathlib import Path
from typing import Any

import tomli_w

from kivo.utils.path import app_data_dir


class Config:
    @classmethod
    def get(
        cls,
        section: str,
        key: str,
        default: Any = None,
    ) -> Any:
        data = cls._read()

        section_data = data.get(section)
        if not isinstance(section_data, dict):
            return default

        return section_data.get(
            key,
            default,
        )

    @classmethod
    def set(
        cls,
        section: str,
        key: str,
        value: Any,
    ) -> None:
        data = cls._read()

        section_data = data.get(section)

        if not isinstance(section_data, dict):
            section_data = {}
            data[section] = section_data

        section_data[key] = value

        cls._write(data)

    @classmethod
    def path(cls) -> Path:
        return (
            app_data_dir("Kivo")
            / "config.toml"
        )

    @classmethod
    def _read(cls) -> dict[str, Any]:
        path = cls.path()

        if not path.exists():
            return {}

        with path.open(
            "rb",
        ) as file:
            return tomllib.load(file)

    @classmethod
    def _write(
        cls,
        data: dict[str, Any],
    ) -> None:
        path = cls.path()

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "wb",
        ) as file:
            tomli_w.dump(
                data,
                file,
            )