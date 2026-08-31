from PySide6.QtCore import QModelIndex, QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import (
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
)


class CardItemDelegate(QStyledItemDelegate):

    class Style:
        item_height: int = 48
        content_padding_x: int = 16
        border_radius: int = 4

        font_family: str | None = None
        font_size: int = 11
        font_weight: QFont.Weight = QFont.Weight.Normal

        text_color: str = "#F1F3F4"
        hover_background: str = "#292B2F"
        selected_background: str = "#34363A"

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> None:
        painter.save()

        rect = option.rect

        if option.state & QStyle.StateFlag.State_Selected:
            painter.setBrush(QColor(CardItemDelegate.Style.selected_background))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(
                rect,
                CardItemDelegate.Style.border_radius,
                CardItemDelegate.Style.border_radius,
            )

        elif option.state & QStyle.StateFlag.State_MouseOver:
            painter.setBrush(QColor(CardItemDelegate.Style.hover_background))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(
                rect,
                CardItemDelegate.Style.border_radius,
                CardItemDelegate.Style.border_radius,
            )

        font = QFont()

        if CardItemDelegate.Style.font_family is not None:
            font.setFamily(CardItemDelegate.Style.font_family)

        font.setPointSize(CardItemDelegate.Style.font_size)
        font.setWeight(CardItemDelegate.Style.font_weight)

        painter.setFont(font)
        painter.setPen(QColor(CardItemDelegate.Style.text_color))

        text_rect = rect.adjusted(
            CardItemDelegate.Style.content_padding_x,
            0,
            -CardItemDelegate.Style.content_padding_x,
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
            CardItemDelegate.Style.item_height,
        )