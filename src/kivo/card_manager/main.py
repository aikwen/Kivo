import sys

from kivo.ipc.json_channel import JsonChannel
from kivo.ipc.message_type import MessageType

class CardManager:
    def cards(self) -> list[str]:
        return [
            "JSON Formatter",
            "JWT Viewer",
            "Color Converter",
            "Calendar",
            "Timestamp Converter",
        ]

    def open_card(self, card: str) -> bool:
        return True


def run() -> int:
    manager = CardManager()

    channel = JsonChannel(
        reader=sys.stdin,
        writer=sys.stdout,
    )

    channel.send(
        {
            "type": MessageType.CARDS,
            "cards": manager.cards(),
        }
    )

    while True:
        message = channel.recv()

        if message is None:
            break

        if message.get("type") == MessageType.OPEN_CARD:
            manager.open_card(message["card"])

    return 0


if __name__ == "__main__":
    raise SystemExit(run())