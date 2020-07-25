import os
import sys

import pytest

try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import main_window
from drag_list import NODES_TO_ICONS


@pytest.fixture
def app(qtbot):
    test_hello_app = main_window.MainWindow()
    qtbot.addWidget(test_hello_app)

    return test_hello_app


class TestMainScreen:
    def test_statusbar(self, app):
        assert app.statusbar_label.text() == "0/0"

    def test_menubar(self, app):
        menu_list: [QMenu] = app.menuBar().findChildren(QMenu, "")
        assert len(menu_list) == 2

    def test_dock_widget(self, app):
        dock = app.findChildren(QDockWidget, "")[0]
        drag_lists = dock.findChildren(QListWidget, "")
        assert len(drag_lists) == 7
        for drag_list in drag_lists:
            for i in range(drag_list.count()):
                if "Demux" in drag_list.item(i).text():
                    continue
                assert NODES_TO_ICONS.get(drag_list.item(i).text())
