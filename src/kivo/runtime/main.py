from PySide6.QtWidgets import QApplication

from kivo.cards.launcher.main import LauncherWindow
from kivo.hotkey.main import GlobalHotkey
from kivo.runtime.card_client import CardClient
from kivo.tray.main import Tray
from kivo.ipc.message_type import MessageType
from kivo.utils.window import move_widget_to_cursor_screen


class KivoRuntime:
    def __init__(self, app: QApplication) -> None:
        self.app = app

        self.launcher = LauncherWindow()
        self.launcher.resize(
            LauncherWindow.Style.width,
            LauncherWindow.Style.height,
        )

        self.tray = Tray()
        self.hotkey = GlobalHotkey()
        self.card_client = CardClient()

        self.card_client.message_received.connect(
            self._on_card_message
        )

        self.launcher.card_activated.connect(
            self._open_card
        )

        self.tray.activated.connect(
            self._toggle_launcher
        )
        self.tray.exit_requested.connect(
            self.app.quit
        )

        self.hotkey.activated.connect(
            self._toggle_launcher
        )

    def start(self) -> None:
        self.card_client.start()

        self.app.installNativeEventFilter(
            self.hotkey.event_filter()
        )

        self.hotkey.register()
        self.tray.show()

    def stop(self) -> None:
        self.hotkey.unregister()
        self.card_client.stop()

    def _on_card_message(self, message: object) -> None:
        if not isinstance(message, dict):
            return

        message_type = message.get("type")

        if message_type == MessageType.CARDS:
            cards = message.get("cards")

            if isinstance(cards, list):
                self.launcher.set_cards(cards)

    def _open_card(self, card: str) -> None:
        self.card_client.send(
            {
                "type": MessageType.OPEN_CARD,
                "card": card,
            }
        )

    def show_launcher(self) -> None:
        move_widget_to_cursor_screen(
            self.launcher,
            LauncherWindow.Style.x_ratio,
            LauncherWindow.Style.y_ratio,
        )

        self.launcher.show()
        self.launcher.raise_()
        self.launcher.activateWindow()

    def _toggle_launcher(self) -> None:
        if self.launcher.isVisible():
            self.launcher.hide()
            return

        self.show_launcher()