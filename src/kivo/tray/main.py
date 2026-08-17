import sys
from importlib.resources import files

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMenu,
    QSystemTrayIcon,
)


class Tray(QObject):
    activated = Signal()
    exit_requested = Signal()

    def __init__(
        self,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        icon_path = files(
            "kivo.resources.icons"
        ).joinpath(
            "tray.ico"
        )

        icon = QIcon(str(icon_path))

        self._tray = QSystemTrayIcon(icon, self)

        self._menu = QMenu()

        self._exit_action = QAction("Exit", self._menu)
        self._exit_action.triggered.connect(
            self.exit_requested
        )

        self._menu.addAction(self._exit_action)

        self._tray.setContextMenu(self._menu)
        self._tray.activated.connect(
            self._on_activated
        )

    def show(self) -> None:
        self._tray.show()

    def hide(self) -> None:
        self._tray.hide()

    def _on_activated(
        self,
        reason: QSystemTrayIcon.ActivationReason,
    ) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.activated.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    tray = Tray()

    tray.activated.connect(
        lambda: print("tray activated")
    )
    tray.exit_requested.connect(app.quit)

    tray.show()

    sys.exit(app.exec())