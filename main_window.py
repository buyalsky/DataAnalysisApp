import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from main_widget import MainWidget
from drag_list import DragList
from node import Node, NodeDemux


class MainWindow(QMainWindow):
    ordered_nodes = None

    def __init__(self):
        super().__init__()
        self.main_widget = MainWidget(parent_window=self)
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage('Ready')

        self.statusbar_label = QLabel("0/0")

        self.statusBar().addPermanentWidget(self.statusbar_label)

        menubar = self.menuBar()

        self.is_ordered = False

        self.setWindowTitle("Data Analysis App")

        # add submenus to a menu
        file_menu = menubar.addMenu('File')
        help_menu = menubar.addMenu('Help')

        # add an action with a callback
        file_menu.addAction('Quit', self.destroy)

        # add separator
        file_menu.addSeparator()

        toolbar = self.addToolBar('File')

        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setAllowedAreas(
            Qt.TopToolBarArea |
            Qt.BottomToolBarArea
        )

        dock = QDockWidget("Tools")

        dock_loaders_widget = QWidget(self)
        dock_preprocess_widget = QWidget(self)
        dock_regression_widget = QWidget(self)
        dock_classification_widget = QWidget(self)
        dock_clustering_widget = QWidget(self)
        dock_visualization_widget = QWidget(self)
        dock_demux_widget = QWidget(self)

        nodes_list_loaders = DragList()
        nodes_list_preprocess = DragList()
        nodes_list_regression = DragList()
        nodes_list_classification = DragList()
        nodes_list_clustering = DragList()
        nodes_list_visualization = DragList()
        nodes_list_demux = DragList()

        nodes_list_loaders.add_items(['Csv Loader', 'Excel Loader', "Xml Loader", "Deserializer"],
                                     icon="icons/input24.png")
        nodes_list_preprocess.add_items(['Attribute Remover', 'Filter'], icon="icons/both24.png")
        nodes_list_regression.add_items(['Linear Regression'], icon="icons/both24.png")
        nodes_list_classification.add_items(['Knn', 'SVM', 'Naive Bayes', 'Decision Tree'], icon="icons/both24.png")
        nodes_list_clustering.add_items(['K-Means', "Hierarchical"], icon="icons/both24.png")
        nodes_list_visualization.add_items(["Text output", "Scatter plot", "Pie Chart", "Predictor", "Serializer",
                                            "Simple Plot", "Histogram", "Csv Saver"], icon="icons/output24.png")
        nodes_list_demux.add_items(["1x2 Demux", "1x3 Demux", "1x4 Demux", "1x5 Demux"], icon="icons/demux.png")

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        tab_widget = QTabWidget()
        tab_widget.setMovable(False)
        tab_widget.setTabPosition(QTabWidget.West)
        tab_widget.resize(100, 100)

        dock_layout_loaders = QHBoxLayout()
        dock_layout_preprocess = QHBoxLayout()
        dock_layout_regression = QHBoxLayout()
        dock_layout_classification = QHBoxLayout()
        dock_layout_clustering = QHBoxLayout()
        dock_layout_visualization = QHBoxLayout()
        dock_layout_demux = QHBoxLayout()

        dock_loaders_widget.setLayout(dock_layout_loaders)
        dock_preprocess_widget.setLayout(dock_layout_preprocess)
        dock_regression_widget.setLayout(dock_layout_regression)
        dock_classification_widget.setLayout(dock_layout_classification)
        dock_clustering_widget.setLayout(dock_layout_clustering)
        dock_visualization_widget.setLayout(dock_layout_visualization)
        dock_demux_widget.setLayout(dock_layout_demux)

        # dock_layout.addWidget(tab_widget)

        dock_layout_loaders.addWidget(nodes_list_loaders)
        dock_layout_preprocess.addWidget(nodes_list_preprocess)
        dock_layout_regression.addWidget(nodes_list_regression)
        dock_layout_classification.addWidget(nodes_list_classification)
        dock_layout_clustering.addWidget(nodes_list_clustering)
        dock_layout_visualization.addWidget(nodes_list_visualization)
        dock_layout_demux.addWidget(nodes_list_demux)

        tab_widget.addTab(dock_loaders_widget, 'Inputs')
        tab_widget.addTab(dock_preprocess_widget, 'Preprocessors')
        tab_widget.addTab(dock_regression_widget, 'Regression')
        tab_widget.addTab(dock_classification_widget, 'Classification')
        tab_widget.addTab(dock_clustering_widget, 'Clustering')
        tab_widget.addTab(dock_visualization_widget, 'Output')
        tab_widget.addTab(dock_demux_widget, "Demux")

        dock.setWidget(tab_widget)

        help_menu.addAction('About', self.show_about_dialog)
        # TODO: Give credit for licence owner
        help_menu.addAction("Credits", self.credits)
        help_menu.addAction("Node List", self.print_paths)

        self.show()

    def print_paths(self):
        print(self.main_widget)
        print(self.main_widget.nodes)
        print("there is " + str(len(self.main_widget.nodes)) + " nodes exist on the scene")
        for edge in self.main_widget.edges:
            print("from " + edge.start_socket.node.title + " to " + edge.end_socket.node.title)
        self.order_path()
        print("printing the ordered nodes")
        for inner_list in self.ordered_nodes:
            for path in inner_list:
                print("{}-".format(path.title), end="")
            print("")

    def order_path(self):
        first_node = None
        self.is_ordered = True
        self.ordered_nodes = [[]]
        for node in self.main_widget.nodes:
            if isinstance(node, Node) and node.is_first:
                first_node = node

        self.append_nodes_by_order(first_node, self.ordered_nodes[0])

    def append_nodes_by_order(self, node, l):
        if isinstance(node, Node):
            l.append(node)
            if node.is_last:
                return
        while True:
            if not l[-1].output_socket.has_edge() and not l[-1].is_last:
                QMessageBox.critical(self, "Warning!", "Every path must end with an output socket!")
                self.is_ordered = False
                return
            next_node = l[-1].output_socket.edge.end_socket.node
            if isinstance(next_node, NodeDemux):
                copied_lists = []
                for i in range(len(next_node.output_sockets) - 1):
                    copied_lists.append([])

                for i, socket in enumerate(next_node.output_sockets):
                    if i == len(next_node.output_sockets) - 1:
                        self.append_nodes_by_order(socket.edge.end_socket.node, l)
                    else:
                        for item in l:
                            copied_lists[i].append(item)
                        self.ordered_nodes.append(copied_lists[i])
                        if not socket.has_edge():
                            QMessageBox.critical(self, "Warning!", "Every demux sockets must be connected to a node!")
                            self.is_ordered = False
                            return
                        self.append_nodes_by_order(socket.edge.end_socket.node, copied_lists[i])
                break
            l.append(next_node)
            if next_node.is_last:
                break

    def feed_next_node(self, node):
        for ordered_nodes in self.ordered_nodes:
            try:
                i = ordered_nodes.index(node)
            except ValueError:
                continue
            ordered_nodes[i + 1].feed(node.output)

    def show_about_dialog(self):
        QMessageBox.about(
            self,
            "About",
            "This is a data analysis app written in PyQt5."
        )

    def change_statusbar_text(self):
        completed_count = 0
        set_of_nodes = set()
        for node in self.main_widget.nodes:
            if node not in set_of_nodes:
                if isinstance(node, Node) and node.is_finished:
                    completed_count += 1
                set_of_nodes.add(node)
        self.statusbar_label.setText("{}/{}".format(completed_count, len(self.main_widget.nodes)))

    def credits(self):
        QMessageBox.about(
            self,
            "Acknowledgements",
            "I would like to appreciate Freepik and Pixel Perfect for the icons they provided."
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
