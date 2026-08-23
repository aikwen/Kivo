from PySide6.QtWidgets import QWidget

from kivo.cards.collection import CardCollection


class CardManager:
    def __init__(self) -> None:
        self._instances: dict[str, QWidget] = {}

    def open(self, card_id: str) -> None:
        card = self._instances.get(card_id)

        if card is None:
            card_class = CardCollection.get(card_id)

            if card_class is None:
                return

            card = card_class(isolated=False)
            self._instances[card_id] = card

        card.show()
        card.raise_()
        card.activateWindow()