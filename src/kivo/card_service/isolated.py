import sys

from PySide6.QtWidgets import QApplication

from kivo.cards.collection import CardCollection


def run(card_id: str) -> None:
    app = QApplication(sys.argv)

    card_class = CardCollection.get(card_id)
    if card_class is None:
        raise RuntimeError(
            f"Card not found: {card_id}"
        )

    card = card_class(isolated=True)
    card.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise RuntimeError(
            "Usage: python -m kivo.card_service.isolated <card_id>"
        )

    run(sys.argv[1])