import ctypes
from ctypes import wintypes

from PySide6.QtCore import (
    QAbstractNativeEventFilter,
    QObject,
    Signal,
)


WM_HOTKEY = 0x0312

MOD_ALT = 0x0001
MOD_SHIFT = 0x0004

VK_K = 0x4B

HOTKEY_ID = 1


user32 = ctypes.windll.user32


class _HotkeyEventFilter(QAbstractNativeEventFilter):
    def __init__(self, owner: "GlobalHotkey") -> None:
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
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self._registered = False
        self._filter = _HotkeyEventFilter(self)

    def register(self) -> bool:
        if self._registered:
            return True

        success = user32.RegisterHotKey(
            None,
            HOTKEY_ID,
            MOD_ALT | MOD_SHIFT,
            VK_K,
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

    def event_filter(self) -> QAbstractNativeEventFilter:
        return self._filter