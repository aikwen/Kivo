import os
import sys
from pathlib import Path


def env_path_add(path: str | Path) -> bool:
    if sys.platform == "win32":
        return _windows_path_add(Path(path))

    raise NotImplementedError(
        f"Unsupported platform: {sys.platform}"
    )


def _windows_path_add(path: Path) -> bool:
    import winreg

    path_text = str(path)

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Environment",
        0,
        winreg.KEY_READ | winreg.KEY_WRITE,
    ) as key:
        try:
            current_path, value_type = winreg.QueryValueEx(
                key,
                "Path",
            )
        except FileNotFoundError:
            current_path = ""
            value_type = winreg.REG_EXPAND_SZ

        entries = [
            entry
            for entry in current_path.split(os.pathsep)
            if entry
        ]

        normalized_path = os.path.normcase(
            os.path.normpath(path_text)
        )

        normalized_entries = {
            os.path.normcase(
                os.path.normpath(entry)
            )
            for entry in entries
        }

        if normalized_path in normalized_entries:
            return False

        entries.append(path_text)

        winreg.SetValueEx(
            key,
            "Path",
            0,
            value_type,
            os.pathsep.join(entries),
        )

    return True