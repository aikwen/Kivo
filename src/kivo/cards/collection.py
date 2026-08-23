

class CardCollection:
    @classmethod
    def list(cls) -> list[str]:
        return list(cls._cards)

    @classmethod
    def get(cls, card_id: str) -> type | None:
        return cls._cards.get(card_id)

    _cards: dict[str, type] = {

    }