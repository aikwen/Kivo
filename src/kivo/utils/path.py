import os
import sys
from pathlib import Path


def app_data_dir(name: str) -> Path:
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")

        if not local_app_data:
            raise RuntimeError(
                "LOCALAPPDATA is not available."
            )

        return Path(local_app_data) / name

    if sys.platform == "darwin":
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / name
        )

    raise NotImplementedError(
        f"Unsupported platform: {sys.platform}"
    )

def card_data_dir(card_id: str) -> Path:
    path = (
        app_data_dir("Kivo")
        / "cards"
        / card_id
    )

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path