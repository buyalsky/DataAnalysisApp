import logging
import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from socket_ import LEFT_TOP, LEFT_BOTTOM, RIGHT_BOTTOM, RIGHT_TOP

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

EDGE_ROUNDNESS = 100


class Edge:
    def __init__(self, scene, start_socket, end_socket):

        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.graphic_edge = GraphicEdgeCurved(self)

        self.update_positions()
        self.scene.graphic_scene.addItem(self.graphic_edge)
        self.scene.add_edge(self)

    def __str__(self):
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def update_positions(self):
        source_pos = self.start_socket.get_socket_position()
        source_pos[0] += self.start_socket.node.graphic_node.pos().x()
        source_pos[1] += self.start_socket.node.graphic_node.pos().y()
        self.graphic_edge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.get_socket_position()
            end_pos[0] += self.end_socket.node.graphic_node.pos().x()
            end_pos[1] += self.end_socket.node.graphic_node.pos().y()
            self.graphic_edge.setDestination(*end_pos)
        else:
            self.graphic_edge.setDestination(*source_pos)
        self.graphic_edge.update()

    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.set_edge(None)
        if self.end_socket is not None:
            self.end_socket.set_edge(None)
        self.end_socket = None
        self.start_socket = None

    def remove(self):
        logger.debug(" Removing Edge {}".format(self))
        logger.debug(" - remove edge from all sockets")
        self.remove_from_sockets()
        self.scene.graphic_scene.removeItem(self.graphic_edge)
        self.graphic_edge = None
        try:
            self.scene.remove_edge(self)
        except ValueError:
            pass
        try:
            self.scene.parent_widget.edges.remove(self)
        except ValueError:
            pass


class GraphicEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)
        self._pen_dragging.setWidthF(2.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.setPath(self.calc_path())

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def intersects_with(self, p1, p2):
        cutpath = QPainterPath(p1)
        cutpath.lineTo(p2)
        path = self.calc_path()
        return cutpath.intersects(path)

    def calc_path(self):
        raise NotImplementedError


class GraphicEdgeCurved(GraphicEdge):
    def calc_path(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        sspos = self.edge.start_socket.position

        if (s[0] > d[0] and sspos in (RIGHT_TOP, RIGHT_BOTTOM)) or (s[0] < d[0] and sspos in (LEFT_BOTTOM, LEFT_TOP)):
            cpx_d *= -1
            cpx_s *= -1

            cpy_d = (
                (s[1] - d[1]) / math.fabs(
                    (s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.00001
                )
            ) * EDGE_ROUNDNESS
            cpy_s = (
                (d[1] - s[1]) / math.fabs(
                    (d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.00001
                )
            ) * EDGE_ROUNDNESS

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.posDestination[0], self.posDestination[1])

        return path
