from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication

from kivo.cards.launcher.main import LauncherWindow
from kivo.hotkey.main import GlobalHotkey
from kivo.tray.main import Tray


class KivoRuntime:
    def __init__(self, app: QApplication) -> None:
        self.app = app

        self.launcher = LauncherWindow()
        self.launcher.resize(
            LauncherWindow.Style.width,
            LauncherWindow.Style.height,
        )

        self.tray = Tray()
        self.hotkey = GlobalHotkey()

        self.launcher.set_cards(
            [
                "JSON Formatter",
                "JWT Viewer",
                "Color Converter",
                "Calendar",
                "Timestamp Converter",
                "Base64",
                "UUID Generator",
                "Hash Calculator",
                "Regular Expression",
                "Environment Variables",
                "json 格式化",
            ]
        )

        self.tray.activated.connect(
            self._toggle_launcher
        )
        self.tray.exit_requested.connect(
            self.app.quit
        )

        self.hotkey.activated.connect(
            self._toggle_launcher
        )

    def start(self) -> None:
        self.app.installNativeEventFilter(
            self.hotkey.event_filter()
        )

        self.hotkey.register()
        self.tray.show()

    def stop(self) -> None:
        self.hotkey.unregister()

    def _move_launcher(self) -> None:
        screen = self.app.screenAt(QCursor.pos())

        if screen is None:
            screen = self.app.primaryScreen()

        if screen is None:
            return

        geometry = screen.availableGeometry()

        x = geometry.x() + int(
            geometry.width()
            * LauncherWindow.Style.x_ratio
        )
        y = geometry.y() + int(
            geometry.height()
            * LauncherWindow.Style.y_ratio
        )

        self.launcher.move(x, y)

    def _toggle_launcher(self) -> None:
        if self.launcher.isVisible():
            self.launcher.hide()
            return

        self._move_launcher()

        self.launcher.show()
        self.launcher.raise_()
        self.launcher.activateWindow()