from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from nodes.input_nodes import *
from nodes.both_input_and_output import *
from nodes.output_nodes import *
from scene import Scene
from node import Node, NodeDemux
from edge import Edge, EDGE_TYPE_BEZIER
from graphics_view import GraphicsView

LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_INPUT = 1
OP_NODE_OUTPUT = 2
OP_NODE_ADD = 3
OP_NODE_SUB = 4
OP_NODE_MUL = 5
OP_NODE_DIV = 6


class MainWidget(QWidget):
    def __init__(self, parent_window=None, parent=None):
        super().__init__(parent)
        if parent_window:
            self.parent_window = parent_window

        self.load_stylesheet('qss/nodestyle.qss')

        self.initUI()
        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.addDragEnterListener(self.on_drag_enter)
        self.scene.addDropListener(self.on_drop)

        self._close_event_listeners = []

    def initUI(self):
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

        self.setWindowTitle("Node Editor")
        self.show()

    def load_stylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def on_drag_enter(self, event):
        # print("CalcSubWnd :: ~onDragEnter")
        # print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            # print(" ... denied drag enter event")
            event.setAccepted(False)

    def on_drop(self, event):
        # print("CalcSubWnd :: ~onDrop")
        # print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.graphic_scene.views()[0].mapToScene(mouse_position)

            print("GOT DROP: [%d] '%s'" % (op_code, text), "mouse:", mouse_position, "scene:", scene_position)

            # node = Node(self.scene, text, inputs=1, outputs=1)
            # TODO: these if statements are verbose, use dictionary instead
            if text == "Csv Loader":
                node = CsvLoader(self.scene)
            elif text == "Excel Loader":
                node = ExcelLoader(self.scene)
            elif text == "Attribute Remover":
                node = AttributeRemover(self.scene)
            elif text == "Text output":
                node = TextOutput(self.scene)
            elif text == "Naive Bayes":
                node = NaiveBayesClassify(self.scene)
            elif text == "Knn":
                node = Knn(self.scene)
            elif text == "Decision Tree":
                node = DecisionTree(self.scene)
            elif text == "SVM":
                node = SVM(self.scene)
            elif text == "Scatter plot":
                node = ScatterPlot(self.scene)
            elif text == "Histogram":
                node = Histogram(self.scene)
            elif text == "Xml Loader":
                node = XmlLoader(self.scene)
            elif text == "Predictor":
                node = Predictor(self.scene)
            elif text == "Serializer":
                node = Serializer(self.scene)
            elif text == "Deserializer":
                node = Deserializer(self.scene)
            elif "Demux" in text:
                node = NodeDemux(self.scene, inputs=1, outputs=int(text[2]))
            else:
                node = Node(self.scene, text, inputs=1, outputs=1)
            node.set_pos(scene_position.x(), scene_position.y())
            # self.scene.add_node(node)
            self.nodes.append(node)
            self.parent_window.change_statusbar_text()

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
