import sys

from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication, QWidget

from .ui import (
    CONTENT_SPACING,
    FRAME_BORDER_WIDTH,
    SEARCH_HEIGHT,
    SHADOW_MARGIN,
    LauncherWindowUI,
)


LAUNCHER_X_RATIO = 0.41
LAUNCHER_Y_RATIO = 0.34


class LauncherWindow(LauncherWindowUI):
    card_activated = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._cards: list[str] = []

        self.search.textChanged.connect(self._on_search_changed)
        self.search.installEventFilter(self)

        self.card_list.activated.connect(self.card_activated)

    def set_cards(self, cards: list[str]) -> None:
        self._cards = cards

        # Card registry 更新后，按照当前 query 重新过滤。
        self._on_search_changed(self.search.text())

    def showEvent(self, event) -> None:
        super().showEvent(event)

        self.raise_()
        self.activateWindow()

        self.search.setFocus(
            Qt.FocusReason.ActiveWindowFocusReason
        )
        self.search.selectAll()

    def changeEvent(self, event) -> None:
        super().changeEvent(event)

        if (
                event.type() == QEvent.Type.ActivationChange
                and not self.isActiveWindow()
        ):
            self.hide()

    def eventFilter(
        self,
        watched: QObject,
        event: QEvent,
    ) -> bool:
        if watched is self.search and event.type() == QEvent.Type.KeyPress:
            key_event = event

            if isinstance(key_event, QKeyEvent):
                key = key_event.key()

                if key == Qt.Key.Key_Down:
                    self.card_list.select_next()
                    return True

                if key == Qt.Key.Key_Up:
                    self.card_list.select_previous()
                    return True

                if key in (
                    Qt.Key.Key_Return,
                    Qt.Key.Key_Enter,
                ):
                    self._activate_current_card()
                    return True

                if key == Qt.Key.Key_Escape:
                    self.hide()
                    return True

        return super().eventFilter(watched, event)

    def _on_search_changed(self, text: str) -> None:
        query = text.strip().lower()

        if not query:
            self.card_list.set_cards([])
            self.search.set_expanded(False)
            self._update_height()
            return

        results = [
            card
            for card in self._cards
            if query in card.lower()
        ]

        has_results = bool(results)

        self.card_list.set_cards(results)
        self.search.set_expanded(has_results)

        self._update_height()

    def _update_height(self) -> None:
        frame_height = (
            SEARCH_HEIGHT
            + FRAME_BORDER_WIDTH * 2
        )

        if self.card_list.isVisible():
            frame_height += CONTENT_SPACING
            frame_height += self.card_list.height()

        window_height = (
            frame_height
            + SHADOW_MARGIN * 2
        )

        self.frame.setFixedHeight(frame_height)
        self.setFixedHeight(window_height)

        frame_layout = self.frame.layout()
        if frame_layout is not None:
            frame_layout.activate()

        window_layout = self.layout()
        if window_layout is not None:
            window_layout.activate()

    def _activate_current_card(self) -> None:
        card = self.card_list.current_card()

        if card is None:
            return

        self.card_activated.emit(card)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LauncherWindow()
    window.resize(
        570,
        SEARCH_HEIGHT
        + FRAME_BORDER_WIDTH * 2
        + SHADOW_MARGIN * 2,
    )

    screen = app.primaryScreen()
    if screen is not None:
        geometry = screen.availableGeometry()

        x = geometry.x() + int(
            geometry.width() * LAUNCHER_X_RATIO
        )
        y = geometry.y() + int(
            geometry.height() * LAUNCHER_Y_RATIO
        )

        window.move(x, y)

    window.set_cards(
        [
            "JSON Formatter",
            "JWT Viewer",
            "Color Converter",
            "Calendar",
            "Timestamp Converter",
            "Base64",
            "UUID Generator",
            "Hash Calculator",
            "Regular Expression",
            "Environment Variables",
        ]
    )

    window.card_activated.connect(
        lambda card: print(f"activate: {card}")
    )

    window.show()

    app.lastWindowClosed.connect(app.quit)

    sys.exit(app.exec())