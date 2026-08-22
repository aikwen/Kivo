from pathlib import Path
from collections.abc import Mapping
import configparser


def ini_write(
    path: str | Path,
    section: str,
    values: Mapping[str, str],
) -> None:
    config = configparser.ConfigParser()

    path = Path(path)

    if path.exists():
        config.read(
            path,
            encoding="utf-8",
        )

    config[section] = dict(values)

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        config.write(file)