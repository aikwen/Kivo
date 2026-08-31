import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from kivo.cards.collection import CardCollection
from kivo.log import Log
from kivo.resources.loader import resource_path


def run(card_id: str) -> None:
    logger = Log.kivo()

    try:
        app = QApplication(sys.argv)

        card_class = CardCollection.get(card_id)
        if card_class is None:
            raise RuntimeError(
                f"Card not found: {card_id}"
            )

        card = card_class()

        card.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        with resource_path(
            "icons",
            "tray.ico",
        ) as icon_path:
            card.setWindowIcon(
                QIcon(str(icon_path))
            )

        card.hide_requested.connect(
            card.showMinimized
        )

        card.exit_requested.connect(
            card.close
        )

        card.exit_requested.connect(
            app.quit
        )

        card.show()

        sys.exit(app.exec())

    except Exception:
        logger.exception(
            "Failed to run isolated card: %s",
            card_id,
        )
        raise


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise RuntimeError(
            "Usage: python -m kivo.card_service.isolated <card_id>"
        )

    run(sys.argv[1])