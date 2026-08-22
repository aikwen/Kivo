import sys

from PySide6.QtWidgets import QApplication

from kivo.runtime.main import KivoRuntime


def run() -> int:
    app = QApplication(sys.argv)

    # Kivo 依赖 Tray 常驻，不因为 Card hide 而退出。
    app.setQuitOnLastWindowClosed(False)

    runtime = KivoRuntime(app)
    runtime.start()

    exit_code = app.exec()

    runtime.stop()

    return exit_code


if __name__ == "__main__":
    raise SystemExit(run())