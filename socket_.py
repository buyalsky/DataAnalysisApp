import logging

try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Socket:
    def __init__(self, node, index=0, position=LEFT_TOP):

        self.node = node
        self.index = index
        self.position = position

        self.graphic_socket = GraphicSocket(self)

        self.graphic_socket.setPos(*self.node.get_socket_position(index, position))

        self.edge = None

    def __str__(self):
        return "<Socket %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def get_socket_position(self):
        res = self.node.get_socket_position(self.index, self.position)
        return res

    def set_edge(self, edge=None):
        self.edge = edge
        self.graphic_socket.change_socket_color(bool(edge))

    def has_edge(self):
        return self.edge is not None


class GraphicSocket(QGraphicsItem):
    def __init__(self, socket):
        self.socket = socket
        super().__init__(socket.node.graphic_node)

        self.radius = 6.0
        self.outline_width = 1.0

        self._pen = QPen(QColor("#FF000000"))
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(QColor("#ff0000"))

    def paint(self, painter, graphics_item, widget=None):
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

    def change_socket_color(self, is_connected):
        if is_connected:
            self._brush.setColor(QColor("#00ff00"))
        else:
            self._brush.setColor(QColor("#ff0000"))

