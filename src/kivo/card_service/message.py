from enum import StrEnum
from typing import Any, TypedDict


class Event(StrEnum):
    CARD_LIST = "card_list"
    CARD_OPEN = "card_open"


class Message(TypedDict):
    event: Event
    data: dict[str, Any]


class CardListData(TypedDict):
    cards: list[str]


class CardOpenData(TypedDict):
    card: str
    isolated: bool