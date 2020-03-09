from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from nodes.input_nodes import *
from nodes.both_input_and_output import *
from nodes.output_nodes import *
from scene import Scene
from node import Node
from edge import Edge, EDGE_TYPE_BEZIER
from graphics_view import QDMGraphicsView
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

        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()
        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)

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
        #self.add_nodes()

        # create graphics view
        self.view = QDMGraphicsView(self.scene.graphic_scene, self)
        self.layout.addWidget(self.view)


        self.setWindowTitle("Node Editor")
        self.show()

    def add_nodes(self):
        for i in range(3):
            self.nodes.append(Node(self.scene, "My Awesome Node " + str(i+1), inputs=[0], outputs=[1]))

        self.nodes[0].setPos(-350, -250)
        self.nodes[1].setPos(-75, 0)
        self.nodes[2].setPos(200, -150)

        self.edges.append(Edge(self.scene, self.nodes[0].outputs[0], self.nodes[1].inputs[0], edge_type=EDGE_TYPE_BEZIER))
        self.edges.append(Edge(self.scene, self.nodes[1].outputs[0], self.nodes[2].inputs[0], edge_type=EDGE_TYPE_BEZIER))

    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.graphic_scene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.graphic_scene.addText("This is my Awesome text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello World")
        proxy1 = self.graphic_scene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.graphic_scene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.graphic_scene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)

    def loadStylesheet(self, filename):
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

    def onDragEnter(self, event):
        # print("CalcSubWnd :: ~onDragEnter")
        # print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            # print(" ... denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event):
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

            # @TODO Fix me!
            #node = Node(self.scene, text, inputs=1, outputs=1)
            if text == "Csv Loader":
                node = CsvLoader(self.scene)
            elif text == "Excel Loader":
                node = ExcelLoader(self.scene)
            elif text == "Text output":
                node = TextOutput(self.scene)
            elif text == "Scatter plot":
                node = ScatterPlot(self.scene)
            elif text == "Histogram":
                node = Histogram(self.scene)
            else:
                node = Node(self.scene, text, inputs=1, outputs=1)
            node.setPos(scene_position.x(), scene_position.y())
            self.scene.add_node(node)
            self.nodes.append(node)
            self.parent_window.change_statusbar_text()

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            # print(" ... drop ignored, not requested format '%s'" % LISTBOX_MIMETYPE)
            event.ignore()

