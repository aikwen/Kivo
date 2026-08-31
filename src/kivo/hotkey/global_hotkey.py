import ctypes
from ctypes import wintypes

from PySide6.QtCore import (
    QAbstractNativeEventFilter,
    QObject,
    Signal,
)


WM_HOTKEY = 0x0312

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008

HOTKEY_ID = 1

DEFAULT_SHORTCUT = "Alt + Shift + K"


user32 = ctypes.windll.user32


def _parse_shortcut(
    shortcut: str,
) -> tuple[int, int]:
    parts = [
        part.strip()
        for part in shortcut.split("+")
    ]

    if (
        len(parts) != 3
        or any(not part for part in parts)
    ):
        raise ValueError(
            f"Invalid hotkey: {shortcut}"
        )

    modifiers = 0

    for modifier in parts[:-1]:
        name = modifier.lower()

        if name == "alt":
            modifiers |= MOD_ALT
            continue

        if name in {"ctrl", "control"}:
            modifiers |= MOD_CONTROL
            continue

        if name == "shift":
            modifiers |= MOD_SHIFT
            continue

        if name in {"win", "windows"}:
            modifiers |= MOD_WIN
            continue

        raise ValueError(
            f"Unsupported hotkey modifier: {modifier}"
        )

    key = parts[-1].upper()

    if len(key) == 1 and (
        "A" <= key <= "Z"
        or "0" <= key <= "9"
    ):
        virtual_key = ord(key)
    else:
        raise ValueError(
            f"Unsupported hotkey key: {key}"
        )

    return modifiers, virtual_key


class _HotkeyEventFilter(QAbstractNativeEventFilter):
    def __init__(
        self,
        owner: "GlobalHotkey",
    ) -> None:
        super().__init__()

        self._owner = owner

    def nativeEventFilter(
        self,
        event_type,
        message,
    ) -> tuple[bool, int]:
        msg = wintypes.MSG.from_address(
            int(message)
        )

        if (
            msg.message == WM_HOTKEY
            and msg.wParam == HOTKEY_ID
        ):
            self._owner.activated.emit()
            return True, 0

        return False, 0


class GlobalHotkey(QObject):
    activated = Signal()

    def __init__(
        self,
        shortcut: str,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self.shortcut = shortcut

        (
            self._modifiers,
            self._virtual_key,
        ) = _parse_shortcut(shortcut)

        self._registered = False
        self._filter = _HotkeyEventFilter(self)

    def register(self) -> bool:
        if self._registered:
            return True

        success = user32.RegisterHotKey(
            None,
            HOTKEY_ID,
            self._modifiers,
            self._virtual_key,
        )

        if not success:
            return False

        self._registered = True

        return True

    def unregister(self) -> None:
        if not self._registered:
            return

        user32.UnregisterHotKey(
            None,
            HOTKEY_ID,
        )

        self._registered = False

    def event_filter(
        self,
    ) -> QAbstractNativeEventFilter:
        return self._filter