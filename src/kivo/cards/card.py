import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizeGrip,
    QVBoxLayout,
    QWidget,
)

from kivo.components.title_bar.main import TitleBar
from kivo.resources.loader import resource_path


class Card(QWidget):
    settings_requested = Signal()
    hide_requested = Signal()
    exit_requested = Signal()

    class Style:
        frame_background = "#FFFFFF"
        frame_radius = 8

        shadow_margin = 12
        shadow_size = 8
        shadow_offset_y = 1
        shadow_max_alpha = 16

        min_width = 360
        min_height = 240

        size_grip_size = 16

    def __init__(
        self,
        title: str = "",
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

        self.setMinimumSize(
            self.Style.min_width,
            self.Style.min_height,
        )

        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(
            self.Style.shadow_margin,
            self.Style.shadow_margin,
            self.Style.shadow_margin,
            self.Style.shadow_margin,
        )
        self.root_layout.setSpacing(0)

        self.frame = QFrame(self)
        self.frame.setObjectName("card_frame")
        self.frame.setStyleSheet(
            f"""
            QFrame#card_frame {{
                background: {self.Style.frame_background};
                border: none;
                border-radius: {self.Style.frame_radius}px;
            }}
            """
        )

        self.root_layout.addWidget(self.frame)

        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.frame_layout.setSpacing(0)

        self.title_bar = TitleBar(
            title=title,
            settings_enabled=settings_enabled,
            parent=self.frame,
        )

        self.content = QWidget(self.frame)

        self.content_layout = QVBoxLayout(
            self.content
        )
        self.content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.content_layout.setSpacing(0)

        self.resize_bar = QWidget(self.frame)

        self.resize_layout = QHBoxLayout(
            self.resize_bar
        )
        self.resize_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.resize_layout.setSpacing(0)

        self.size_grip = QSizeGrip(
            self.frame
        )
        self.size_grip.setFixedSize(
            self.Style.size_grip_size,
            self.Style.size_grip_size,
        )

        self.size_grip.setStyleSheet(
            """
            QSizeGrip {
                background: transparent;
            }
            """
        )

        self.resize_layout.addStretch()
        self.resize_layout.addWidget(
            self.size_grip
        )

        self.frame_layout.addWidget(
            self.title_bar
        )
        self.frame_layout.addWidget(
            self.content,
            1,
        )
        self.frame_layout.addWidget(
            self.resize_bar
        )

        self.title_bar.settings_requested.connect(
            self.settings_requested.emit
        )

        self.title_bar.hide_requested.connect(
            self.hide_requested.emit
        )

        self.title_bar.exit_requested.connect(
            self.exit_requested.emit
        )

    def paintEvent(
        self,
        event,
    ) -> None:
        super().paintEvent(event)

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True,
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        frame_rect = self.frame.geometry()

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
                self.Style.frame_radius + spread,
                self.Style.frame_radius + spread,
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    card = Card(
        title="JSON Formatter",
        settings_enabled=True,
    )

    card.setWindowFlags(
        Qt.WindowType.Window
        | Qt.WindowType.FramelessWindowHint
        | Qt.WindowType.WindowStaysOnTopHint
    )

    card.resize(
        560,
        360,
    )

    with resource_path(
        "icons",
        "tray.ico",
    ) as icon_path:
        card.setWindowIcon(
            QIcon(str(icon_path))
        )

    content_label = QLabel(
        "这里是 Card 的内容区域"
    )

    content_label.setStyleSheet(
        """
        QLabel {
            color: #636366;
            padding: 16px;
        }
        """
    )

    card.content_layout.addWidget(
        content_label
    )

    card.content_layout.addStretch()

    card.settings_requested.connect(
        lambda: print("设置")
    )

    card.hide_requested.connect(
        card.showMinimized
    )

    card.exit_requested.connect(
        card.close
    )

    card.exit_requested.connect(
        app.quit
    )

    card.show()

    sys.exit(app.exec())