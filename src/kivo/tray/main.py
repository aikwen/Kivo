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

        menu_width = self._menu.width()
        menu_height = self._menu.height()

        center = geometry.center()

        shadow_margin = self._menu.Style.shadow_margin
        offset = 2

        if cursor.x() < center.x():
            # 左侧：菜单左边靠近鼠标，向右展开
            x = cursor.x() - shadow_margin + offset
        else:
            # 右侧：菜单右边靠近鼠标，向左展开
            x = (
                    cursor.x()
                    - menu_width
                    + shadow_margin
                    - offset
            )

        if cursor.y() < center.y():
            # 上侧：菜单顶部靠近鼠标，向下展开
            y = cursor.y() - shadow_margin + offset
        else:
            # 下侧：菜单底部靠近鼠标，向上展开
            y = (
                    cursor.y()
                    - menu_height
                    + shadow_margin
                    - offset
            )

        self._menu.move(x, y)
        self._menu.show()
        self._menu.raise_()
        self._menu.activateWindow()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    tray = Tray()

    tray.activated.connect(
        lambda: print("tray activated")
    )
    tray.exit_requested.connect(app.quit)

    tray.show()

    sys.exit(app.exec())