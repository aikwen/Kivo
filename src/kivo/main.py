import sys

from PySide6.QtWidgets import QApplication

from kivo.hotkey.main import GlobalHotkey
from kivo.launcher.window.main import LauncherWindow
from kivo.tray.main import Tray


LAUNCHER_X_RATIO = 0.41
LAUNCHER_Y_RATIO = 0.34


def run() -> int:
    app = QApplication(sys.argv)

    # Kivo 依赖 Tray 常驻，不因为 Launcher hide 而退出。
    app.setQuitOnLastWindowClosed(False)

    launcher = LauncherWindow()
    launcher.resize(570, 63)

    launcher.set_cards(
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
        ]
    )

    tray = Tray()
    hotkey = GlobalHotkey()

    def move_launcher() -> None:
        screen = app.primaryScreen()
        if screen is None:
            return

        geometry = screen.availableGeometry()

        x = geometry.x() + int(
            geometry.width() * LAUNCHER_X_RATIO
        )
        y = geometry.y() + int(
            geometry.height() * LAUNCHER_Y_RATIO
        )

        launcher.move(x, y)

    def toggle_launcher() -> None:
        if launcher.isVisible():
            launcher.hide()
            return

        move_launcher()

        launcher.show()
        launcher.raise_()
        launcher.activateWindow()

    tray.activated.connect(toggle_launcher)
    tray.exit_requested.connect(app.quit)

    hotkey.activated.connect(toggle_launcher)

    app.installNativeEventFilter(
        hotkey.event_filter()
    )

    hotkey.register()
    tray.show()

    exit_code = app.exec()

    hotkey.unregister()

    return exit_code


if __name__ == "__main__":
    raise SystemExit(run())