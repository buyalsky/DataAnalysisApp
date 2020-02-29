import sys
from PyQt5.QtWidgets import *

from main_widget import MainWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = MainWidget()

    sys.exit(app.exec_())
