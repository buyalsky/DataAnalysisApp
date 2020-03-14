import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from main_widget import MainWidget
from drag_list import DragList

class MainWindow(QMainWindow): # change to mainwindow

    #settings = {'show_warnings': True}
    settings = QSettings('Alan D Moore', 'text editor')

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here

        ######################
        # The central widget #
        ######################
        #self.textedit = QTextEdit()
        self.main_widget = MainWidget(parent_window=self)
        self.setCentralWidget(self.main_widget)

        #################
        # The Statusbar #
        #################

        # The long way 'round
        #status_bar = QStatusBar()
        #self.setStatusBar(status_bar)
        #status_bar.showMessage('Welcome to text_editor.py')

        # The short way 'round
        self.statusBar().showMessage('Ready')

        # add widgets to statusbar
        self.statusbar_label = QLabel("0/0")

        self.statusBar().addPermanentWidget(self.statusbar_label)

        ###############j
        # The menubar #
        ###############
        menubar = self.menuBar()

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

        # connect to a Qt Slot

        # create a QAction manually

        redo_action = QAction('Redo', self)
        edit_menu.addAction(redo_action)

        ############################
        # The Toolbar and QActions #
        ############################

        toolbar = self.addToolBar('File')
        #toolbar.addAction(open_action)
        #toolbar.addAction("Save")

        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setAllowedAreas(
            Qt.TopToolBarArea |
            Qt.BottomToolBarArea
        )

        # Add with icons
        open_icon = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        save_icon = self.style().standardIcon(QStyle.SP_DriveHDIcon)
        run_icon = self.style().standardIcon(QStyle.SP_MediaPlay)
        open_action.setIcon(open_icon)
        toolbar.addAction(open_action)
        toolbar.addAction(
            save_icon,
            'Save',
            lambda: self.statusBar().showMessage('File Saved!')
        )
        toolbar.addAction(run_icon, 'Run', lambda :None)
        # create a custom QAction

        help_action = QAction(
            self.style().standardIcon(QStyle.SP_DialogHelpButton),
            'Help',
            self,  # important to pass the parent!
            triggered=self.print_paths
        )
        toolbar.addAction(help_action)

        dock = QDockWidget("Tools")

        dock_loaders_widget = QWidget(self)
        dock_preprocess_widget = QWidget(self)
        dock_regression_widget = QWidget(self)
        dock_classification_widget = QWidget(self)
        dock_clustering_widget = QWidget(self)
        dock_visualization_widget = QWidget(self)


        nodes_list_loaders = DragList()
        nodes_list_preprocess = DragList()
        nodes_list_regression = DragList()
        nodes_list_classification = DragList()
        nodes_list_clustering = DragList()
        nodes_list_visualization = DragList()

        nodes_list_loaders.add_my_items(['Csv Loader', 'Excel Loader'])
        nodes_list_preprocess.add_my_items(['Attribute Remover', 'Filter'])
        nodes_list_regression.add_my_items(['Linear Regression'])
        nodes_list_classification.add_my_items(['Knn', 'SVM', 'Naive Bayes', 'Decision Tree', 'Decision Tree'])
        nodes_list_clustering.add_my_items(['K-means', "Hierarchical"])
        nodes_list_visualization.add_my_items(["Text output", "Scatter plot", "Histogram"])

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


        dock_loaders_widget.setLayout(dock_layout_loaders)
        dock_preprocess_widget.setLayout(dock_layout_preprocess)
        dock_regression_widget.setLayout(dock_layout_regression)
        dock_classification_widget.setLayout(dock_layout_classification)
        dock_clustering_widget.setLayout(dock_layout_clustering)
        dock_visualization_widget.setLayout(dock_layout_visualization)

        #dock_layout.addWidget(tab_widget)

        dock_layout_loaders.addWidget(nodes_list_loaders)
        dock_layout_preprocess.addWidget(nodes_list_preprocess)
        dock_layout_regression.addWidget(nodes_list_regression)
        dock_layout_classification.addWidget(nodes_list_classification)
        dock_layout_clustering.addWidget(nodes_list_clustering)
        dock_layout_visualization.addWidget(nodes_list_visualization)


        tab_widget.addTab(dock_loaders_widget, 'Tab 1')
        tab_widget.addTab(dock_preprocess_widget, 'Tab 2')
        tab_widget.addTab(dock_regression_widget, 'Tab 3')
        tab_widget.addTab(dock_classification_widget, 'Tab 4')
        tab_widget.addTab(dock_clustering_widget, 'Tab 5')
        tab_widget.addTab(dock_visualization_widget, 'Tab 6')

        dock.setWidget(tab_widget)

        # QMessageBox
        help_menu.addAction('About', self.showAboutDialog)

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
        open_action.triggered.connect(self.openFile)
        save_action.triggered.connect(self.saveFile)

        # QFontDialog

        edit_menu.addAction('Set Font…', self.set_font)

        # Custom dialog
        edit_menu.addAction('Settings…', self.show_settings)

        ###################
        # Saving Settings #
        ###################


        # End main UI code
        self.show()

    def print_paths(self):
        print(self.main_widget)
        print(self.main_widget.nodes)
        print("there is " + str(len(self.main_widget.nodes)) + " nodes exist on the scene")
        for edge in self.main_widget.edges:
            print("from " + edge.start_socket.node.title + " to " + edge.end_socket.node.title)
        self.order_path()
        print("printing the ordered nodes")
        for node in self.ordered_nodes:
            print(node.title)

    def order_path(self):
        first_node = None
        last_node = None
        self.ordered_nodes = []
        for node in self.main_widget.nodes:
            if node.is_first:
                first_node = node
            if node.is_last:
                last_node = node

        assert first_node is not None and last_node is not None
        self.ordered_nodes.append(first_node)

        while len(self.ordered_nodes) < len(self.main_widget.nodes) -1:
            self.ordered_nodes.append(self.ordered_nodes[-1].output_socket.edge.end_socket.node)
        self.ordered_nodes.append(last_node)

    def feed_next_node(self, node):
        i = self.ordered_nodes.index(node)
        self.ordered_nodes[i+1].feed(node.output)


    def showAboutDialog(self):
        QMessageBox.about(
            self,
            "About text_editor.py",
            "This is a text editor written in PyQt5."
        )

    def openFile(self):
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

    def saveFile(self):
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
        for node in self.main_widget.nodes:
            if node.is_finished:
                completed_count += 1
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
            #checked=settings.get('show_warnings')
            checked=settings.value('show_warnings', type=bool)
        )
        self.layout().addRow("Show Warnings", self.show_warnings_cb)

        self.accept_btn = QPushButton('Ok', clicked=self.accept)
        self.cancel_btn = QPushButton('Cancel', clicked=self.reject)
        self.layout().addRow(self.accept_btn, self.cancel_btn)

    def accept(self):
        #self.settings['show_warnings'] = self.show_warnings_cb.isChecked()
        self.settings.setValue(
            'show_warnings',
            self.show_warnings_cb.isChecked()
        )
        print(self.settings.value('show_warnings'))
        super().accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
