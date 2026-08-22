import queue
import subprocess
import sys
import threading
from typing import Any

from PySide6.QtCore import QObject, QTimer, Signal

from kivo.ipc.json_channel import JsonChannel


class CardClient(QObject):
    message_received = Signal(object)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._process: subprocess.Popen[str] | None = None
        self._channel: JsonChannel | None = None

        self._messages: queue.Queue[Any] = queue.Queue()
        self._reader_thread: threading.Thread | None = None

        self._message_timer = QTimer(self)
        self._message_timer.setInterval(20)
        self._message_timer.timeout.connect(
            self._process_messages
        )

    def start(self) -> None:
        if self._process is not None:
            return

        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "kivo.card_manager.main",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )

        if process.stdin is None or process.stdout is None:
            process.terminate()
            raise RuntimeError(
                "Failed to create Host communication pipes."
            )

        self._process = process
        self._channel = JsonChannel(
            reader=process.stdout,
            writer=process.stdin,
        )

        self._reader_thread = threading.Thread(
            target=self._read_messages,
            daemon=True,
        )
        self._reader_thread.start()

        self._message_timer.start()

    def stop(self) -> None:
        self._message_timer.stop()

        process = self._process

        if process is None:
            return

        if process.stdin is not None:
            process.stdin.close()

        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait()

        self._process = None
        self._channel = None
        self._reader_thread = None

    def send(self, message: Any) -> None:
        channel = self._channel

        if channel is None:
            return

        channel.send(message)

    def _read_messages(self) -> None:
        channel = self._channel

        if channel is None:
            return

        while True:
            message = channel.recv()

            if message is None:
                break

            self._messages.put(message)

    def _process_messages(self) -> None:
        while True:
            try:
                message = self._messages.get_nowait()
            except queue.Empty:
                break

            self.message_received.emit(message)