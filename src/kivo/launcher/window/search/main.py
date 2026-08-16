import sys

from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QWidget

from .ui import SearchUI


DIVIDER_WIDTH_RATIO = 0.9
DIVIDER_HEIGHT = 1
DIVIDER_COLOR = "#444444"


class Search(SearchUI):
    text_changed = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._expanded = False

        self.textChanged.connect(self.text_changed)

    def set_expanded(self, expanded: bool) -> None:
        if self._expanded == expanded:
            return

        self._expanded = expanded
        self.update()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        if not self._expanded:
            return

        painter = QPainter(self)

        divider_width = round(
            self.width() * DIVIDER_WIDTH_RATIO
        )
        x = (self.width() - divider_width) // 2
        y = self.height() - DIVIDER_HEIGHT

        painter.fillRect(
            x,
            y,
            divider_width,
            DIVIDER_HEIGHT,
            QColor(DIVIDER_COLOR),
        )

    def focus(self) -> None:
        self.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    search = Search()
    search.resize(570, 57)

    search.text_changed.connect(print)

    search.set_expanded(True)

    search.show()
    search.focus()

    sys.exit(app.exec())