from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

LISTBOX_MIMETYPE = "application/x-item"


class DragList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

    def add_items(self, items, icon=None):
        for item in items:
            item = QListWidgetItem(item, self)
            pixmap = QPixmap(icon if icon is not None else ".")
            item.setIcon(QIcon(pixmap))
            item.setSizeHint(QSize(32, 32))

            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

            # setup data
            item.setData(Qt.UserRole, pixmap)
            item.setData(Qt.UserRole + 1, 1)

    def startDrag(self, *args, **kwargs):
        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)
            # print("dragging item <%d>" % op_code, item)

            pixmap = QPixmap(item.data(Qt.UserRole))

            item_data = QByteArray()
            data_stream = QDataStream(item_data, QIODevice.WriteOnly)
            data_stream << pixmap
            data_stream.writeInt(op_code)
            data_stream.writeQString(item.text())

            mime_data = QMimeData()
            mime_data.setData(LISTBOX_MIMETYPE, item_data)

            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            Exception(e)
