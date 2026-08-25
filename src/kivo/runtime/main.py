import os
from typing import cast

from PySide6.QtWidgets import QApplication

from kivo.card_service.client import CardServiceClient
from kivo.card_service.message.card_list import (
    CardListRequest,
    CardListResponse,
)
from kivo.card_service.message.card_open import CardOpenRequest
from kivo.cards.launcher.main import LauncherWindow
from kivo.config.main import Config
from kivo.hotkey.global_hotkey import (
    DEFAULT_SHORTCUT,
    GlobalHotkey,
)
from kivo.runtime.debug_panel import DebugPanel
from kivo.tray.main import Tray
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

        shortcut = Config.get(
            "hotkey",
            "launcher",
            DEFAULT_SHORTCUT,
        )

        if not isinstance(shortcut, str):
            raise RuntimeError(
                "Invalid launcher hotkey configuration."
            )

        self.hotkey = GlobalHotkey(
            shortcut
        )

        self.card_service_client = CardServiceClient()

        self.debug_panel: DebugPanel | None = None

        self.card_service_client.message_received.connect(
            self._on_card_service_message
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
        self.card_service_client.start()

        request: CardListRequest = {
            "action": "card_list",
            "data": {},
        }
        self.card_service_client.send(request)

        self.app.installNativeEventFilter(
            self.hotkey.event_filter()
        )

        self.hotkey.register()
        self.tray.show()

        if os.getenv("KIVO_DEBUG") == "1":
            self.debug_panel = DebugPanel(self)
            self.debug_panel.show()

    def stop(self) -> None:
        self.hotkey.unregister()
        self.card_service_client.stop()

    def _on_card_service_message(
        self,
        message: object,
    ) -> None:
        if not isinstance(message, dict):
            return

        action = message.get("action")

        if action == "card_list":
            response = cast(
                CardListResponse,
                message,
            )
            self.launcher.set_cards(
                response["data"]
            )
            return

    def _open_card(
        self,
        card: str,
        isolated: bool,
    ) -> None:
        request: CardOpenRequest = {
            "action": "card_open",
            "data": {
                "card": card,
                "isolated": isolated,
            },
        }

        self.card_service_client.send(
            request
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