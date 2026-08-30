from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MoreButton(QPushButton):
    class Style:
        size = 28
        radius = 6

        dot_radius = 1.5
        dot_spacing = 5

        dot_color = "#3A3A3C"

        hover_background = "#F5F5F5"
        pressed_background = "#EAEAEA"

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setFixedSize(
            self.Style.size,
            self.Style.size,
        )

        self.setStyleSheet(
            f"""
            QPushButton {{
                border: none;
                border-radius: {self.Style.radius}px;
                background: transparent;
            }}

            QPushButton:hover {{
                background: {self.Style.hover_background};
            }}

            QPushButton:pressed {{
                background: {self.Style.pressed_background};
            }}
            """
        )

    def paintEvent(
        self,
        event: QPaintEvent,
    ) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )
        painter.setBrush(
            QColor(self.Style.dot_color)
        )

        center = self.rect().center()

        for offset in (
            -self.Style.dot_spacing,
            0,
            self.Style.dot_spacing,
        ):
            painter.drawEllipse(
                QPointF(
                    center.x() + offset,
                    center.y(),
                ),
                self.Style.dot_radius,
                self.Style.dot_radius,
            )


class PopupMenuUI(QWidget):
    class Style:
        width = 128

        frame_background = "#FFFFFF"
        frame_border_color = "#E5E5EA"
        frame_border_width = 1
        frame_radius = 10

        shadow_margin = 12
        shadow_blur_radius = 22
        shadow_offset_y = 1
        shadow_alpha = 18

        content_margin = 6
        content_spacing = 0

        item_height = 36
        item_radius = 7
        item_padding_x = 12

        text_color = "#1C1C1E"

        item_hover_background = "#F5F5F5"
        item_pressed_background = "#EAEAEA"

    def __init__(
        self,
        settings_enabled: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setFixedWidth(
            self.Style.width
            + self.Style.shadow_margin * 2
        )

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(
            self.Style.shadow_margin,
            self.Style.shadow_margin,
            self.Style.shadow_margin,
            self.Style.shadow_margin,
        )

        self.frame = QFrame(self)
        self.frame.setObjectName(
            "popup_menu_frame"
        )

        self.frame.setStyleSheet(
            f"""
            QFrame#popup_menu_frame {{
                background: {self.Style.frame_background};
                border: {self.Style.frame_border_width}px
                    solid {self.Style.frame_border_color};
                border-radius: {self.Style.frame_radius}px;
            }}
            """
        )

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(
            self.Style.shadow_blur_radius
        )
        shadow.setOffset(
            0,
            self.Style.shadow_offset_y,
        )
        shadow.setColor(
            QColor(
                0,
                0,
                0,
                self.Style.shadow_alpha,
            )
        )

        self.frame.setGraphicsEffect(
            shadow
        )

        root_layout.addWidget(
            self.frame
        )

        self.content_layout = QVBoxLayout(
            self.frame
        )
        self.content_layout.setContentsMargins(
            self.Style.content_margin,
            self.Style.content_margin,
            self.Style.content_margin,
            self.Style.content_margin,
        )
        self.content_layout.setSpacing(
            self.Style.content_spacing
        )

        self.settings_button = self._create_item(
            "设置"
        )
        self.hide_button = self._create_item(
            "隐藏"
        )
        self.exit_button = self._create_item(
            "退出"
        )

        self.settings_button.setVisible(
            settings_enabled
        )

        self.content_layout.addWidget(
            self.settings_button
        )
        self.content_layout.addWidget(
            self.hide_button
        )
        self.content_layout.addWidget(
            self.exit_button
        )

    def _create_item(
        self,
        text: str,
    ) -> QPushButton:
        button = QPushButton(text)

        button.setFixedHeight(
            self.Style.item_height
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setStyleSheet(
            f"""
            QPushButton {{
                border: none;
                border-radius: {self.Style.item_radius}px;

                padding-left: {self.Style.item_padding_x}px;
                padding-right: {self.Style.item_padding_x}px;

                text-align: left;

                color: {self.Style.text_color};
                background: transparent;
            }}

            QPushButton:hover {{
                background: {self.Style.item_hover_background};
            }}

            QPushButton:pressed {{
                background: {self.Style.item_pressed_background};
            }}
            """
        )

        return button