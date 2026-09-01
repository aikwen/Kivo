import os
import shutil
import subprocess
import sys
from pathlib import Path

from kivo.config.main import Config
from kivo.resources.loader import resource_path
from kivo.utils.env import env_path_add
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


def setup(
    reset: bool = False,
) -> None:
    kivo_home = app_data_dir("Kivo")
    bin_dir = kivo_home / "bin"
    executor_path = bin_dir / "kivo.exe"

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
            executor_path,
        )

    with resource_path(
        "config",
        "win.toml",
    ) as config_template:
        if reset:
            Config.reset(
                config_template,
            )
        else:
            Config.ensure(
                config_template,
            )

    Config.set(
        "runtime",
        "python",
        sys.executable,
    )

    env_path_add(bin_dir)

    _create_start_menu_shortcut(
        executor_path
    )


def _create_start_menu_shortcut(
    target: Path,
) -> None:
    app_data = Path(
        os.environ["APPDATA"]
    )

    shortcut_path = (
        app_data
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Kivo.lnk"
    )

    shortcut_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    target_text = _powershell_quote(
        target
    )
    shortcut_text = _powershell_quote(
        shortcut_path
    )
    working_directory_text = _powershell_quote(
        target.parent
    )

    script = (
        "$shell = New-Object -ComObject WScript.Shell; "
        f"$shortcut = $shell.CreateShortcut('{shortcut_text}'); "
        f"$shortcut.TargetPath = '{target_text}'; "
        f"$shortcut.IconLocation = '{target_text},0'; "
        f"$shortcut.WorkingDirectory = '{working_directory_text}'; "
        "$shortcut.Save()"
    )

    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            script,
        ],
        check=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )


def _powershell_quote(
    path: Path,
) -> str:
    return str(path).replace(
        "'",
        "''",
    )