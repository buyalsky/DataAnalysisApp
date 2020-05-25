import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from nodes.input_nodes import CsvLoader, XmlLoader, ExcelLoader, Deserializer
from nodes.both_input_and_output import LinearRegression, KmeansClustering, DecisionTree, Knn, SVM, Filter, \
    AttributeRemover, \
    NaiveBayesClassify
from nodes.output_nodes import SimplePlot, Serializer, Predictor, Histogram, ScatterPlot, TextOutput, PieChart, CsvSaver
from scene import Scene
from node import Node, NodeDemux
from graphics_view import GraphicsView

LISTBOX_MIMETYPE = "application/x-item"

NODE_LOADER = {
    "Csv Loader": CsvLoader,
    "Excel Loader": ExcelLoader,
    "Attribute Remover": AttributeRemover,
    "Linear Regression": LinearRegression,
    "Filter": Filter,
    "Text output": TextOutput,
    "Naive Bayes": NaiveBayesClassify,
    "Knn": Knn,
    "Decision Tree": DecisionTree,
    "SVM": SVM,
    "Scatter plot": ScatterPlot,
    "Pie Chart": PieChart,
    "Histogram": Histogram,
    "Xml Loader": XmlLoader,
    "Predictor": Predictor,
    "Serializer": Serializer,
    "Deserializer": Deserializer,
    "Simple Plot": SimplePlot,
    "K-Means": KmeansClustering,
    "Csv Saver": CsvSaver
}


class MainWidget(QWidget):
    def __init__(self, parent_window=None, parent=None):
        super().__init__(parent)
        if parent_window:
            self.parent_window = parent_window

        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # crate graphics scene
        self.scene = Scene(parent_widget=self)
        # self.graphic_scene = self.scene.graphic_scene
        self.nodes = []
        self.edges = []
        # self.add_nodes()

        # create graphics view
        self.view = GraphicsView(self.scene.graphic_scene, self)
        self.layout.addWidget(self.view)

        self.show()
        self.scene.addHasBeenModifiedListener(self.set_title)
        self.scene.addDragEnterListener(self.on_drag_enter)
        self.scene.addDropListener(self.on_drop)

        self._close_event_listeners = []

    def set_title(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def add_close_event_listener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def on_drag_enter(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)

    def on_drop(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event_data = event.mimeData().data(LISTBOX_MIMETYPE)
            data_stream = QDataStream(event_data, QIODevice.ReadOnly)
            pixmap = QPixmap()
            data_stream >> pixmap
            op_code = data_stream.readInt()
            text = data_stream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.graphic_scene.views()[0].mapToScene(mouse_position)

            print("GOT DROP: [%d] '%s'" % (op_code, text), "mouse:", mouse_position, "scene:", scene_position)

            if NODE_LOADER.get(text, False):
                node = NODE_LOADER[text](self.scene)
            elif "Demux" in text:
                node = NodeDemux(self.scene, inputs=1, outputs=int(text[2]))
            else:
                node = Node(self.scene, text, inputs=1, outputs=1)
            node.set_pos(scene_position.x(), scene_position.y())

            self.nodes.append(node)
            self.parent_window.change_statusbar_text()

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
