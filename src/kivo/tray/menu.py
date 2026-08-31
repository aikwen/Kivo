from PySide6.QtCore import QEvent, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TrayMenu(QWidget):
    exit_requested = Signal()

    class Style:
        width = 180

        frame_background = "#202124"
        frame_border_color = "#3A3B3E"
        frame_border_width = 1
        frame_border_radius = 8

        shadow_margin = 12
        shadow_size = 10
        shadow_offset_y = 2
        shadow_max_alpha = 48

        content_margin = 6
        content_spacing = 2

        item_height = 34
        item_border_radius = 5
        item_padding_horizontal = 10

        text_color = "#F1F3F4"
        item_hover_background = "#34363A"
        item_pressed_background = "#292B2F"

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._init_window()
        self._init_ui()

    def _init_window(self) -> None:
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

    def _init_ui(self) -> None:
        self._container = QFrame(self)
        self._container.setObjectName("container")

        menu_layout = QVBoxLayout(
            self._container
        )
        menu_layout.setContentsMargins(
            self.Style.content_margin,
            self.Style.content_margin,
            self.Style.content_margin,
            self.Style.content_margin,
        )
        menu_layout.setSpacing(
            self.Style.content_spacing
        )

        self._exit_button = QPushButton(
            "Exit",
            self._container,
        )
        self._exit_button.setObjectName("menuItem")
        self._exit_button.setFixedHeight(
            self.Style.item_height
        )
        self._exit_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self._exit_button.clicked.connect(
            self._on_exit
        )

        menu_layout.addWidget(
            self._exit_button
        )

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(
            self.Style.shadow_margin,
            self.Style.shadow_margin,
            self.Style.shadow_margin,
            self.Style.shadow_margin,
        )
        root_layout.setSpacing(0)

        root_layout.addWidget(
            self._container
        )

        self.setStyleSheet(
            f"""
            QFrame#container {{
                background: {self.Style.frame_background};
                border: {self.Style.frame_border_width}px solid
                        {self.Style.frame_border_color};
                border-radius: {self.Style.frame_border_radius}px;
            }}

            QPushButton#menuItem {{
                color: {self.Style.text_color};
                background: transparent;
                border: none;
                border-radius: {self.Style.item_border_radius}px;
                padding: 0 {self.Style.item_padding_horizontal}px;
                text-align: left;
            }}

            QPushButton#menuItem:hover {{
                background: {self.Style.item_hover_background};
            }}

            QPushButton#menuItem:pressed {{
                background: {self.Style.item_pressed_background};
            }}
            """
        )

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True,
        )
        painter.setPen(
            Qt.PenStyle.NoPen
        )

        frame_rect = QRectF(
            self._container.geometry()
        )

        for spread in range(
            self.Style.shadow_size,
            0,
            -1,
        ):
            ratio = (
                spread
                / self.Style.shadow_size
            )

            alpha = int(
                self.Style.shadow_max_alpha
                * (1.0 - ratio) ** 2
            )

            shadow_rect = frame_rect.adjusted(
                -spread,
                -spread + self.Style.shadow_offset_y,
                spread,
                spread + self.Style.shadow_offset_y,
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
                self.Style.frame_border_radius + spread,
                self.Style.frame_border_radius + spread,
            )

    def event(self, event: QEvent) -> bool:
        if (
            event.type()
            == QEvent.Type.WindowDeactivate
        ):
            self.hide()

        return super().event(event)

    def _on_exit(self) -> None:
        self.hide()
        self.exit_requested.emit()