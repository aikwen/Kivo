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
                card = card_class()
            except Exception:
                self._logger.exception(
                    "Failed to create card: %s",
                    card_id,
                )
                return

            card.hide_requested.connect(
                card.hide
            )

            card.exit_requested.connect(
                lambda card_id=card_id: self._close(
                    card_id
                )
            )

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

    def _close(
        self,
        card_id: str,
    ) -> None:
        card = self._instances.get(card_id)

        if card is None:
            return

        try:
            if card.close():
                self._instances.pop(
                    card_id,
                    None,
                )
        except Exception:
            self._logger.exception(
                "Failed to close card: %s",
                card_id,
            )