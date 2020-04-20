import os
import sys
import pickle

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pandas as pd

sys.path.append(os.path.abspath(os.path.join("..")))
from node import Node


class TextOutput(Node):
    fed_data = None

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
        # TODO: create a method which saves the file
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
        if isinstance(self.fed_data, dict):
            from sklearn.metrics import confusion_matrix
            from sklearn.metrics import classification_report

            model = self.fed_data["model"]
            X_test, y_test = self.fed_data["test_data"]

            y_predicted = model.predict(X_test)
            conf_matrix = confusion_matrix(y_test, y_predicted)
            report = classification_report(y_test, y_predicted)
            with open(self.directory, "w+") as fd:
                fd.write("Confusion Matrix:\n")
                fd.write(str(conf_matrix))
                fd.write("\nAccuracy Score {}".format(model.score(X_test, y_test)))
                fd.write("\nClassification Report:\n")
                fd.write(report)

        else:
            with open(self.directory, "w+") as fd:
                fd.write(str(self.fed_data.describe()))
        print("save completed")

    def feed(self, df_or_model):
        self.fed_data = df_or_model


class Predictor(Node):
    fed_data = None
    scroll_area = None
    gridLayout = None
    scroll_area_widget_contents = None
    formLayout = None
    labels = None
    input_widgets = None

    def __init__(self, scene):
        super().__init__(scene, title="Predictor", inputs=1, outputs=0)
        self.is_last = True

    def run(self):
        if not self.fed_data or not isinstance(self.fed_data, dict):
            QMessageBox.about(
                self.scene.parent_widget,
                "Warning!",
                "You need to complete preceding nodes first."
            )
            return
        self.dialog = QDialog()
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setup_ui(self.dialog)
        self.dialog.show()

    def setup_ui(self, dialog):
        dialog.setObjectName("Dialog")
        dialog.resize(429, 353)
        self.gridLayout = QGridLayout(dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scroll_area = QScrollArea(dialog)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 409, 277))
        self.scroll_area_widget_contents.setObjectName("scroll_area_widget_contents")
        self.formLayout = QFormLayout(self.scroll_area_widget_contents)
        self.formLayout.setObjectName("formLayout")

        df = self.fed_data["data_frame"]
        target_label = self.fed_data["target_label"]

        self.labels = []
        self.input_widgets = []

        self.data_types = dict(df.dtypes)

        for i in range(len(df.columns)):
            if target_label == str(df.columns[i]):
                continue
            self.labels.append(QLabel(self.scroll_area_widget_contents))
            self.labels[-1].setText("{} ({})".format(str(df.columns[i]), self.data_types[df.columns[i]]))
            if "object" in str(self.data_types[df.columns[i]]):
                # TODO: categorical predictions
                self.input_widgets.append(QComboBox(self.scroll_area_widget_contents))
            else:
                self.input_widgets.append(QLineEdit(self.scroll_area_widget_contents))
            self.formLayout.addRow(self.labels[-1], self.input_widgets[-1])

        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        self.gridLayout.addWidget(self.scroll_area, 0, 0, 1, 1)
        self.result_label = QLabel(dialog)
        self.result_label.setObjectName("result_label")
        self.gridLayout.addWidget(self.result_label, 1, 0, 1, 1)
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        _translate = QCoreApplication.translate

        dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.result_label.setText("Result not computed yet")

        self.buttonBox.accepted.connect(self.predict)
        self.buttonBox.rejected.connect(dialog.reject)
        QMetaObject.connectSlotsByName(dialog)

    def predict(self):
        v = []
        df = self.fed_data["data_frame"]
        model = self.fed_data["model"]
        for i, widget in enumerate(self.input_widgets):
            if "float" in str(self.data_types[df.columns[i]]):
                v.append(float(widget.text()))
            elif "int" in str(self.data_types[df.columns[i]]):
                v.append(float(widget.text()))
        result = model.predict([v])
        self.result_label.setText("Result is: {}".format(result[0]))

    def feed(self, df_or_model):
        self.fed_data = df_or_model


class Serializer(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Serializer", inputs=1, outputs=0)
        self.is_last = True
        self.node_type = "visualisation.serializer"

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
        self.buttonBox.accepted.connect(self.save_object)
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

    def save_object(self):
        with open(self.lineEdit.text(), "wb") as f:
            pickle.dump(self.fed_data, f)
        print("save completed")

    def feed(self, model):
        self.fed_data = model


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
