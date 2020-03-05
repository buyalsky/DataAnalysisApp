from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from socket_ import *
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class GraphicNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)


        self.width = 120
        self.height = 120
        self.edge_size = 10.0
        self.title_height = 22.5
        self._padding = 4.0

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        self.init_title()
        self.title = self.node.title
        self.init_sockets()
        self.init_content()

        self.initUI()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.graphic_node.isSelected():
                node.updateConnectedEdges()

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        print(self.node.title)

    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)


    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)


    def init_title(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(
            self.width
            - 2 * self._padding
        )

    def init_content(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.width - 2*self.edge_size, self.height - 2*self.edge_size-self.title_height)
        self.grContent.setWidget(self.content)


    def init_sockets(self):
        pass



    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())


        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())


class NodeContent(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        label = QLabel()
        # label.setStyleSheet("background-color: rgba(0,0,0,0%)")
        # label.setAttribute(Qt.WA_TranslucentBackground)
        pixmap = QPixmap("fish.png")
        label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio))
        self.layout.addWidget(label)


class Node:
    def __init__(self, scene, title="Undefined Node", inputs=None, outputs=None):
        self.scene = scene

        self.title = title
        if outputs is None:
            outputs = []
        if inputs is None:
            inputs = []
        self.content = NodeContent(self)
        self.graphic_node = GraphicNode(self)

        self.scene.add_node(self)
        self.scene.graphic_scene.addItem(self.graphic_node)

        self.socket_spacing = 22

        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=item)
            counter += 1
            self.outputs.append(socket)

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.graphic_node.pos()        # QPointF
    def setPos(self, x, y):
        self.graphic_node.setPos(x, y)

    def get_socket_position(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.graphic_node.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            #y = self.graphic_node.height - self.graphic_node.edge_size - self.graphic_node._padding - index * self.socket_spacing
            y = self.graphic_node.height // 2
        else :
            # start from top
            #y = self.graphic_node.title_height + self.graphic_node._padding + self.graphic_node.edge_size + index * self.socket_spacing
            y = self.graphic_node.height // 2

        return [x, y]


    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.has_edge():
                socket.edge.update_positions()


    def remove(self):
        logger.debug("> Removing Node {}".format(self))
        logger.debug(" - remove all edges from sockets")
        for socket in (self.inputs+self.outputs):
            if socket.has_edge():
                logger.debug("    - removing from socket: {} edge: {}".format(socket, socket.edge))
                socket.edge.remove()
        logger.debug(" - remove graphic_node")
        self.scene.graphic_scene.removeItem(self.graphic_node)
        self.graphic_node = None
        logger.debug(" - remove node.py from the scene")
        self.scene.remove_node(self)
        try:
            self.scene.parent_widget.nodes.remove(self)
        except ValueError:
            pass
        logger.debug(" - everything was done.")
