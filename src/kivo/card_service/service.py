import queue
import sys
import threading
from typing import Any, cast

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

from kivo.card_service.card_manager import CardManager
from kivo.card_service.message.card_list import (
    CardListRequest,
    CardListResponse,
)
from kivo.card_service.message.card_open import CardOpenRequest
from kivo.cards.collection import CardCollection
from kivo.log import Log

from .ipc.json_channel import JsonChannel


_STOP = object()


class CardService(QObject):
    message_received = Signal(object)
    disconnected = Signal()

    def __init__(self) -> None:
        super().__init__()

        self._logger = Log.kivo()

        self._channel = JsonChannel(
            reader=sys.stdin,
            writer=sys.stdout,
        )

        self._send_queue: queue.Queue[Any] = queue.Queue()

        self._reader_thread: threading.Thread | None = None
        self._writer_thread: threading.Thread | None = None

        self._card_manager = CardManager()

        self.message_received.connect(
            self._handle_message
        )
        self.disconnected.connect(
            QApplication.quit
        )

    def start(self) -> None:
        self._reader_thread = threading.Thread(
            target=self._read_messages,
            name="kivo-card-service-reader",
        )
        self._writer_thread = threading.Thread(
            target=self._write_messages,
            name="kivo-card-service-writer",
        )

        self._reader_thread.start()
        self._writer_thread.start()

    def send(self, message: Any) -> None:
        self._send_queue.put(message)

    def stop(self) -> None:
        self._send_queue.put(_STOP)

        if self._writer_thread is not None:
            self._writer_thread.join()

        if self._reader_thread is not None:
            self._reader_thread.join()

    def _read_messages(self) -> None:
        try:
            while True:
                message = self._channel.recv()

                if message is None:
                    self.disconnected.emit()
                    return

                self.message_received.emit(message)

        except Exception:
            self._logger.exception(
                "CardService reader failed."
            )
            self.disconnected.emit()

    def _write_messages(self) -> None:
        try:
            while True:
                message = self._send_queue.get()

                if message is _STOP:
                    return

                self._channel.send(message)

        except Exception:
            self._logger.exception(
                "CardService writer failed."
            )

    def _handle_message(
        self,
        message: Any,
    ) -> None:
        if not isinstance(message, dict):
            return

        action = message.get("action")

        if action == "card_list":
            self._handle_card_list(
                cast(CardListRequest, message)
            )
            return

        if action == "card_open":
            self._handle_card_open(
                cast(CardOpenRequest, message)
            )

    def _handle_card_list(
        self,
        request: CardListRequest,
    ) -> None:
        response: CardListResponse = {
            "action": "card_list",
            "data": CardCollection.list(),
        }

        self.send(response)

    def _handle_card_open(
        self,
        request: CardOpenRequest,
    ) -> None:
        card_id = request["data"]["card"]

        self._card_manager.open(
            card_id
        )


def run() -> None:
    app = QApplication(sys.argv)

    service = CardService()
    service.start()

    app.exec()

    service.stop()


if __name__ == "__main__":
    run()