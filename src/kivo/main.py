import sys

from PySide6.QtWidgets import QApplication

from kivo.runtime.main import KivoRuntime


def run() -> int:
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    runtime = KivoRuntime(app)
    runtime.start()

    try:
        return app.exec()
    finally:
        runtime.stop()


if __name__ == "__main__":
    raise SystemExit(run())