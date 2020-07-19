import logging

from edge import Edge
from edge import GraphicalPath
from socket_ import GraphicSocket

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

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10


class ScrollableField(QGraphicsView):
    previous_edge = None
    last_start_socket = None
    drag_edge = None
    last_lmb_click_scene_pos = None

    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)
        self.graphic_scene = graphic_scene
        self.parent_widget = parent

        self.setRenderHints(
            QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.
            SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.setScene(self.graphic_scene)

        self.mode = MODE_NOOP
        self.editingFlag = False

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]
        self.setStyleSheet("selection-background-color: rgb(255, 255, 255);")

        # cutline
        self.cutline = LineCutter()
        self.graphic_scene.addItem(self.cutline)

        # listeners
        self._drag_enter_listeners = []
        self._drop_listeners = []

    def dragEnterEvent(self, event):
        for callback in self._drag_enter_listeners:
            callback(event)

    def dropEvent(self, event):
        for callback in self._drop_listeners:
            callback(event)

    def add_drag_enter_listener(self, callback):
        self._drag_enter_listeners.append(callback)

    def add_drop_listener(self, callback):
        self._drop_listeners.append(callback)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middle_mouse_button_press(event)
        elif event.button() == Qt.LeftButton:
            self.left_mouse_button_press(event)
        elif event.button() == Qt.RightButton:
            self.right_mouse_button_press(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middle_mouse_button_release(event)
        elif event.button() == Qt.LeftButton:
            self.left_mouse_button_release(event)
        elif event.button() == Qt.RightButton:
            self.right_mouse_button_release(event)
        else:
            super().mouseReleaseEvent(event)

    def middle_mouse_button_press(self, event):
        release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                    Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(release_event)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                 Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fake_event)

    def middle_mouse_button_release(self, event):
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                 Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fake_event)
        self.setDragMode(QGraphicsView.NoDrag)

    def left_mouse_button_press(self, event):
        # get item which we clicked on
        item = self.get_item_at_click(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        logger.debug("Left Click on {}".format(item))

        # logic
        if hasattr(item, "node.py") or isinstance(item, GraphicalPath) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fake_event = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                         Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                         event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fake_event)
                return

        if type(item) is GraphicSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edge_drag_start(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edge_drag_end(item)
            if res:
                return

        if item is None:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fake_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                         Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fake_event)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return

        super().mousePressEvent(event)

    def left_mouse_button_release(self, event):
        # get item which we release mouse button on
        item = self.get_item_at_click(event)

        # logic
        if hasattr(item, "node.py") or isinstance(item, GraphicalPath) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                         Qt.LeftButton, Qt.NoButton,
                                         event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fake_event)
                return

        if self.mode == MODE_EDGE_DRAG:
            if self.distance_between_click_and_release_is_off(event):
                if self.edge_drag_end(item):
                    return

        if self.mode == MODE_EDGE_CUT:
            self.cut_intersecting_edges()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return

        super().mouseReleaseEvent(event)

    def right_mouse_button_press(self, event):
        super().mousePressEvent(event)

        item = self.get_item_at_click(event)

        if isinstance(item, GraphicalPath):
            logger.debug('RMB DEBUG:', item.edge, ' connecting sockets:', item.edge.start_socket, item.edge.end_socket)
        if type(item) is GraphicSocket:
            logger.debug('RMB DEBUG:', item.socket, 'has edge:', item.socket.edge)

        if item is None:
            logger.debug('SCENE:')
            logger.debug('  Nodes:')
            for node in self.graphic_scene.scene.nodes:
                logger.debug('    {}'.format(node))
            logger.debug('  Edges:')
            for edge in self.graphic_scene.scene.edges:
                logger.debug('    {}'.format(edge))

    def right_mouse_button_release(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.drag_edge.graphic_edge.set_destination(pos.x(), pos.y())
            self.drag_edge.graphic_edge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            if not self.editingFlag:
                self.delete_selected()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def cut_intersecting_edges(self):
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]

            for edge in self.graphic_scene.scene.edges:
                if edge.graphic_edge.intersects_with(p1, p2):
                    edge.remove()

    def delete_selected(self):
        response = QMessageBox.question(self, '', "Are you sure to remove selected item(s)?",
                                        QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            for item in self.graphic_scene.selectedItems():
                if isinstance(item, GraphicalPath):
                    item.edge.remove()
                elif hasattr(item, 'node'):
                    item.node.remove()
                    self.parent_widget.parent_window.change_statusbar_text()

    def get_item_at_click(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edge_drag_start(self, item):
        self.previous_edge = item.socket.edge
        self.last_start_socket = item.socket

        self.drag_edge = Edge(self.graphic_scene.scene, item.socket, None)

    # called when we append an edge
    def edge_drag_end(self, item):
        self.mode = MODE_NOOP

        if isinstance(item, GraphicSocket):
            if item.socket != self.last_start_socket:
                logger.debug('Previous edge: {}'.format(self.previous_edge))
                if item.socket.has_edge():
                    item.socket.edge.remove()
                logger.debug('End Socket {}'.format(item.socket))
                if self.previous_edge is not None:
                    self.previous_edge.remove()

                self.drag_edge.start_socket = self.last_start_socket
                self.drag_edge.end_socket = item.socket
                self.drag_edge.start_socket.set_edge(self.drag_edge)
                self.drag_edge.end_socket.set_edge(self.drag_edge)

                logger.debug(type(self.drag_edge))
                self.parent_widget.edges.append(self.drag_edge)
                self.drag_edge.update_positions()
                return True

        logger.debug('View::edgeDragEnd ~ End dragging edge')

        self.drag_edge.remove()
        self.drag_edge = None
        logger.debug('View::edgeDragEnd ~ about to set socket to previous edge: {}'.format(self.previous_edge))
        if self.previous_edge is not None:
            self.previous_edge.start_socket.edge = self.previous_edge
        logger.debug('View::edgeDragEnd ~ everything done.')

        return False

    def distance_between_click_and_release_is_off(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y()) > edge_drag_threshold_sq

    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoom_out_factor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoom_factor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoom_factor, zoom_factor)


class LineCutter(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.line_points = []

        self._pen = QPen(Qt.red)
        self._pen.setWidthF(2.0)
        self._pen.setDashPattern([3, 3])

        self.setZValue(2)

    def boundingRect(self):
        return QRectF(0, 0, 1, 1)

    def paint(self, painter, graphics_item, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self.line_points)
        painter.drawPolyline(poly)
