import sys

from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication, QWidget

from .search.main import Search
from .ui import LauncherWindowUI


class LauncherWindow(LauncherWindowUI):
    card_activated = Signal(str, bool)

    class Style:
        width = Search.Style.width
        height = (
            Search.Style.height
            + LauncherWindowUI.Style.frame_border_width * 2
            + LauncherWindowUI.Style.shadow_margin * 2
        )

        x_ratio = 0.41
        y_ratio = 0.34

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._cards: list[str] = []

        self.search.textChanged.connect(self._on_search_changed)
        self.search.installEventFilter(self)

        self.card_list.activated.connect(
            lambda card: self.card_activated.emit(card, False)
        )

    def set_cards(self, cards: list[str]) -> None:
        self._cards = sorted(
            cards,
            key=lambda card: card.lower(),
        )

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
            self.search.clear()
            self.hide()

    def eventFilter(
        self,
        watched: QObject,
        event: QEvent,
    ) -> bool:
        if (
            watched is self.search
            and event.type() == QEvent.Type.KeyPress
        ):
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
                    modifiers = key_event.modifiers()

                    isolated = bool(
                        modifiers
                        & Qt.KeyboardModifier.ControlModifier
                        and modifiers
                        & Qt.KeyboardModifier.AltModifier
                    )

                    self._activate_current_card(isolated)
                    return True

                if key == Qt.Key.Key_Escape:
                    self.search.clear()
                    self.hide()
                    return True

        return super().eventFilter(watched, event)

    def _on_search_changed(self, text: str) -> None:
        query = text.strip().lower()

        if not query:
            self.card_list.set_cards(self._cards)
            self.search.set_expanded(bool(self._cards))
            self._update_height()
            return

        results = [
            card
            for card in self._cards
            if query in card.lower()
        ]

        self.card_list.set_cards(results)
        self.search.set_expanded(bool(results))

        self._update_height()

    def _update_height(self) -> None:
        frame_height = (
            Search.Style.height
            + LauncherWindowUI.Style.frame_border_width * 2
        )

        if not self.card_list.isHidden():
            frame_height += (
                LauncherWindowUI.Style.content_spacing
            )
            frame_height += self.card_list.height()

        window_height = (
            frame_height
            + LauncherWindowUI.Style.shadow_margin * 2
        )

        self.frame.setFixedHeight(frame_height)
        self.setFixedHeight(window_height)

        frame_layout = self.frame.layout()
        if frame_layout is not None:
            frame_layout.activate()

        window_layout = self.layout()
        if window_layout is not None:
            window_layout.activate()

    def _activate_current_card(
        self,
        isolated: bool,
    ) -> None:
        card = self.card_list.current_card()

        if card is None:
            return

        self.card_activated.emit(card, isolated)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LauncherWindow()
    window.resize(
        LauncherWindow.Style.width,
        LauncherWindow.Style.height,
    )

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
        lambda card, isolated: print(
            f"activate: {card}, isolated: {isolated}"
        )
    )

    window.show()

    app.lastWindowClosed.connect(app.quit)

    sys.exit(app.exec())