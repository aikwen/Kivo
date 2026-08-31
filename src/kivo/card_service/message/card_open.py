from typing import Literal, TypedDict


class CardOpenRequestData(TypedDict):
    card: str


class CardOpenRequest(TypedDict):
    action: Literal["card_open"]
    data: CardOpenRequestData