import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from main_widget import MainWidget
from drag_list import DragList
from node import Node, NodeDemux


class MainWindow(QMainWindow):
    settings = QSettings('Burak Dursunlar', 'Data analysis app')

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
        edit_menu = menubar.addMenu('Edit')
        help_menu = menubar.addMenu('Help')

        # add actions
        open_action = file_menu.addAction('Open')
        save_action = file_menu.addAction('Save')

        # add separator
        file_menu.addSeparator()

        # add an action with a callback
        quit_action = file_menu.addAction('Quit', self.destroy)

        redo_action = QAction('Redo', self)
        edit_menu.addAction(redo_action)

        toolbar = self.addToolBar('File')
        # toolbar.addAction(open_action)
        # toolbar.addAction("Save")

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

        nodes_list_loaders.add_items(['Csv Loader', 'Excel Loader', "Xml Loader", "Deserializer"])
        nodes_list_preprocess.add_items(['Attribute Remover', 'Filter'])
        nodes_list_regression.add_items(['Linear Regression'])
        nodes_list_classification.add_items(['Knn', 'SVM', 'Naive Bayes', 'Decision Tree'])
        nodes_list_clustering.add_items(['K-Means', "Hierarchical"])
        nodes_list_visualization.add_items(["Text output", "Scatter plot", "Pie Chart", "Predictor", "Serializer",
                                            "Simple Plot", "Histogram", "Csv Saver"])
        nodes_list_demux.add_items(["1x2 Demux", "1x3 Demux", "1x4 Demux", "1x5 Demux"])

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        tab_widget = QTabWidget(
            movable=False,
            tabPosition=QTabWidget.West,
            tabShape=QTabWidget.TabShape
        )
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

        # QMessageBox
        help_menu.addAction('About', self.show_about_dialog)
        help_menu.addAction("Node List", self.print_paths)

        if self.settings.value('show_warnings', False, type=bool):
            response = QMessageBox.question(
                self,
                'My Text Editor',
                'This is beta software, do you want to continue?',
                QMessageBox.Yes | QMessageBox.Abort
            )
            if response == QMessageBox.Abort:
                self.close()
                sys.exit()

            # custom message box

            splash_screen = QMessageBox()
            splash_screen.setWindowTitle('My Text Editor')
            splash_screen.setText('BETA SOFTWARE WARNING!')
            splash_screen.setInformativeText(
                'This is very, very beta, '
                'are you really sure you want to use it?'
            )
            splash_screen.setDetailedText(
                'This editor was written for pedagogical '
                'purposes, and probably is not fit for real work.'
            )
            splash_screen.setWindowModality(Qt.WindowModal)
            splash_screen.addButton(QMessageBox.Yes)
            splash_screen.addButton(QMessageBox.Abort)
            response = splash_screen.exec_()
            if response == QMessageBox.Abort:
                self.close()
                sys.exit()

        # QFileDialog
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)

        # QFontDialog
        edit_menu.addAction('Set Font…', self.set_font)

        # Custom dialog
        edit_menu.addAction('Settings…', self.show_settings)
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
            "About main_window.py",
            "This is a data analysis app written in PyQt5."
        )

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a text file to open…",
            QDir.homePath(),
            'Text Files (*.txt) ;;Python Files (*.py) ;;All Files (*)',
            'Python Files (*.py)',
            QFileDialog.DontUseNativeDialog |
            QFileDialog.DontResolveSymlinks
        )
        if filename:
            try:
                with open(filename, 'r') as fh:
                    self.main_widget.setText(fh.read())
            except Exception as e:
                QMessageBox.critical(f"Could not load file: {e}")

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Select the file to save to…",
            QDir.homePath(),
            'Text Files (*.txt) ;;Python Files (*.py) ;;All Files (*)'
        )
        if filename:
            try:
                with open(filename, 'w') as fh:
                    fh.write(self.main_widget.toPlainText())
            except Exception as e:
                QMessageBox.critical(f"Could not save file: {e}")

    def set_font(self):
        current = self.main_widget.currentFont()
        font, accepted = QFontDialog.getFont(
            current,
            self,
            options=(
                    QFontDialog.DontUseNativeDialog |
                    QFontDialog.MonospacedFonts
            )
        )
        if accepted:
            self.main_widget.setCurrentFont(font)

    def show_settings(self):
        settings_dialog = SettingsDialog(self.settings, self)
        settings_dialog.exec()

    def change_statusbar_text(self):
        completed_count = 0
        set_of_nodes = set()
        for node in self.main_widget.nodes:
            if node not in set_of_nodes:
                if isinstance(node, Node) and node.is_finished:
                    completed_count += 1
                set_of_nodes.add(node)
        self.statusbar_label.setText("{}/{}".format(completed_count, len(self.main_widget.nodes)))


class SettingsDialog(QDialog):
    """Dialog for setting the settings"""

    def __init__(self, settings, parent=None):
        super().__init__(parent, modal=True)
        self.setLayout(QFormLayout())
        self.settings = settings
        self.layout().addRow(
            QLabel('<h1>Application Settings</h1>'),
        )
        self.show_warnings_cb = QCheckBox(
            # checked=settings.get('show_warnings')
            checked=settings.value('show_warnings', type=bool)
        )
        self.layout().addRow("Show Warnings", self.show_warnings_cb)

        self.accept_btn = QPushButton('Ok', clicked=self.accept)
        self.cancel_btn = QPushButton('Cancel', clicked=self.reject)
        self.layout().addRow(self.accept_btn, self.cancel_btn)

    def accept(self):
        # self.settings['show_warnings'] = self.show_warnings_cb.isChecked()
        self.settings.setValue(
            'show_warnings',
            self.show_warnings_cb.isChecked()
        )
        print(self.settings.value('show_warnings'))
        super().accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
