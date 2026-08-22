import sys

from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication

from kivo.cards.launcher.main import LauncherWindow
from kivo.hotkey.main import GlobalHotkey
from kivo.tray.main import Tray


def run() -> int:
    app = QApplication(sys.argv)

    # Kivo 依赖 Tray 常驻，不因为 Launcher hide 而退出。
    app.setQuitOnLastWindowClosed(False)

    launcher = LauncherWindow()
    launcher.resize(
        LauncherWindow.Style.width,
        LauncherWindow.Style.height,
    )

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
        # 根据鼠标当前位置选择目标屏幕。
        screen = app.screenAt(QCursor.pos())

        # 获取不到时回退到主屏。
        if screen is None:
            screen = app.primaryScreen()

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