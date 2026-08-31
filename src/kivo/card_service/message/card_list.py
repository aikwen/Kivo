from typing import Literal, TypedDict


class CardListRequest(TypedDict):
    action: Literal["card_list"]
    data: dict


class CardListResponse(TypedDict):
    action: Literal["card_list"]
    data: list[str]