from kivo.cards.card import Card
from kivo.cards.collection import CardCollection
from kivo.log import Log


class CardManager:
    def __init__(self) -> None:
        self._instances: dict[str, Card] = {}
        self._logger = Log.kivo()

    def open(self, card_id: str) -> None:
        card = self._instances.get(card_id)

        if card is None:
            card_class = CardCollection.get(card_id)

            if card_class is None:
                self._logger.error(
                    "Card not found: %s",
                    card_id,
                )
                return

            try:
                card = card_class(
                    isolated=False
                )
            except Exception:
                self._logger.exception(
                    "Failed to create card: %s",
                    card_id,
                )
                return

            self._instances[card_id] = card

        try:
            card.show()
            card.raise_()
            card.activateWindow()
        except Exception:
            self._logger.exception(
                "Failed to show card: %s",
                card_id,
            )