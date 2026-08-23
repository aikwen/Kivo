from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget


class Card(QWidget):
    def __init__(
        self,
        isolated: bool,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.isolated = isolated

        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

    def closeEvent(
        self,
        event: QCloseEvent,
    ) -> None:
        if self.isolated:
            super().closeEvent(event)
            return

        event.ignore()
        self.hide()