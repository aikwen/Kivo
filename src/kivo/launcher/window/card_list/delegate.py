from dataclasses import dataclass

from PySide6.QtCore import QModelIndex, QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import (
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
)


@dataclass(slots=True)
class CardItemStyleConfig:
    item_height: int = 48
    content_padding_x: int = 16
    border_radius: int = 4

    font_family: str | None = None
    font_size: int = 11
    font_weight: QFont.Weight = QFont.Weight.Normal

    text_color: str = "#F1F3F4"
    hover_background: str = "#292B2F"
    selected_background: str = "#34363A"


DEFAULT_CONFIG = CardItemStyleConfig()


class CardItemDelegate(QStyledItemDelegate):
    def __init__(
        self,
        parent=None,
        config: CardItemStyleConfig | None = None,
    ) -> None:
        super().__init__(parent)
        self._config = config or DEFAULT_CONFIG

    def set_config(self, config: CardItemStyleConfig) -> None:
        self._config = config

        parent = self.parent()
        if parent is not None:
            parent.viewport().update()

    def config(self) -> CardItemStyleConfig:
        return self._config

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> None:
        painter.save()

        config = self._config
        rect = option.rect

        if option.state & QStyle.StateFlag.State_Selected:
            painter.setBrush(QColor(config.selected_background))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(
                rect,
                config.border_radius,
                config.border_radius,
            )

        elif option.state & QStyle.StateFlag.State_MouseOver:
            painter.setBrush(QColor(config.hover_background))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(
                rect,
                config.border_radius,
                config.border_radius,
            )

        font = QFont()

        if config.font_family is not None:
            font.setFamily(config.font_family)

        font.setPointSize(config.font_size)
        font.setWeight(config.font_weight)

        painter.setFont(font)
        painter.setPen(QColor(config.text_color))

        text_rect = rect.adjusted(
            config.content_padding_x,
            0,
            -config.content_padding_x,
            0,
        )

        text = index.data(Qt.ItemDataRole.DisplayRole)

        painter.drawText(
            text_rect,
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter,
            text,
        )

        painter.restore()

    def sizeHint(
        self,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> QSize:
        return QSize(
            super().sizeHint(option, index).width(),
            self._config.item_height,
        )