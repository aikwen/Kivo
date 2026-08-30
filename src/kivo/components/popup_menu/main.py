import sys

from PySide6.QtCore import QEvent, QPoint, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from kivo.resources.loader import resource_path

from .ui import MoreButton, PopupMenuUI


class PopupMenu(PopupMenuUI):
    settings_requested = Signal()
    hide_requested = Signal()
    exit_requested = Signal()

    def __init__(
        self,
        settings_enabled: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(
            settings_enabled=settings_enabled,
            parent=parent,
        )

        self.settings_button.clicked.connect(
            self._on_settings
        )
        self.hide_button.clicked.connect(
            self._on_hide
        )
        self.exit_button.clicked.connect(
            self._on_exit
        )

    def show_for(
        self,
        button: QWidget,
    ) -> None:
        self.adjustSize()

        anchor = button.mapToGlobal(
            button.rect().bottomRight()
        )

        position = QPoint(
            anchor.x() - self.width(),
            anchor.y() + 4,
        )

        self.move(position)

        self.show()
        self.raise_()
        self.activateWindow()

    def event(
        self,
        event: QEvent,
    ) -> bool:
        if event.type() == QEvent.Type.WindowDeactivate:
            self.hide()

        return super().event(event)

    def _on_settings(self) -> None:
        self.hide()
        self.settings_requested.emit()

    def _on_hide(self) -> None:
        self.hide()
        self.hide_requested.emit()

    def _on_exit(self) -> None:
        self.hide()
        self.exit_requested.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    window.resize(560, 360)

    window.setWindowFlags(
        Qt.WindowType.Tool
        | Qt.WindowType.FramelessWindowHint
        | Qt.WindowType.WindowStaysOnTopHint
    )

    with resource_path(
        "icons",
        "tray.ico",
    ) as icon_path:
        window.setWindowIcon(
            QIcon(str(icon_path))
        )

    window.setObjectName("card")

    window.setStyleSheet(
        """
        QWidget#card {
            background: #FFFFFF;
        }

        QWidget#title_bar {
            background: #FAFAFA;
            border-bottom: 1px solid #E5E5EA;
        }

        QLabel#title {
            color: #1C1C1E;
        }

        QLabel#content {
            color: #636366;
        }
        """
    )

    root_layout = QVBoxLayout(window)
    root_layout.setContentsMargins(
        0,
        0,
        0,
        0,
    )
    root_layout.setSpacing(0)

    title_bar = QWidget()
    title_bar.setObjectName(
        "title_bar"
    )
    title_bar.setFixedHeight(40)

    title_layout = QHBoxLayout(
        title_bar
    )
    title_layout.setContentsMargins(
        14,
        0,
        8,
        0,
    )
    title_layout.setSpacing(8)

    title = QLabel(
        "JSON Formatter"
    )
    title.setObjectName(
        "title"
    )

    more_button = MoreButton()

    title_layout.addWidget(
        title
    )
    title_layout.addStretch()
    title_layout.addWidget(
        more_button
    )

    content = QFrame()

    content_layout = QVBoxLayout(
        content
    )
    content_layout.setContentsMargins(
        16,
        16,
        16,
        16,
    )

    content_label = QLabel(
        "这里是 Card 的内容区域"
    )
    content_label.setObjectName(
        "content"
    )

    content_layout.addWidget(
        content_label
    )
    content_layout.addStretch()

    root_layout.addWidget(
        title_bar
    )
    root_layout.addWidget(
        content,
        1,
    )

    menu = PopupMenu(
        settings_enabled=False
    )

    more_button.clicked.connect(
        lambda: menu.show_for(
            more_button
        )
    )

    menu.settings_requested.connect(
        lambda: print("设置")
    )

    menu.hide_requested.connect(
        lambda: print("隐藏")
    )

    menu.exit_requested.connect(
        app.quit
    )

    window.show()

    sys.exit(app.exec())