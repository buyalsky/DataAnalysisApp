from socket_ import *
import logging
import time
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class GraphicNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self._title = self.node.title
        self.content = self.node.content

        title_font = QFont("Consolas", 10)

        self.width = 120
        self.height = 120
        self.edge_size = 5.0
        self.title_height = 40 if len(self.node.title) > 12 else 22.5
        self.padding = 4.0

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))
        self._pen_selected.setWidth(2)

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(Qt.white)
        self.title_item.setFont(title_font)
        self.title_item.setPos(self.padding, 0)
        self.title_item.setTextWidth(self.width - 2 * self.padding)
        self.title_item.setPlainText(self._title)
        self.init_content()

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        for node in self.scene().scene.nodes:
            if node.graphic_node.isSelected():
                node.update_connected_edges()

    def mouseDoubleClickEvent(self, event):
        self.node.run()

    @property
    def title(self):
        return self._title

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def init_content(self):
        self.gr_content = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.width - 2 * self.edge_size, self.height - 2 * self.edge_size - self.title_height)
        self.gr_content.setWidget(self.content)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size,
                           self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size,
                                    self.edge_size)
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


class GraphicsNodeDemux(QGraphicsItem):
    def __init__(self, node, parent=None, socket_count=0):
        super().__init__(parent)
        self.node = node

        self._pen_default = QPen(QColor("6e6a6a"))
        self._pen_selected = QPen(QColor("#FFFFA637"))
        self._pen_selected.setWidth(2)
        self._brush_title = QBrush(QColor("#FF313131"))

        self.width = 50
        self.height = socket_count * 30
        self.edge_size = 10.0
        self.padding = 4.0

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        for node in self.scene().scene.nodes:
            if node.graphic_node.isSelected():
                node.update_connected_edges()

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        polygon = QPolygonF()
        # sol ust
        polygon.append(QPoint(0, self.height // 2 - 10))
        # sol alt
        polygon.append(QPoint(0, self.height // 2 + 10))
        polygon.append(QPoint(50, self.height))
        polygon.append(QPoint(50, 0))
        """
        linepen = QPen()
        linepen.setWidth(5)
        linepen.setColor(Qt.red)
        painter.setPen(linepen)
        """

        painter_path = QPainterPath()
        painter_path.addPolygon(polygon)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(self._brush_title)

        painter.drawPolygon(polygon)
        painter.drawPath(painter_path.simplified())


class NodeContentWidget(QWidget):
    def __init__(self, node, parent=None, icon_name=None):
        self.node = node
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setStyleSheet("background: transparent;")
        label = QLabel()
        # label.setStyleSheet("background-color: rgba(0,0,0,0%)")
        # label.setAttribute(Qt.WA_TranslucentBackground)

        pixmap = QPixmap(icon_name if icon_name else ".")
        label.setPixmap(pixmap.scaled(60, 160, Qt.KeepAspectRatio))
        self.layout.addWidget(label, alignment=Qt.AlignCenter)


class Node:
    def __init__(self, scene, title="Undefined Node", inputs=0, outputs=0, icon_name=None):
        self.scene = scene
        self.is_finished = False

        self.title = title

        self.content = NodeContentWidget(self, icon_name=icon_name)
        self.graphic_node = GraphicNode(self)

        self.scene.add_node(self)
        self.scene.graphic_scene.addItem(self.graphic_node)
        self.node_type = ""

        self.is_first = False
        self.is_last = False

        self.input_socket = None
        self.output_socket = None

        if inputs:
            self.input_socket = Socket(node=self, index=0, position=LEFT_BOTTOM)
        if outputs:
            self.output_socket = Socket(node=self, index=0, position=RIGHT_TOP)

    def __hash__(self):
        return id(self)

    def __str__(self):
        return "Node {}".format(self.title)

    def run(self):
        print("node")

    @property
    def pos(self):
        return self.graphic_node.pos()

    def set_pos(self, x, y):
        self.graphic_node.setPos(x, y)

    def get_socket_position(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.graphic_node.width
        y = self.graphic_node.height // 2

        return [x, y]

    def update_connected_edges(self):
        if self.input_socket and self.input_socket.has_edge():
            self.input_socket.edge.update_positions()
        if self.output_socket and self.output_socket.has_edge():
            self.output_socket.edge.update_positions()

    def remove(self):
        if self.input_socket and self.input_socket.has_edge():
            logger.debug("    - removing from socket: {} edge: {}".format(self.input_socket, self.input_socket.edge))
            self.input_socket.edge.remove()
        if self.output_socket and self.output_socket.has_edge():
            logger.debug("    - removing from socket: {} edge: {}".format(self.output_socket, self.output_socket.edge))
            self.output_socket.edge.remove()
        self.scene.graphic_scene.removeItem(self.graphic_node)
        self.graphic_node = None
        logger.debug(" - remove node.py from the scene")
        self.scene.remove_node(self)
        try:
            self.scene.parent_widget.nodes.remove(self)
        except ValueError:
            pass


class InputNode(Node):
    dialog = None
    line_edit = None
    df = None

    def __init__(self, scene, title=None, inputs=0, outputs=1, icon_name="icons/input128.png"):
        Node.__init__(self, scene, title=title, inputs=inputs, outputs=outputs, icon_name=icon_name)
        self.is_first = True

    def run(self):
        self.dialog = QDialog()
        self.dialog.setModal(True)
        self.setup_ui()
        self.dialog.show()

    def setup_ui(self):
        raise NotImplementedError

    def return_file(self):
        self.dialog.accept()
        if isinstance(self.df, pd.core.frame.DataFrame):
            self.is_finished = True
            self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
            # order the nodes
            self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
            # feed the next node
            if self.graphic_node.scene().scene.parent_widget.parent_window.is_ordered:
                self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)
        else:
            self.is_finished = False

    @property
    def output(self):
        return {"data_frame": self.df, "input_file_path": self.line_edit.text()}


class InputOutputNode(Node):
    dialog = None
    fed_data = None
    modified_data = None
    required_keys = ["data_frame"]

    def __init__(self, scene, title=None, icon_name="icons/both128.png"):
        Node.__init__(self, scene, title=title, inputs=1, outputs=1, icon_name=icon_name)

    def run(self):
        if not isinstance(self.fed_data, dict):
            QMessageBox.warning(
                self.scene.parent_widget,
                "Warning!",
                "You need to complete preceding nodes first!"
            )
            return
        else:
            k = self.fed_data.keys()
            for requirement in self.required_keys:
                if requirement not in k:
                    QMessageBox.warning(
                        self.scene.parent_widget,
                        "Warning!",
                        "This node does not match with its previous node!"
                    )
                    return
        self.dialog = QDialog()
        self.dialog.setModal(True)
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setup_ui()
        self.dialog.show()

    def setup_ui(self):
        raise NotImplementedError

    def return_file(self):
        self.dialog.accept()
        self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
        # order the nodes
        self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
        # feed the next node
        self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)

    def feed(self, data):
        self.fed_data = data
        self.modified_data = data

    @property
    def output(self):
        return self.modified_data


class OutputNode(Node):
    dialog = None
    fed_data = None
    required_keys = ["data_frame"]

    def __init__(self, scene, title=None, icon_name="icons/output128.png"):
        Node.__init__(self, scene, title=title, inputs=1, outputs=0, icon_name=icon_name)
        self.is_last = True

    def run(self):
        if not isinstance(self.fed_data, dict):
            QMessageBox.warning(
                self.scene.parent_widget,
                "Warning!",
                "You need to complete preceding nodes first!"
            )
            return
        else:
            k = self.fed_data.keys()
            for requirement in self.required_keys:
                if requirement not in k:
                    QMessageBox.warning(
                        self.scene.parent_widget,
                        "Warning!",
                        "This node does not match with its previous node!"
                    )
                    return
        self.dialog = QDialog()
        self.dialog.setModal(True)
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setup_ui()
        self.dialog.show()

    def setup_ui(self):
        raise NotImplementedError

    def feed(self, data):
        self.fed_data = data


class NodeDemux:
    def __init__(self, scene, inputs=0, outputs=0):
        self.scene = scene

        self.graphic_node = GraphicsNodeDemux(self, socket_count=outputs)

        self.scene.add_node(self)
        self.scene.graphic_scene.addItem(self.graphic_node)

        self.socket_spacing = 30

        self.node_type = ""
        self.title = "1x{}Demux".format(outputs)

        self.input_socket = None
        self.output_sockets = []

        if inputs:
            self.input_socket = Socket(node=self, index=0, position=LEFT_TOP)

        for i in range(outputs):
            self.output_sockets.append(Socket(node=self, index=i, position=RIGHT_BOTTOM))

    def __str__(self):
        return "DemuxNode which contains {} outputs".format(len(self.output_sockets))

    @property
    def pos(self):
        return self.graphic_node.pos()  # QPointF

    def set_pos(self, x, y):
        self.graphic_node.setPos(x, y)

    def get_socket_position(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.graphic_node.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.graphic_node.height - self.graphic_node.edge_size - self.graphic_node.padding - index * \
                self.socket_spacing
        else:
            y = self.graphic_node.height // 2

        return [x, y]

    def update_connected_edges(self):
        if self.input_socket and self.input_socket.has_edge():
            self.input_socket.edge.update_positions()
        for output_socket in self.output_sockets:
            if output_socket and output_socket.has_edge():
                output_socket.edge.update_positions()

    def remove(self):
        logger.debug("> Removing Demux Node {}".format(self))
        logger.debug(" - remove all edges from sockets")
        if self.input_socket and self.input_socket.has_edge():
            logger.debug("    - removing from socket: {} edge: {}".format(self.input_socket, self.input_socket.edge))
            self.input_socket.edge.remove()
        for output_socket in self.output_sockets:
            if output_socket and output_socket.has_edge():
                logger.debug("    - removing from socket: {} edge: {}".format(output_socket, output_socket.edge))
                output_socket.edge.remove()
        logger.debug(" - remove graphic_node")
        self.scene.graphic_scene.removeItem(self.graphic_node)
        self.graphic_node = None
        logger.debug(" - remove node.py from the scene")
        self.scene.remove_node(self)
        try:
            self.scene.parent_widget.nodes.remove(self)
        except ValueError:
            pass
