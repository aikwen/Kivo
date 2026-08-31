from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
)

from kivo.components.popup_menu.ui import MoreButton


class TitleBarUI(QWidget):
    class Style:
        height = 40

        background = "#FAFAFA"
        border_color = "#E5E5EA"
        border_width = 1

        padding_left = 14
        padding_right = 8
        spacing = 8

        text_color = "#1C1C1E"

    def __init__(
        self,
        title: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setFixedHeight(
            self.Style.height
        )

        self.setObjectName(
            "title_bar"
        )

        self.setStyleSheet(
            f"""
            QWidget#title_bar {{
                background: {self.Style.background};
                border: none;
                border-bottom: {self.Style.border_width}px
                    solid {self.Style.border_color};
            }}

            QLabel#title {{
                color: {self.Style.text_color};
                background: transparent;
                border: none;
            }}
            """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            self.Style.padding_left,
            0,
            self.Style.padding_right,
            0,
        )
        layout.setSpacing(
            self.Style.spacing
        )

        self.title_label = QLabel(title)
        self.title_label.setObjectName(
            "title"
        )

        self.more_button = MoreButton()

        layout.addWidget(
            self.title_label
        )
        layout.addStretch()
        layout.addWidget(
            self.more_button
        )