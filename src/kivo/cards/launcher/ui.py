from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QWidget,
)

from .card_list.main import CardList
from .search.main import Search


class LauncherWindowUI(QWidget):
    class Style:
        content_spacing = 4

        frame_background = "#202124"
        frame_border_color = "#444444"
        frame_border_width = 1
        frame_border_radius = 6

        shadow_margin = 12
        shadow_size = 10
        shadow_offset_y = 2
        shadow_max_alpha = 48

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.frame = QFrame(self)
        self.frame.setObjectName("launcherFrame")
        self.frame.setStyleSheet(
            f"""
            QFrame#launcherFrame {{
                background: {LauncherWindowUI.Style.frame_background};
                border: {LauncherWindowUI.Style.frame_border_width}px solid
                        {LauncherWindowUI.Style.frame_border_color};
                border-radius: {LauncherWindowUI.Style.frame_border_radius}px;
            }}
            """
        )

        self.search = Search(self.frame)
        self.search.setFixedHeight(Search.Style.height)

        self.card_list = CardList(self.frame)
        self.card_list.hide()

        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(
            LauncherWindowUI.Style.content_spacing
        )

        frame_layout.addWidget(self.search)
        frame_layout.addWidget(self.card_list)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            LauncherWindowUI.Style.shadow_margin,
            LauncherWindowUI.Style.shadow_margin,
            LauncherWindowUI.Style.shadow_margin,
            LauncherWindowUI.Style.shadow_margin,
        )
        layout.setSpacing(0)

        layout.addWidget(self.frame)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True,
        )
        painter.setPen(Qt.PenStyle.NoPen)

        frame_rect = QRectF(self.frame.geometry())

        for spread in range(
            LauncherWindowUI.Style.shadow_size,
            0,
            -1,
        ):
            ratio = (
                spread
                / LauncherWindowUI.Style.shadow_size
            )

            alpha = int(
                LauncherWindowUI.Style.shadow_max_alpha
                * (1.0 - ratio) ** 2
            )

            shadow_rect = frame_rect.adjusted(
                -spread,
                -spread + LauncherWindowUI.Style.shadow_offset_y,
                spread,
                spread + LauncherWindowUI.Style.shadow_offset_y,
            )

            painter.setBrush(
                QColor(
                    0,
                    0,
                    0,
                    alpha,
                )
            )

            painter.drawRoundedRect(
                shadow_rect,
                LauncherWindowUI.Style.frame_border_radius + spread,
                LauncherWindowUI.Style.frame_border_radius + spread,
            )