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
        self.main_widget = MainWidget()
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
        charcount_label = QLabel("chars: 0")

        self.statusBar().addPermanentWidget(charcount_label)

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

        # create a toolbar in another part of the screen:
        #toolbar2 = QToolBar('Edit')
        #self.addToolBar(Qt.RightToolBarArea, toolbar2)
        #toolbar2.addAction('Copy', self.textedit.copy)
        #toolbar2.addAction('Cut', self.textedit.cut)
        #toolbar2.addAction('Paste', self.textedit.paste)

        dock = QDockWidget("Tools")
        dock_inner_widget = QWidget(self)
        nodes_list_widget = DragList()
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        dock_layout = QHBoxLayout()
        tab_widget = QTabWidget(
            movable=False,
            tabPosition=QTabWidget.West,
            tabShape=QTabWidget.TabShape
        )
        tab_widget.resize(100,100)
        container = QWidget(self)
        subwidget = QWidget(self)
        dock_inner_widget.setLayout(dock_layout)
        #dock_layout.addWidget(tab_widget)
        dock_layout.addWidget(nodes_list_widget)

        tab_widget.addTab(dock_inner_widget, 'Tab 1')
        tab_widget.addTab(subwidget, 'Tab 2')

        dock.setWidget(tab_widget)


        search_and_replace_btn = QPushButton("Print path", clicked=self.print_paths)

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
        print("there is " + str(len(self.main_widget.nodes)) + "nodes exist on the scene")
        for edge in self.main_widget.edges:
            print("from " + edge.start_socket.node.title + " to " + edge.end_socket.node.title)


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
