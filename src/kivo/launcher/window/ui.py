from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QWidget,
)

from .card_list.main import CardList
from .search.main import Search


SEARCH_HEIGHT = 57
CONTENT_SPACING = 4

FRAME_BACKGROUND = "#202124"
FRAME_BORDER_COLOR = "#444444"
FRAME_BORDER_WIDTH = 1
FRAME_BORDER_RADIUS = 6

WINDOW_MARGIN = 2


class LauncherWindowUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.frame = QFrame(self)
        self.frame.setObjectName("launcherFrame")
        self.frame.setStyleSheet(
            f"""
            QFrame#launcherFrame {{
                background: {FRAME_BACKGROUND};
                border: {FRAME_BORDER_WIDTH}px solid {FRAME_BORDER_COLOR};
                border-radius: {FRAME_BORDER_RADIUS}px;
            }}
            """
        )

        self.search = Search(self.frame)
        self.search.setFixedHeight(SEARCH_HEIGHT)

        self.card_list = CardList(self.frame)
        self.card_list.hide()

        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(CONTENT_SPACING)

        frame_layout.addWidget(self.search)
        frame_layout.addWidget(self.card_list)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            WINDOW_MARGIN,
            WINDOW_MARGIN,
            WINDOW_MARGIN,
            WINDOW_MARGIN,
        )
        layout.setSpacing(0)

        layout.addWidget(self.frame)