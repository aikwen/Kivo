import sys

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
)

from kivo.resources.loader import resource_path
from kivo.tray.menu import TrayMenu


class Tray(QObject):
    activated = Signal()
    exit_requested = Signal()

    def __init__(
        self,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        with resource_path(
            "icons",
            "tray.ico",
        ) as icon_path:
            icon = QIcon(str(icon_path))

        self._tray = QSystemTrayIcon(icon, self)

        self._menu = TrayMenu()
        self._menu.exit_requested.connect(
            self.exit_requested
        )

        self._tray.activated.connect(
            self._on_activated
        )

    def show(self) -> None:
        self._tray.show()

    def hide(self) -> None:
        self._tray.hide()
        self._menu.hide()

    def _on_activated(
        self,
        reason: QSystemTrayIcon.ActivationReason,
    ) -> None:
        if (
            reason
            == QSystemTrayIcon.ActivationReason.Trigger
        ):
            self.activated.emit()
            return

        if (
            reason
            == QSystemTrayIcon.ActivationReason.Context
        ):
            self._show_menu()

    def _show_menu(self) -> None:
        cursor = QCursor.pos()

        screen = QApplication.screenAt(cursor)
        if screen is None:
            screen = QApplication.primaryScreen()

        if screen is None:
            return

        geometry = screen.availableGeometry()

        self._menu.adjustSize()

        center = geometry.center()
        offset = 4

        if cursor.x() < center.x():
            x = cursor.x() + offset
        else:
            x = (
                cursor.x()
                - self._menu.width()
                - offset
            )

        if cursor.y() < center.y():
            y = cursor.y() + offset
        else:
            y = (
                cursor.y()
                - self._menu.height()
                - offset
            )

        self._menu.move(x, y)

        self._menu.show()
        self._menu.raise_()
        self._menu.activateWindow()
        self._menu.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    tray = Tray()

    tray.activated.connect(
        lambda: print("tray activated")
    )
    tray.exit_requested.connect(app.quit)

    tray.show()

    sys.exit(app.exec())