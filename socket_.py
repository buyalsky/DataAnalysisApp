from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class GraphicSocket(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.radius = 6.0
        self.outline_width = 1.0
        self._color_background = QColor("#ff0000")
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # painting circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self):
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4
DEBUG = False

class Socket:
    def __init__(self, node, index=0, position=LEFT_TOP):

        self.node = node
        self.index = index
        self.position = position

        if DEBUG:
            print("Socket -- creating with", self.index, self.position, "for node", self.node)

        self.graphic_socket = GraphicSocket(self.node.graphic_node)

        self.graphic_socket.setPos(*self.node.get_socket_position(index, position))

        self.graphic_socket.setPos(*self.node.get_socket_position(index, position))

        self.edge = None

    def getSocketPosition(self):
        if DEBUG:
            print("  GSP: ", self.index, self.position, "node:", self.node)
        res = self.node.get_socket_position(self.index, self.position)
        if DEBUG:
            print("  res", res)
        return res

    def setConnectedEdge(self, edge=None):
        self.edge = edge




