from collections import deque
from typing import Any, TYPE_CHECKING

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from kivo.cards.collection import CardCollection

if TYPE_CHECKING:
    from kivo.runtime.main import KivoRuntime


class DebugPanel(QWidget):
    refresh_interval = 1000
    max_messages = 100

    def __init__(
        self,
        runtime: "KivoRuntime",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._runtime = runtime

        self._messages: deque[str] = deque(
            maxlen=self.max_messages
        )

        self._init_window()
        self._init_ui()
        self._init_connections()

        self._timer = QTimer(self)
        self._timer.setInterval(self.refresh_interval)
        self._timer.timeout.connect(self._refresh)
        self._timer.start()

        self._refresh()

    def _init_window(self) -> None:
        self.setWindowTitle("Kivo Debug")

        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        self.resize(460, 520)

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        runtime_group = QGroupBox("Runtime")
        runtime_layout = QFormLayout(runtime_group)

        self._launcher_visible = QLabel()
        self._hotkey_registered = QLabel()

        runtime_layout.addRow(
            "Launcher visible",
            self._launcher_visible,
        )
        runtime_layout.addRow(
            "Hotkey registered",
            self._hotkey_registered,
        )

        service_group = QGroupBox("Card Service")
        service_layout = QFormLayout(service_group)

        self._service_pid = QLabel()
        self._service_alive = QLabel()
        self._reader_alive = QLabel()
        self._writer_alive = QLabel()
        self._send_queue_size = QLabel()

        service_layout.addRow(
            "PID",
            self._service_pid,
        )
        service_layout.addRow(
            "Process alive",
            self._service_alive,
        )
        service_layout.addRow(
            "Reader thread",
            self._reader_alive,
        )
        service_layout.addRow(
            "Writer thread",
            self._writer_alive,
        )
        service_layout.addRow(
            "Send queue",
            self._send_queue_size,
        )

        cards_group = QGroupBox("Cards")
        cards_layout = QFormLayout(cards_group)

        self._registered_cards = QLabel()

        cards_layout.addRow(
            "Registered",
            self._registered_cards,
        )

        messages_group = QGroupBox("Messages")
        messages_layout = QVBoxLayout(messages_group)

        self._message_log = QPlainTextEdit()
        self._message_log.setReadOnly(True)

        messages_layout.addWidget(self._message_log)

        layout.addWidget(runtime_group)
        layout.addWidget(service_group)
        layout.addWidget(cards_group)
        layout.addWidget(messages_group)

    def _init_connections(self) -> None:
        self._runtime.card_service_client.message_received.connect(
            self._on_message_received
        )

    def _refresh(self) -> None:
        self._launcher_visible.setText(
            self._bool_text(
                self._runtime.launcher.isVisible()
            )
        )

        self._hotkey_registered.setText(
            self._bool_text(
                self._runtime.hotkey._registered
            )
        )

        client = self._runtime.card_service_client

        process = client._process

        if process is None:
            self._service_pid.setText("-")
            self._service_alive.setText("No")
        else:
            self._service_pid.setText(str(process.pid))
            self._service_alive.setText(
                self._bool_text(
                    process.poll() is None
                )
            )

        self._reader_alive.setText(
            self._thread_status(
                client._reader_thread
            )
        )

        self._writer_alive.setText(
            self._thread_status(
                client._writer_thread
            )
        )

        self._send_queue_size.setText(
            str(client._send_queue.qsize())
        )

        self._registered_cards.setText(
            str(len(CardCollection.list()))
        )

    def _on_message_received(
        self,
        message: Any,
    ) -> None:
        self._messages.append(
            f"<- {message!r}"
        )

        self._message_log.setPlainText(
            "\n".join(self._messages)
        )

        scrollbar = self._message_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @staticmethod
    def _bool_text(value: bool) -> str:
        return "Yes" if value else "No"

    @staticmethod
    def _thread_status(thread: Any) -> str:
        if thread is None:
            return "-"

        return (
            "Alive"
            if thread.is_alive()
            else "Stopped"
        )