import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import math


class GraphicScene(qtw.QGraphicsScene):

    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.scene = scene

        self.gridSize = 20
        self.gridSquares = 5

        self._color_background = qtg.QColor("#ffffff")
        self._color_light = qtg.QColor("#d9d8d7")
        self._color_dark = qtg.QColor("#bcbbba")

        self._pen_light = qtg.QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = qtg.QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)

    def set_graphic_scene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if (x % (self.gridSize * self.gridSquares) != 0):
                lines_light.append(qtc.QLine(x, top, x, bottom))

            else:
                lines_dark.append(qtc.QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if (y % (self.gridSize * self.gridSquares) != 0):
                lines_light.append(qtc.QLine(left, y, right, y))
            else:
                lines_dark.append(qtc.QLine(left, y, right, y))

        # draw the lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)


class Scene:
    def __init__(self, width=64000, height=64000):
        self.nodes = []
        self.edges = []

        self.scene_width = width
        self.scene_height = height

        self.initUI()

    def initUI(self):
        self.graphic_scene = GraphicScene(self)
        self.graphic_scene.set_graphic_scene(self.scene_width, self.scene_height)

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_node(self, node):
        self.nodes.remove(node)

    def remove_edge(self, edge):
        self.edges.remove(edge)