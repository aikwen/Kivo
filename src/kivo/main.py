import sys

from PySide6.QtWidgets import QApplication

from kivo.instance.main import InstanceServer
from kivo.runtime.main import KivoRuntime


def run() -> int:
    app = QApplication(sys.argv)

    instance = InstanceServer("Kivo")

    if not instance.acquire():
        return 0

    # Kivo 依赖 Tray 常驻，不因为 Card hide 而退出。
    app.setQuitOnLastWindowClosed(False)

    runtime = KivoRuntime(app)

    instance.activated.connect(
        runtime.show_launcher
    )

    runtime.start()

    try:
        return app.exec()
    finally:
        runtime.stop()


if __name__ == "__main__":
    raise SystemExit(run())