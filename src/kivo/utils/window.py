from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication, QWidget


def move_widget_to_cursor_screen(
    widget: QWidget,
    x_ratio: float,
    y_ratio: float,
) -> None:
    screen = QApplication.screenAt(QCursor.pos())

    if screen is None:
        screen = QApplication.primaryScreen()

    if screen is None:
        return

    geometry = screen.availableGeometry()

    x = geometry.x() + int(
        geometry.width() * x_ratio
    )
    y = geometry.y() + int(
        geometry.height() * y_ratio
    )

    widget.move(x, y)