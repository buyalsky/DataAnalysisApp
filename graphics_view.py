from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import logging

from socket_ import GraphicSocket
from edge import GraphicEdge
from edge import Edge

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10


class GraphicsView(QGraphicsView):
    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)
        self.graphic_scene = graphic_scene
        self.parent_widget = parent

        self.initUI()

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
        self.cutline = CutLine()
        self.graphic_scene.addItem(self.cutline)

        # listeners
        self._drag_enter_listeners = []
        self._drop_listeners = []

    def initUI(self):
        self.setRenderHints(
            QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def dragEnterEvent(self, event):
        for callback in self._drag_enter_listeners:
            callback(event)

    def dropEvent(self, event):
        for callback in self._drop_listeners:
            callback(event)

    def addDragEnterListener(self, callback):
        self._drag_enter_listeners.append(callback)

    def addDropListener(self, callback):
        self._drop_listeners.append(callback)

    def mousePressEvent(self, event):
        print("Mouse pressed")
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        # get item which we clicked on
        item = self.getItemAtClick(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        logger.debug("LMB Click on {} {}".format(item, self.debug_modifiers(event)))

        # logic
        if hasattr(item, "node.py") or isinstance(item, GraphicEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return

        if type(item) is GraphicSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res:
                return

        if item is None:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        # logic
        if hasattr(item, "node.py") or isinstance(item, GraphicEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return

        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)

        if isinstance(item, GraphicEdge):
            logger.debug('RMB DEBUG:', item.edge, ' connecting sockets:', item.edge.start_socket, '<-->'
                         , item.edge.end_socket)
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

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.graphic_edge.setDestination(pos.x(), pos.y())
            self.dragEdge.graphic_edge.update()

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

    def cutIntersectingEdges(self):
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
                if isinstance(item, GraphicEdge):
                    item.edge.remove()
                # TODO: Take a look at this one later
                elif hasattr(item, 'node'):
                    item.node.remove()
                    self.parent_widget.parent_window.change_statusbar_text()

    def debug_modifiers(self, event):
        out = "MODS: "
        if event.modifiers() & Qt.ShiftModifier:
            out += "SHIFT "
        if event.modifiers() & Qt.ControlModifier:
            out += "CTRL "
        if event.modifiers() & Qt.AltModifier:
            out += "ALT "
        return out

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        logger.debug('View::edgeDragStart ~ Start dragging edge')
        logger.debug('View::edgeDragStart ~   assign Start Socket to:'.format(item.socket))
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket

        self.dragEdge = Edge(self.graphic_scene.scene, item.socket, None)
        logger.debug('View::edgeDragStart ~   dragEdge:'.format(self.dragEdge))

    # called when we append an edge
    def edgeDragEnd(self, item):
        self.mode = MODE_NOOP

        if isinstance(item, GraphicSocket):
            if item.socket != self.last_start_socket:
                logger.debug('View::edgeDragEnd ~   previous edge: {}'.format(self.previousEdge))
                if item.socket.has_edge():
                    item.socket.edge.remove()
                logger.debug('View::edgeDragEnd ~   assign End Socket {}'.format(item.socket))
                if self.previousEdge is not None:
                    self.previousEdge.remove()
                logger.debug('View::edgeDragEnd ~  previous edge removed')

                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.set_edge(self.dragEdge)
                self.dragEdge.end_socket.set_edge(self.dragEdge)

                logger.debug('View::edgeDragEnd ~  reassigned start & end sockets to drag edge')

                logger.debug(type(self.dragEdge))
                self.parent_widget.edges.append(self.dragEdge)
                self.dragEdge.update_positions()
                return True

        logger.debug('View::edgeDragEnd ~ End dragging edge')

        self.dragEdge.remove()
        self.dragEdge = None
        logger.debug('View::edgeDragEnd ~ about to set socket to previous edge: {}'.format(self.previousEdge))
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge
        logger.debug('View::edgeDragEnd ~ everything done.')

        return False

    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y()) > edge_drag_threshold_sq

    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

class CutLine(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.line_points = []

        self._pen = QPen(Qt.red)
        self._pen.setWidthF(2.0)
        self._pen.setDashPattern([3, 3])

        self.setZValue(2)

    def boundingRect(self):
        return QRectF(0, 0, 1, 1)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self.line_points)
        painter.drawPolyline(poly)
