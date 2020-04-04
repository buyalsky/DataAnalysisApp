import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pandas as pd

sys.path.append(os.path.abspath(os.path.join("..")))
from node import Node


class TextOutput(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Text Output", inputs=1, outputs=0)
        self.is_last = True
        self.node_type = "visualisation.text"

    def run(self):
        self.dialog = QDialog()
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setupUi(self.dialog)
        self.dialog.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(398, 167)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(30, 120, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QWidget(Dialog)
        self.widget.setGeometry(QRect(10, 30, 381, 81))
        self.widget.setObjectName("widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QLabel(self.widget)
        font = QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.pushButton.clicked.connect(self.select_directory)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Select Directory"))
        self.pushButton.setText(_translate("Dialog", "Select"))
        self.label_2.setText(_translate("Dialog", "Text file will be saved to the directory you select."))

    def select_directory(self):
        self.directory, _ = QFileDialog.getSaveFileName(QMainWindow(), "Save as", QDir.homePath(), "Text files (*.txt)",
                                    options=QFileDialog.DontResolveSymlinks | QFileDialog.DontUseNativeDialog)
        self.lineEdit.setText(self.directory)
        if isinstance(self.df_or_model, pd.core.frame.DataFrame):
            with open(self.directory, "w+") as fd:
                fd.write(str(self.df_or_model.describe()))
        else:
            with open(self.directory, "w+") as fd:
                fd.write("Score {}".format(self.df_or_model.score()))
            print("save completed")

    def feed(self, df_or_model):
        self.df_or_model = df_or_model



class ScatterPlot(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Scatter Plot", inputs=1, outputs=0)
        self.is_last = True
        self.node_type = "visualisation.scatter"


class Histogram(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Histogram", inputs=1, outputs=0)
        self.is_last = True
        self.node_type = "visualisation.histogram"
