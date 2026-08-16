import sys

from PySide6.QtWidgets import QApplication

from kivo.launcher.window.main import LauncherWindow
from kivo.tray.main import Tray


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

    def toggle_launcher() -> None:
        if launcher.isVisible():
            launcher.hide()
            return

        launcher.show()
        launcher.raise_()
        launcher.activateWindow()

    tray.activated.connect(toggle_launcher)
    tray.exit_requested.connect(app.quit)

    tray.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())