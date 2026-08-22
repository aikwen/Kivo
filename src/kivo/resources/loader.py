from collections.abc import Iterator
from contextlib import contextmanager
from importlib.resources import as_file, files
from pathlib import Path


@contextmanager
def resource_path(
    *parts: str,
) -> Iterator[Path]:
    resource = files(
        "kivo.resources"
    ).joinpath(*parts)

    if not resource.is_file():
        raise FileNotFoundError(
            f"Kivo resource not found: {'/'.join(parts)}"
        )

    with as_file(resource) as path:
        yield path