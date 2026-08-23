import queue
import subprocess
import sys
import threading
from typing import Any

from PySide6.QtCore import QObject, Signal

from .ipc.json_channel import JsonChannel


_STOP = object()


class CardServiceClient(QObject):
    message_received = Signal(object)

    def __init__(self) -> None:
        super().__init__()

        self._process: subprocess.Popen[str] | None = None
        self._channel: JsonChannel | None = None

        self._send_queue: queue.Queue[Any] = queue.Queue()

        self._reader_thread: threading.Thread | None = None
        self._writer_thread: threading.Thread | None = None

        self._running = False

    def start(self) -> None:
        if self._running:
            return

        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "kivo.card_service.service",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
            text=True,
            bufsize=1,
        )

        if process.stdin is None or process.stdout is None:
            process.terminate()
            raise RuntimeError("Failed to create CardService IPC pipes.")

        self._process = process
        self._channel = JsonChannel(
            reader=process.stdout,
            writer=process.stdin,
        )

        self._running = True

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
        if not self._running:
            raise RuntimeError("CardServiceClient is not running.")

        self._send_queue.put(message)

    def stop(self) -> None:
        if not self._running:
            return

        self._running = False

        process = self._process
        reader_thread = self._reader_thread
        writer_thread = self._writer_thread

        self._send_queue.put(_STOP)

        if writer_thread is not None:
            writer_thread.join()

        if process is not None:
            if process.stdin is not None:
                process.stdin.close()

            process.wait()

        if reader_thread is not None:
            reader_thread.join()

        self._process = None
        self._channel = None
        self._reader_thread = None
        self._writer_thread = None

    def _write_messages(self) -> None:
        channel = self._channel
        if channel is None:
            return

        while True:
            message = self._send_queue.get()

            if message is _STOP:
                return

            channel.send(message)

    def _read_messages(self) -> None:
        channel = self._channel
        if channel is None:
            return

        while True:
            message = channel.recv()

            if message is None:
                return

            self.message_received.emit(message)