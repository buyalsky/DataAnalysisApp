from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

LISTBOX_MIMETYPE = "application/x-item"
NODES_TO_ICONS = {
    "Csv Loader": "icons/csv24.png",
    "Excel Loader": "icons/excel24.png",
    "Xml Loader": "icons/xml24.png",
    "Attribute Remover": "icons/preprocessing242.png",
    "Filter": "icons/filter24.png",
    "Linear Regression": "icons/linear-reg24.png",
    "Decision Tree": "icons/decision-tree24.png",
    "Knn": "icons/classification24.png",
    "Naive Bayes": "icons/classification24.png",
    "SVM": "icons/classification24.png",
    "K-Means": "icons/clustering24.png",
    "Hierarchical": "icons/clustering24.png",
    "Csv Saver": "icons/saver24.png",
    "Serializer": "icons/serializer24.png",
    "Deserializer": "icons/serializer24.png",
    "Predictor": "icons/loupe24.png",
    "Pie Chart": "icons/pie-chart24.png",
    "Scatter plot": "icons/scatter24.png",
    "Simple Plot": "icons/plot24.png",
    "Text output": "icons/text24.png",
    "Histogram": "icons/histogram24.png"
}


class DragList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

    def add_items(self, items, icon):
        for item_name in items:
            item = QListWidgetItem(item_name, self)
            pixmap = QPixmap(NODES_TO_ICONS.get(item_name, icon))
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
