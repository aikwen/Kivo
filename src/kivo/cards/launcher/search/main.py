import sys

from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QWidget

from .ui import SearchUI


class Search(SearchUI):
    text_changed = Signal(str)

    class Style:
        width = 570
        height = 57

        divider_width_ratio = 0.9
        divider_height = 1
        divider_color = "#444444"

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
            self.width() * Search.Style.divider_width_ratio
        )
        x = (self.width() - divider_width) // 2
        y = self.height() - Search.Style.divider_height

        painter.fillRect(
            x,
            y,
            divider_width,
            Search.Style.divider_height,
            QColor(Search.Style.divider_color),
        )

    def focus(self) -> None:
        self.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    search = Search()
    search.resize(
        Search.Style.width,
        Search.Style.height,
    )

    search.text_changed.connect(print)

    search.set_expanded(True)

    search.show()
    search.focus()

    sys.exit(app.exec())