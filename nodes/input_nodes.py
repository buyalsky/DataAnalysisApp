import sys
import os
import pickle

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
sys.path.append(os.path.abspath(os.path.join("..")))
from node import InputNode
import xml.etree.ElementTree as ET


class CsvLoader(InputNode):
    button_box = None
    widget = None
    label = None
    label2 = None
    label3 = None
    label4 = None
    label5 = None
    line_edit = None
    push_button = None
    widget1 = None
    vertical_layout = None
    horizontal_layout = None
    horizontal_layout2 = None
    horizontal_layout3 = None
    horizontal_layout4 = None
    horizontal_layout5 = None
    combo_box = None
    combo_box2 = None
    combo_box3 = None
    combo_box4 = None

    def __init__(self, scene):
        super().__init__(scene, title="Csv Loader")
        self.node_type = "loader.csv"

    def setup_ui(self):
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(372, 324)
        self.button_box = QDialogButtonBox(self.dialog)
        self.button_box.setGeometry(QRect(10, 280, 341, 32))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setObjectName("buttonBox")
        self.widget = QWidget(self.dialog)
        self.widget.setGeometry(QRect(20, 30, 331, 41))
        self.widget.setObjectName("widget")
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setObjectName("horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontal_layout.addWidget(self.label)
        self.line_edit = QLineEdit(self.widget)
        self.line_edit.setObjectName("lineEdit")
        self.horizontal_layout.addWidget(self.line_edit)
        self.push_button = QPushButton(self.widget)
        self.push_button.setObjectName("pushButton")
        self.horizontal_layout.addWidget(self.push_button)
        self.widget1 = QWidget(self.dialog)
        self.widget1.setGeometry(QRect(20, 80, 331, 161))
        self.widget1.setObjectName("widget1")
        self.vertical_layout = QVBoxLayout(self.widget1)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setObjectName("verticalLayout")
        self.horizontal_layout2 = QHBoxLayout()
        self.horizontal_layout2.setObjectName("horizontalLayout_2")
        self.label2 = QLabel(self.widget1)
        self.label2.setObjectName("label_2")
        self.horizontal_layout2.addWidget(self.label2)
        self.combo_box = QComboBox(self.widget1)
        self.combo_box.setObjectName("comboBox")
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.horizontal_layout2.addWidget(self.combo_box)
        self.vertical_layout.addLayout(self.horizontal_layout2)
        self.horizontal_layout3 = QHBoxLayout()
        self.horizontal_layout3.setObjectName("horizontalLayout_3")
        self.label3 = QLabel(self.widget1)
        self.label3.setObjectName("label_3")
        self.horizontal_layout3.addWidget(self.label3)
        self.combo_box2 = QComboBox(self.widget1)
        self.combo_box2.setObjectName("comboBox_2")
        self.combo_box2.addItem("")
        self.combo_box2.addItem("")
        self.horizontal_layout3.addWidget(self.combo_box2)
        self.vertical_layout.addLayout(self.horizontal_layout3)
        self.horizontal_layout4 = QHBoxLayout()
        self.horizontal_layout4.setObjectName("horizontalLayout_4")
        self.label4 = QLabel(self.widget1)
        self.label4.setObjectName("label_4")
        self.horizontal_layout4.addWidget(self.label4)
        self.combo_box3 = QComboBox(self.widget1)
        self.combo_box3.setObjectName("comboBox_3")
        self.combo_box3.addItem("")
        self.combo_box3.addItem("")
        self.horizontal_layout4.addWidget(self.combo_box3)
        self.vertical_layout.addLayout(self.horizontal_layout4)
        self.horizontal_layout5 = QHBoxLayout()
        self.horizontal_layout5.setObjectName("horizontalLayout_5")
        self.label5 = QLabel(self.widget1)
        self.label5.setObjectName("label_5")
        self.horizontal_layout5.addWidget(self.label5)
        self.combo_box4 = QComboBox(self.widget1)
        self.combo_box4.setObjectName("comboBox_4")
        self.combo_box4.addItem("")
        self.combo_box4.addItem("")
        self.combo_box4.addItem("")
        self.horizontal_layout5.addWidget(self.combo_box4)
        self.vertical_layout.addLayout(self.horizontal_layout5)

        _translate = QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Select file"))
        self.push_button.setText(_translate("Dialog", "Select"))
        self.label2.setText(_translate("Dialog", "Separator"))
        self.combo_box.setItemText(0, _translate("Dialog", "Comma"))
        self.combo_box.setItemText(1, _translate("Dialog", "Semicolon"))
        self.label3.setText(_translate("Dialog", "Thousands Separator"))
        self.combo_box2.setItemText(0, _translate("Dialog", "Comma"))
        self.combo_box2.setItemText(1, _translate("Dialog", "Dot"))
        self.label4.setText(_translate("Dialog", "Decimal Point Char."))
        self.combo_box3.setItemText(0, _translate("Dialog", "Dot"))
        self.combo_box3.setItemText(1, _translate("Dialog", "Comma"))
        self.label5.setText(_translate("Dialog", "Encoding"))
        self.combo_box4.setItemText(0, _translate("Dialog", "utf-8"))
        self.combo_box4.setItemText(1, _translate("Dialog", "utf-16"))
        self.combo_box4.setItemText(2, _translate("Dialog", "utf-32"))

        self.button_box.accepted.connect(self.return_file)
        self.button_box.rejected.connect(self.dialog.reject)
        self.push_button.clicked.connect(self.file_select_clicked)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        QMetaObject.connectSlotsByName(self.dialog)

    def file_select_clicked(self):
        print("clicked")
        self.fname = QFileDialog.getOpenFileName(QWidget(), "Open File", "C:/", "Csv (*.csv)")
        print("clicked")
        if not self.fname[0]:
            return
        else:
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)

    def return_file(self):
        self.dialog.accept()
        options = ["," if self.combo_box.currentText() == "Comma" else ";",
                   "," if self.combo_box2.currentText() == "Comma" else ".",
                   "," if self.combo_box3.currentText() == "Comma" else ".", self.combo_box4.currentText()]
        self.df = pd.read_csv(self.fname[0], sep=options[0], thousands=options[1],
                              decimal=options[2], encoding=options[3])
        print(self.df.head(10))
        if isinstance(self.df, pd.core.frame.DataFrame):
            self.is_finished = True
            print("completed")
            self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
            #order the nodes
            self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
            #feed the next node
            self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)

        else:
            self.is_finished = False
            print("not completed")


class ExcelLoader(InputNode):
    button_box = None
    widget = None
    horizontal_layout = None
    label = None
    line_edit = None
    push_button = None

    def __init__(self, scene):
        super().__init__(scene, title="Excel Loader")
        self.node_type = "loader.excel"

    def setup_ui(self):
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(372, 134)
        self.button_box = QDialogButtonBox(self.dialog)
        self.button_box.setGeometry(QRect(10, 80, 341, 32))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setObjectName("buttonBox")
        self.widget = QWidget(self.dialog)
        self.widget.setGeometry(QRect(20, 30, 331, 41))
        self.widget.setObjectName("widget")
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setObjectName("horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontal_layout.addWidget(self.label)
        self.line_edit = QLineEdit(self.widget)
        self.line_edit.setObjectName("lineEdit")
        self.horizontal_layout.addWidget(self.line_edit)
        self.push_button = QPushButton(self.widget)
        self.push_button.setObjectName("pushButton")
        self.horizontal_layout.addWidget(self.push_button)

        _translate = QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Select file"))
        self.push_button.setText(_translate("Dialog", "Select"))

        self.button_box.accepted.connect(self.return_file)
        self.button_box.rejected.connect(self.dialog.reject)
        self.push_button.clicked.connect(self.file_select_clicked)
        QMetaObject.connectSlotsByName(self.dialog)

    def file_select_clicked(self):
        print("clicked")
        self.fname = QFileDialog.getOpenFileName(QWidget(), "Open File", "C:/", "Excel (*.xls *.xlsl)")
        print("clicked")
        if not self.fname[0]:
            return

        self.df = pd.read_excel(self.fname[0])
        print(self.df.head(10))


class XmlLoader(InputNode):
    widget = None
    vertical_layout = None
    vertical_layout2 = None
    horizontal_layout = None
    label = None
    line_edit = None
    push_button = None
    tree_widget = None
    buttonBox = None

    def __init__(self, scene):
        super().__init__(scene, title="Xml Loader")
        self.node_type = "loader.xml"

    def setup_ui(self):
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(461, 509)
        self.widget = QWidget(self.dialog)
        self.widget.setGeometry(QRect(30, 40, 401, 421))
        self.widget.setObjectName("widget")
        self.vertical_layout2 = QVBoxLayout(self.widget)
        self.vertical_layout2.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout2.setObjectName("verticalLayout_2")
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontal_layout.addWidget(self.label)
        self.line_edit = QLineEdit(self.widget)
        self.line_edit.setObjectName("lineEdit")
        self.horizontal_layout.addWidget(self.line_edit)
        self.push_button = QPushButton(self.widget)
        self.push_button.setObjectName("pushButton")
        self.horizontal_layout.addWidget(self.push_button)
        self.vertical_layout2.addLayout(self.horizontal_layout)
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName("verticalLayout")
        self.tree_widget = QTreeWidget(self.widget)
        self.tree_widget.setObjectName("treeWidget")

        self.vertical_layout.addWidget(self.tree_widget)
        self.buttonBox = QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vertical_layout.addWidget(self.buttonBox)
        self.vertical_layout2.addLayout(self.vertical_layout)
        self.dialog.setWindowTitle("Dialog")
        self.label.setText("Select File")
        self.push_button.setText("PushButton")
        self.tree_widget.headerItem().setText(0, "1")

        self.buttonBox.accepted.connect(self.print_current)
        self.buttonBox.rejected.connect(self.dialog.reject)
        self.push_button.clicked.connect(self.file_select_clicked)
        QMetaObject.connectSlotsByName(self.dialog)

    def create_dataframe(self):
        self.data = {}
        for option in self.selected_options:
            self.data[option.text(0)] = []
        print(self.data)

        tree = ET.parse(self.fname[0])
        root = tree.getroot()

        for child in root:
            if child.tag == self.top_parent_item.text(0):
                if len(child) > 0:
                    self.add_data_element(child)
                elif child.tag in [option.text(0) for option in self.selected_options]:
                    self.data[child.tag].append(child.text)

        print(self.data)
        self.df = pd.DataFrame(self.data, columns=[option.text(0) for option in self.selected_options])
        print(self.df.head(10))
        # convert columns to best possible data type
        for column in self.df:
            none_count = 0
            int_count = 0
            float_count = 0
            total_count = 0
            if self.df[column].dtype == "object":
                for value in self.df[column].values:
                    if not value or value == "None" or value == "NaN":
                        print("Type of none value: {}".format(type(value)))
                        value = None
                        none_count += 1
                    else:
                        try:
                            int(value)
                            int_count += 1
                        except ValueError:
                            try:
                                float(value)
                                float_count += 1
                            except ValueError:
                                pass
                    total_count += 1
                print("For {}, none_count: {}, int_count: {}, float_count: {}, total_count: {}"
                      .format(column, none_count, int_count, float_count, total_count))

            if int_count == total_count:
                self.df[column] = self.df[column].astype(int)
            elif float_count + none_count == total_count or int_count + none_count == total_count:
                self.df[column] = self.df[column].astype(float)

    def add_data_element(self, root):
        for key, value in root.attrib.items():
            if key in [option.text(0) for option in self.selected_options]:
                self.data[key].append(value)
        for child in root:
            if len(child) > 0:
                self.add_data_element(child)
            elif child.tag in [option.text(0) for option in self.selected_options]:
                self.data[child.tag].append(child.text)

    def print_current(self):
        self.selected_options = []
        print("printing the selected options")
        for option in self.options:
            if option.checkState(0) == Qt.Checked:
                self.selected_options.append(option)
                print(self.selected_options[-1].text(0))
        print(self.check_validity())
        self.create_dataframe()
        self.return_file()

    def check_validity(self):
        self.top_parent_item = self.top_parent(self.selected_options[0])
        for option in self.selected_options:
            print(self.top_parent(option).text(0))
            if option.checkState(0) == Qt.Checked and self.top_parent_item.text(0) != self.top_parent(option).text(0):
                return False
        return True

    def top_parent(self, tree_widget_item):
        if not tree_widget_item.parent():
            return None
        parent_item = tree_widget_item.parent()
        while parent_item.parent():
            parent_item = parent_item.parent()
        return parent_item

    def file_select_clicked(self):
        self.fname = QFileDialog.getOpenFileName(QWidget(), "Open File", "C:/", "Xml files (*.xml)")
        if not self.fname[0]:
            return
        self.main2()

    def main2(self):
        tree = ET.parse(self.fname[0])
        root = tree.getroot()

        #child = root[0]
        self.options = []
        self.create_tree(root, self.tree_widget)

    def create_tree(self, root, tree_widget):
        a = set([child.tag for child in root])
        print(a)

        for child in root:
            if not a:
                break
            if child.tag in a:
                parent = QTreeWidgetItem(tree_widget)
                parent.setText(0, child.tag)
                print(parent.text(0))
                parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                self.create_sub_tree(child, parent)
                a.remove(child.tag)

        print(len(self.options))
        for option in self.options:
            print(option.text(0))

    def create_sub_tree(self, root, parent):
        for key in root.attrib.keys():
            child = QTreeWidgetItem(parent)
            child.setForeground(0, QBrush(QColor(Qt.red)))
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            self.options.append(child)
            child.setText(0, key)
            child.setCheckState(0, Qt.Unchecked)

        for x in root:
            child = QTreeWidgetItem(parent)
            if len(x) == 0:
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                self.options.append(child)
            else:
                child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            child.setText(0, x.tag)
            child.setCheckState(0, Qt.Unchecked)
            if len(x) > 0:
                self.create_sub_tree(x, child)


class Deserializer(InputNode):
    def __init__(self, scene):
        super().__init__(scene, title="Object Loader")

    def setupUi(self):
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(398, 167)
        self.buttonBox = QDialogButtonBox(self.dialog)
        self.buttonBox.setGeometry(QRect(30, 120, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QWidget(self.dialog)
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

        self.dialog.setWindowTitle("Deserializer")
        self.label.setText("Select Directory")
        self.pushButton.setText("Select")
        self.label_2.setText("Text file will be saved to the directory you select.")

        self.buttonBox.accepted.connect(self.save_object)
        self.buttonBox.rejected.connect(self.dialog.reject)
        self.pushButton.clicked.connect(self.select_directory)
        QMetaObject.connectSlotsByName(self.dialog)

    def return_file(self):
        self.dialog.accept()
        print(type(self.output_object))
        if isinstance(self.output_object, dict):
            self.is_finished = True
            print("completed")
            self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
            # order the nodes
            self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
            # feed the next node
            self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)
        else:
            self.is_finished = False
            print("not completed")

    @property
    def output(self):
        return self.output_object

    def select_directory(self):
        directory, _ = QFileDialog.getOpenFileName(QMainWindow(), "Save as", QDir.homePath(), "All Files (*.*)",
                                                        options=QFileDialog.DontResolveSymlinks |
                                                                QFileDialog.DontUseNativeDialog)
        self.lineEdit.setText(directory)

    def save_object(self):
        with open(self.lineEdit.text(), "rb") as f:
            self.output_object = pickle.load(f)
        print("Object loading completed")
        self.return_file()
