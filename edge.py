from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraphicEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.update_path()

        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def update_path(self):
        """ Will handle drawing QPainterPath from Point A to B """
        raise NotImplemented("This method has to be overriden in a child class")

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]


class GraphicEdgeDirect(GraphicEdge):
    def update_path(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)


class GraphicEdgeBezier(GraphicEdge):
    def update_path(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        if s[0] > d[0]: dist *= -1

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo( s[0] + dist, s[1], d[0] - dist, d[1], self.posDestination[0], self.posDestination[1])
        self.setPath(path)


EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2
DEBUG = False


class Edge:
    def __init__(self, scene, start_socket, end_socket, edge_type=EDGE_TYPE_DIRECT):

        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.graphic_edge = GraphicEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else GraphicEdgeBezier(self)

        self.updatePositions()
        if DEBUG: print("Edge: ", self.graphic_edge.posSource, "to", self.graphic_edge.posDestination)

        self.scene.graphic_scene.addItem(self.graphic_edge)

    def updatePositions(self):
        print("update postions")
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.graphic_node.pos().x()
        source_pos[1] += self.start_socket.node.graphic_node.pos().y()
        self.graphic_edge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.graphic_node.pos().x()
            end_pos[1] += self.end_socket.node.graphic_node.pos().y()
            self.graphic_edge.setDestination(*end_pos)
        if DEBUG: print(" SS:", self.start_socket)
        if DEBUG: print(" ES:", self.end_socket)
        self.graphic_edge.update()

    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.end_socket = None
        self.start_socket = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.graphic_edge)
        self.graphic_edge = None
        self.scene.removeEdge(self)

