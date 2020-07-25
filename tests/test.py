import os
import sys

import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import main_window


@pytest.fixture
def app(qtbot):
    test_hello_app = main_window.MainWindow()
    qtbot.addWidget(test_hello_app)

    return test_hello_app


class TestMainScreen:
    def test1(self):
        assert 2 + 2 == 4

    def test_statusbar(self, app):
        assert app.statusbar_label.text() == "0/0"

