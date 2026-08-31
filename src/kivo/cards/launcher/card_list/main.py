import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QWidget

from .ui import CardListUI


class CardList(CardListUI):
    activated = Signal(str)

    class Style:
        width = 570
        max_visible_items = 8

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.doubleClicked.connect(self._on_activated)

    def set_cards(self, cards: list[str]) -> None:
        self.card_model.set_cards(cards)

        self._adjust_height()
        self.select_first()

    def current_card(self) -> str | None:
        return self.card_model.card(self.currentIndex())

    def select_first(self) -> None:
        if self.card_model.rowCount() == 0:
            self.clearSelection()
            return

        self.scrollToTop()

        index = self.card_model.index(0)
        self.setCurrentIndex(index)

    def select_next(self) -> None:
        count = self.card_model.rowCount()
        if count == 0:
            return

        current = self.currentIndex().row()
        next_row = min(current + 1, count - 1)

        index = self.card_model.index(next_row)
        self.setCurrentIndex(index)
        self.scrollTo(index)

    def select_previous(self) -> None:
        count = self.card_model.rowCount()
        if count == 0:
            return

        current = self.currentIndex().row()
        previous_row = max(current - 1, 0)

        index = self.card_model.index(previous_row)
        self.setCurrentIndex(index)
        self.scrollTo(index)

    def _adjust_height(self) -> None:
        count = self.card_model.rowCount()

        if count == 0:
            self.setFixedHeight(0)
            self.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )
            self.hide()
            return

        visible_count = min(count, CardList.Style.max_visible_items)
        item_height = self.card_delegate.Style.item_height

        self.setFixedHeight(
            visible_count * item_height
        )

        if count > CardList.Style.max_visible_items:
            self.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOn
            )
        else:
            self.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )

        self.show()

    def _on_activated(self) -> None:
        card = self.current_card()

        if card is not None:
            self.activated.emit(card)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    card_list = CardList()
    card_list.resize(CardList.Style.width, 0)

    card_list.set_cards(
        [
            "JSON Formatter",
            "JWT Viewer",
            "Color Converter",
            "Calendar",
            "Timestamp Converter",
            "Base64",
            "UUID",
            "Hash",
            "Regular Expression",
            "Environment Variables",
        ]
    )

    card_list.activated.connect(print)

    card_list.show()

    sys.exit(app.exec())