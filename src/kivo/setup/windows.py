import shutil
import subprocess
import sys

from kivo.resources.loader import resource_path
from kivo.utils.env import env_path_add
from kivo.utils.ini import ini_write
from kivo.utils.path import app_data_dir


def run() -> None:
    with resource_path(
        "executor",
        "kivo.exe",
    ) as executor:
        subprocess.Popen(
            [
                str(executor),
                sys.executable,
            ]
        )


def setup() -> None:
    kivo_home = app_data_dir("Kivo")
    bin_dir = kivo_home / "bin"

    bin_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    with resource_path(
        "executor",
        "kivo.exe",
    ) as executor:
        shutil.copy2(
            executor,
            bin_dir / "kivo.exe",
        )

    ini_write(
        kivo_home / "config.ini",
        "runtime",
        {
            "python": sys.executable,
        },
    )

    env_path_add(bin_dir)