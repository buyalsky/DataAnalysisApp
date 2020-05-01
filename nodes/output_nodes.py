import os
import sys
import pickle

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from matplotlib import pyplot as plt

sys.path.append(os.path.abspath(os.path.join("..")))
from node import OutputNode


class TextOutput(OutputNode):
    line_edit = None

    def __init__(self, scene):
        super().__init__(scene, title="Text Output")
        self.node_type = "visualisation.text"

    def run(self):
        self.dialog = QDialog()
        self.dialog.setModal(True)
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setup_ui()
        self.dialog.show()

    def setup_ui(self):
        self.dialog.resize(398, 167)
        button_box = QDialogButtonBox(self.dialog)
        button_box.setGeometry(QRect(30, 120, 341, 32))
        button_box.setOrientation(Qt.Horizontal)
        button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        widget = QWidget(self.dialog)
        widget.setGeometry(QRect(10, 30, 381, 81))
        vertical_layout = QVBoxLayout(widget)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout = QHBoxLayout()
        label = QLabel(widget)
        horizontal_layout.addWidget(label)
        self.line_edit = QLineEdit(widget)
        horizontal_layout.addWidget(self.line_edit)
        push_button = QPushButton(widget)
        horizontal_layout.addWidget(push_button)
        vertical_layout.addLayout(horizontal_layout)
        label_info = QLabel(widget)
        font = QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(10)
        label_info.setFont(font)
        vertical_layout.addWidget(label_info)

        self.dialog.setWindowTitle("Text Output")
        label.setText("Select Directory")
        push_button.setText("Select")
        label_info.setText("Text file will be saved to the directory you select.")

        button_box.accepted.connect(self.save_file)
        button_box.rejected.connect(self.dialog.reject)
        push_button.clicked.connect(self.select_directory)
        QMetaObject.connectSlotsByName(self.dialog)

    def select_directory(self):
        directory, _ = QFileDialog.getSaveFileName(QMainWindow(), "Save as", QDir.homePath(), "Text files (*.txt)",
                                                   options=QFileDialog.DontResolveSymlinks | QFileDialog.
                                                   DontUseNativeDialog)
        self.line_edit.setText(directory)

    def save_file(self):
        directory = self.line_edit.text()
        if not directory:
            QMessageBox.warning(
                self.dialog,
                "Warning!",
                "You need to specify a directory."
            )
            return
        if isinstance(self.fed_data, dict):
            from sklearn.metrics import confusion_matrix
            from sklearn.metrics import classification_report

            model = self.fed_data["model"]
            X_test, y_test = self.fed_data["test_data"]

            y_predicted = model.predict(X_test)
            conf_matrix = confusion_matrix(y_test, y_predicted)
            report = classification_report(y_test, y_predicted)
            with open(directory, "w+") as fd:
                fd.write("Confusion Matrix:\n")
                fd.write(str(conf_matrix))
                fd.write("\nAccuracy Score {}".format(model.score(X_test, y_test)))
                fd.write("\nClassification Report:\n")
                fd.write(report)

        else:
            with open(directory, "w+") as fd:
                fd.write(str(self.fed_data.describe()))
        print("save completed")
        self.dialog.accept()

    def feed(self, df_or_model):
        self.fed_data = df_or_model


class Predictor(OutputNode):
    data_types = None
    result_label = None
    input_widgets = None

    def __init__(self, scene):
        super().__init__(scene, title="Predictor")

    def run(self):
        if not self.fed_data or not isinstance(self.fed_data, dict):
            QMessageBox.about(
                self.scene.parent_widget,
                "Warning!",
                "You need to complete preceding nodes first."
            )
            return
        self.dialog = QDialog()
        self.dialog.setModal(True)
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setup_ui()
        self.dialog.show()

    def setup_ui(self):
        self.dialog.resize(429, 353)
        grid_layout = QGridLayout(self.dialog)
        scroll_area = QScrollArea(self.dialog)
        scroll_area.setWidgetResizable(True)
        scroll_area_widget_contents = QWidget()
        scroll_area_widget_contents.setGeometry(QRect(0, 0, 409, 277))
        scroll_area_widget_contents.setObjectName("scroll_area_widget_contents")
        form_layout = QFormLayout(scroll_area_widget_contents)

        df = self.fed_data["data_frame"]
        target_label = self.fed_data["target_label"]

        labels = []
        self.input_widgets = []

        self.data_types = dict(df.dtypes)

        for i in range(len(df.columns)):
            if target_label == str(df.columns[i]):
                continue
            labels.append(QLabel(scroll_area_widget_contents))
            labels[-1].setText("{} ({})".format(str(df.columns[i]), self.data_types[df.columns[i]]))
            if "object" in str(self.data_types[df.columns[i]]):
                # TODO: categorical predictions
                self.input_widgets.append(QComboBox(scroll_area_widget_contents))
            else:
                self.input_widgets.append(QLineEdit(scroll_area_widget_contents))
            form_layout.addRow(labels[-1], self.input_widgets[-1])

        scroll_area.setWidget(scroll_area_widget_contents)

        grid_layout.addWidget(scroll_area, 0, 0, 1, 1)
        self.result_label = QLabel(self.dialog)
        grid_layout.addWidget(self.result_label, 1, 0, 1, 1)
        button_box = QDialogButtonBox(self.dialog)
        button_box.setOrientation(Qt.Horizontal)
        button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        grid_layout.addWidget(button_box, 2, 0, 1, 1)

        self.dialog.setWindowTitle("Predictor")
        self.result_label.setText("Result not computed yet")

        button_box.accepted.connect(self.predict)
        button_box.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

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


class Serializer(OutputNode):
    line_edit = None

    def __init__(self, scene):
        super().__init__(scene, title="Serializer")
        self.node_type = "visualisation.serializer"

    def run(self):
        self.dialog = QDialog()
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setup_ui()
        self.dialog.show()

    def setup_ui(self):
        self.dialog.resize(398, 167)
        button_box = QDialogButtonBox(self.dialog)
        button_box.setGeometry(QRect(30, 120, 341, 32))
        button_box.setOrientation(Qt.Horizontal)
        button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        widget = QWidget(self.dialog)
        widget.setGeometry(QRect(10, 30, 381, 81))
        vertical_layout = QVBoxLayout(widget)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout = QHBoxLayout()
        label = QLabel(widget)
        horizontal_layout.addWidget(label)
        self.line_edit = QLineEdit(widget)
        horizontal_layout.addWidget(self.line_edit)
        push_button = QPushButton(widget)
        horizontal_layout.addWidget(push_button)
        vertical_layout.addLayout(horizontal_layout)
        label2 = QLabel(widget)
        font = QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(10)
        label2.setFont(font)
        vertical_layout.addWidget(label2)

        self.dialog.setWindowTitle("Dialog")
        label.setText("Select Directory")
        push_button.setText("Select")
        label2.setText("Text file will be saved to the directory you select.")

        button_box.accepted.connect(self.save_object)
        button_box.rejected.connect(self.dialog.reject)
        push_button.clicked.connect(self.select_directory)
        QMetaObject.connectSlotsByName(self.dialog)

    def select_directory(self):
        directory, _ = QFileDialog.getSaveFileName(QMainWindow(), "Save as", QDir.homePath(), "Text files (*.txt)",
                                                   options=QFileDialog.DontResolveSymlinks | QFileDialog.
                                                   DontUseNativeDialog)
        self.line_edit.setText(directory)

    def save_object(self):
        directory = self.line_edit.text()
        if not directory:
            QMessageBox.warning(
                self.dialog,
                "Warning!",
                "You need to specify a directory."
            )
            return
        with open(directory, "wb") as f:
            pickle.dump(self.fed_data, f)
        self.dialog.accept()

    def feed(self, model):
        self.fed_data = model


class SimplePlot(OutputNode):
    style_select_combo_box = None
    check_boxes = None
    title_name_edit = None
    plot_button = None
    combo_box_x = None
    scroll_area_widget_contents = None

    def __init__(self, scene):
        super().__init__(scene, title="Simple Plot")
        self.node_type = "visualisation.simple"

    def run(self):
        self.dialog = QDialog()
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setup_ui()
        self.dialog.show()

    def setup_ui(self):
        self.dialog.resize(606, 459)
        grid_layout = QGridLayout(self.dialog)
        vertical_layout = QVBoxLayout()
        horizontal_layout3 = QHBoxLayout()
        label = QLabel(self.dialog)
        horizontal_layout3.addWidget(label, 30)
        self.combo_box_x = QComboBox(self.dialog)
        horizontal_layout3.addWidget(self.combo_box_x, 70)
        vertical_layout.addLayout(horizontal_layout3)
        horizontal_layout2 = QHBoxLayout()
        label2 = QLabel(self.dialog)
        horizontal_layout2.addWidget(label2, 30)
        scroll_area_y = QScrollArea(self.dialog)
        scroll_area_y.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 532, 269))

        vertical_layout5 = QVBoxLayout(self.scroll_area_widget_contents)
        self.check_boxes = []

        self.combo_box_x.addItem("Not selected yet")
        data_types = dict(self.fed_data.dtypes)
        for i in range(len(self.fed_data.columns)):
            data_type = str(data_types[self.fed_data.columns[i]])
            if "int" in data_type or "float" in data_type:
                c = QCheckBox(self.scroll_area_widget_contents)
                c.setText("{}".format(self.fed_data.columns[i]))
                self.check_boxes.append(c)
                self.combo_box_x.addItem(c.text())
                vertical_layout5.addWidget(c)

        scroll_area_y.setWidget(self.scroll_area_widget_contents)
        horizontal_layout2.addWidget(scroll_area_y, 70)
        vertical_layout.addLayout(horizontal_layout2)
        horizontal_layout = QHBoxLayout()
        label3 = QLabel(self.dialog)
        horizontal_layout.addWidget(label3, 30)
        self.title_name_edit = QLineEdit(self.dialog)
        horizontal_layout.addWidget(self.title_name_edit, 70)
        vertical_layout.addLayout(horizontal_layout)
        horizontal_layout4 = QHBoxLayout()
        label4 = QLabel(self.dialog)
        horizontal_layout4.addWidget(label4, 30)
        self.style_select_combo_box = QComboBox(self.dialog)
        horizontal_layout4.addWidget(self.style_select_combo_box, 70)

        self.style_select_combo_box.addItem("Default style")
        self.style_select_combo_box.addItems(plt.style.available)

        vertical_layout.addLayout(horizontal_layout4)
        self.plot_button = QPushButton(self.dialog)
        self.plot_button.setEnabled(False)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.plot_button.sizePolicy().hasHeightForWidth())
        self.plot_button.setSizePolicy(size_policy)
        vertical_layout.addWidget(self.plot_button)
        grid_layout.addLayout(vertical_layout, 0, 0, 1, 1)
        button_box = QDialogButtonBox(self.dialog)
        button_box.setOrientation(Qt.Horizontal)
        button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        grid_layout.addWidget(button_box, 1, 0, 1, 1)

        self.dialog.setWindowTitle("Simple Plot")
        label.setText("X axis")
        label2.setText("Y axis")
        label3.setText("Title name")
        label4.setText("Style select")
        self.plot_button.setText("Plot")

        button_box.accepted.connect(self.dialog.accept)
        button_box.rejected.connect(self.dialog.reject)
        self.plot_button.clicked.connect(self.plot_data)
        self.combo_box_x.currentTextChanged.connect(self.x_axis_changed)

        for checkbox in self.check_boxes:
            checkbox.clicked.connect(self.checkbox_selected)

        QMetaObject.connectSlotsByName(self.dialog)

    def plot_data(self):
        if self.style_select_combo_box.currentText() != "Default style":
            plt.style.use(self.style_select_combo_box.currentText())

        x_axis = self.fed_data[self.combo_box_x.currentText()]
        for check_box in self.check_boxes:
            if check_box.isChecked():
                plt.plot(x_axis, self.fed_data[check_box.text()], label=check_box.text())

        if self.title_name_edit.text():
            plt.title(self.title_name_edit.text())

        plt.legend()

        plt.tight_layout()

        plt.show()

    def x_axis_changed(self, text):
        if text == "Not selected yet":
            self.plot_button.setEnabled(False)
            for checkbox in self.check_boxes:
                checkbox.setEnabled(True)
        else:
            self.disable_checkbox(text)

    def checkbox_selected(self):
        for checkbox in self.check_boxes:
            if checkbox.isEnabled() and checkbox.isChecked():
                if self.combo_box_x.currentText() != "Not selected yet":
                    self.plot_button.setEnabled(True)
                    return
        self.plot_button.setEnabled(False)

    def disable_checkbox(self, text):
        for checkbox in self.check_boxes:
            if checkbox.text() == text:
                checkbox.setEnabled(False)
            else:
                checkbox.setEnabled(True)

    def feed(self, model):
        self.fed_data = model


class ScatterPlot(OutputNode):
    def __init__(self, scene):
        super().__init__(scene, title="Scatter Plot")
        self.node_type = "visualisation.scatter"


class Histogram(OutputNode):
    def __init__(self, scene):
        super().__init__(scene, title="Histogram")
        self.node_type = "visualisation.histogram"
