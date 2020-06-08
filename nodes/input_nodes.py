import sys
import os
import pickle
import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd

sys.path.append(os.path.abspath(os.path.join("..")))
from node import InputNode


class CsvLoader(InputNode):
    button_box = None
    widget = None
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
        super().__init__(scene, title="Csv Loader", icon_name="icons/csv128.png")

    def setup_ui(self):
        self.dialog.resize(372, 324)
        self.button_box = QDialogButtonBox(self.dialog)
        self.button_box.setGeometry(QRect(10, 280, 341, 32))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        widget = QWidget(self.dialog)
        widget.setGeometry(QRect(20, 30, 331, 41))
        self.horizontal_layout = QHBoxLayout(widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(widget)
        self.horizontal_layout.addWidget(label)
        self.line_edit = QLineEdit(widget)
        self.horizontal_layout.addWidget(self.line_edit)
        self.push_button = QPushButton(widget)
        self.horizontal_layout.addWidget(self.push_button)
        self.widget1 = QWidget(self.dialog)
        self.widget1.setGeometry(QRect(20, 80, 331, 161))
        self.vertical_layout = QVBoxLayout(self.widget1)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout2 = QHBoxLayout()
        label2 = QLabel(self.widget1)
        self.horizontal_layout2.addWidget(label2)
        self.combo_box = QComboBox(self.widget1)
        self.horizontal_layout2.addWidget(self.combo_box)
        self.vertical_layout.addLayout(self.horizontal_layout2)
        self.horizontal_layout3 = QHBoxLayout()
        label3 = QLabel(self.widget1)
        self.horizontal_layout3.addWidget(label3)
        self.combo_box2 = QComboBox(self.widget1)
        self.horizontal_layout3.addWidget(self.combo_box2)
        self.vertical_layout.addLayout(self.horizontal_layout3)
        self.horizontal_layout4 = QHBoxLayout()
        label4 = QLabel(self.widget1)
        self.horizontal_layout4.addWidget(label4)
        self.combo_box3 = QComboBox(self.widget1)
        self.horizontal_layout4.addWidget(self.combo_box3)
        self.vertical_layout.addLayout(self.horizontal_layout4)
        self.horizontal_layout5 = QHBoxLayout()
        label5 = QLabel(self.widget1)
        self.horizontal_layout5.addWidget(label5)
        self.combo_box4 = QComboBox(self.widget1)
        self.horizontal_layout5.addWidget(self.combo_box4)
        self.vertical_layout.addLayout(self.horizontal_layout5)
        self.dialog.setWindowTitle("Csv Loader")
        label.setText("Select file")
        self.push_button.setText("Select")
        label2.setText("Separator")
        self.combo_box.addItems(["Comma", "Semicolon"])
        label3.setText("Thousands Separator")
        self.combo_box2.addItems(["Comma", "Dot"])
        label4.setText("Decimal Point Char.")
        self.combo_box3.addItems(["Dot", "Comma"])
        label5.setText("Encoding")
        self.combo_box4.addItems(["utf-8", "utf-16", "utf-32"])

        self.button_box.accepted.connect(self.return_file)
        self.button_box.rejected.connect(self.dialog.reject)
        self.push_button.clicked.connect(self.file_select_clicked)
        self.line_edit.textChanged.connect(lambda text: self.button_box.button(QDialogButtonBox.Ok)
                                           .setEnabled(bool(text)))
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        QMetaObject.connectSlotsByName(self.dialog)

    def file_select_clicked(self):
        file_name = QFileDialog.getOpenFileName(QWidget(), "Open File", "C:/", "Csv (*.csv)")[0]
        self.line_edit.setText(file_name)
        if not file_name:
            return
        else:
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)

    def return_file(self):
        options = ["," if self.combo_box.currentText() == "Comma" else ";",
                   "," if self.combo_box2.currentText() == "Comma" else ".",
                   "," if self.combo_box3.currentText() == "Comma" else ".", self.combo_box4.currentText()]
        try:
            self.df = pd.read_csv(self.line_edit.text(), sep=options[0], thousands=options[1],
                              decimal=options[2], encoding=options[3])
        except Exception as err:
            QMessageBox.warning(self.dialog, "Error happened while opening the file", str(err))
            return

        self.dialog.accept()

        for column, value in self.df.iteritems():
            if len(set(value)) < 5:
                print("{} can be categorical".format(column))
                self.df[column] = self.df[column].astype("category")

        if isinstance(self.df, pd.core.frame.DataFrame):
            self.is_finished = True
            self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
            # order the nodes
            self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
            # feed the next node
            self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)

        else:
            self.is_finished = False


class ExcelLoader(InputNode):
    button_box = None
    widget = None
    horizontal_layout = None
    label = None
    push_button = None

    def __init__(self, scene):
        super().__init__(scene, title="Excel Loader", icon_name="icons/excel128.png")
        self.node_type = "loader.excel"

    def setup_ui(self):
        self.dialog.resize(372, 134)
        self.button_box = QDialogButtonBox(self.dialog)
        self.button_box.setGeometry(QRect(10, 80, 341, 32))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.widget = QWidget(self.dialog)
        self.widget.setGeometry(QRect(20, 30, 331, 41))
        self.widget.setObjectName("widget")
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.horizontal_layout.addWidget(self.label)
        self.line_edit = QLineEdit(self.widget)
        self.horizontal_layout.addWidget(self.line_edit)
        self.push_button = QPushButton(self.widget)
        self.horizontal_layout.addWidget(self.push_button)

        _translate = QCoreApplication.translate
        self.dialog.setWindowTitle("Dialog")
        self.label.setText("Select file")
        self.push_button.setText("Select")

        self.button_box.accepted.connect(self.load_file)
        self.button_box.rejected.connect(self.dialog.reject)
        self.push_button.clicked.connect(self.file_select_clicked)
        self.line_edit.textChanged.connect(lambda text: self.button_box.button(QDialogButtonBox.Ok)
                                           .setEnabled(bool(text)))
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        QMetaObject.connectSlotsByName(self.dialog)

    def file_select_clicked(self):
        self.line_edit.setText(QFileDialog.getOpenFileName(QWidget(), "Open File", "C:/", "Excel (*.xls *.xlsl)")[0])

    def load_file(self):
        try:
            self.df = pd.read_excel(self.line_edit.text())
        except Exception as err:
            QMessageBox.warning(self.dialog, "Error happened while opening the file", str(err))
            return
        self.return_file()


class XmlLoader(InputNode):
    widget = None
    vertical_layout = None
    vertical_layout2 = None
    horizontal_layout = None
    label = None
    push_button = None
    tree_widget = None
    button_box = None

    def __init__(self, scene):
        super().__init__(scene, title="Xml Loader", icon_name="icons/xml128.png")
        self.node_type = "loader.xml"

    def setup_ui(self):
        self.dialog.resize(461, 509)
        self.widget = QWidget(self.dialog)
        self.widget.setGeometry(QRect(30, 40, 401, 421))
        self.vertical_layout2 = QVBoxLayout(self.widget)
        self.vertical_layout2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout = QHBoxLayout()
        self.label = QLabel(self.widget)
        self.horizontal_layout.addWidget(self.label)
        self.line_edit = QLineEdit(self.widget)
        self.line_edit.setReadOnly(True)
        self.horizontal_layout.addWidget(self.line_edit)
        self.push_button = QPushButton(self.widget)
        self.horizontal_layout.addWidget(self.push_button)
        self.vertical_layout2.addLayout(self.horizontal_layout)
        self.vertical_layout = QVBoxLayout()
        self.tree_widget = QTreeWidget(self.widget)

        self.vertical_layout.addWidget(self.tree_widget)
        self.button_box = QDialogButtonBox(self.widget)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.vertical_layout.addWidget(self.button_box)
        self.vertical_layout2.addLayout(self.vertical_layout)
        self.dialog.setWindowTitle("Xml Loader")
        self.label.setText("Select File")
        self.push_button.setText("Select")
        self.tree_widget.headerItem().setText(0, "")

        self.button_box.accepted.connect(self.convert_to_data_frame)
        self.button_box.rejected.connect(self.dialog.reject)
        self.push_button.clicked.connect(self.file_select_clicked)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        QMetaObject.connectSlotsByName(self.dialog)

    def create_dataframe(self):
        self.data = {}
        for option in self.selected_options:
            self.data[option.text(0)] = []
        print(self.data)

        tree = ET.parse(self.line_edit.text())
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

    def convert_to_data_frame(self):
        self.selected_options = []
        for option in self.options:
            if option.checkState(0) == Qt.Checked:
                self.selected_options.append(option)
        if self.check_validity():
            self.create_dataframe()
            self.return_file()
        else:
            QMessageBox.warning(self.dialog, "Error happened", "Selected attributes must be within same root!")

    def check_validity(self):
        self.top_parent_item = self.top_parent(self.selected_options[0])
        for option in self.selected_options:
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
        self.line_edit.setText(QFileDialog.getOpenFileName(QWidget(), "Open File", "C:/", "Xml files (*.xml)")[0])
        self.open_xml_file()

    def open_xml_file(self):
        try:
            tree = ET.parse(self.line_edit.text())
            root = tree.getroot()
        except Exception as err:
            QMessageBox.warning(self.dialog, "Error happened while parsing xml file", str(err))
            return
        # child = root[0]
        self.options = []
        self.create_tree(root, self.tree_widget)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)

    def create_tree(self, root, tree_widget):
        a = set([child.tag for child in root])
        print(a)

        for child in root:
            if not a:
                break
            if child.tag in a:
                parent = QTreeWidgetItem(tree_widget)
                parent.setText(0, child.tag)
                parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                self.create_sub_tree(child, parent)
                a.remove(child.tag)


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
    output_object = None

    def __init__(self, scene):
        super().__init__(scene, title="Deserializer", icon_name="icons/serializer128.png")

    def setup_ui(self):
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(405, 127)
        self.buttonBox = QDialogButtonBox(self.dialog)
        self.buttonBox.setGeometry(QRect(30, 80, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QWidget(self.dialog)
        self.widget.setGeometry(QRect(10, 10, 381, 81))
        self.widget.setObjectName("widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        label = QLabel(self.widget)
        self.horizontalLayout.addWidget(label)
        self.line_edit = QLineEdit(self.widget)
        self.line_edit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.line_edit)
        self.pushButton = QPushButton(self.widget)
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.dialog.setWindowTitle("Deserializer")
        label.setText("Select Directory")
        self.pushButton.setText("Select")

        self.buttonBox.accepted.connect(self.load_object)
        self.buttonBox.rejected.connect(self.dialog.reject)
        self.pushButton.clicked.connect(self.select_directory)
        QMetaObject.connectSlotsByName(self.dialog)

    def return_file(self):
        self.dialog.accept()
        if isinstance(self.output_object, dict):
            self.is_finished = True
            self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
            # order the nodes
            self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
            # feed the next node
            self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)
        else:
            self.is_finished = False
            QMessageBox.warning(self.dialog, "Incompatible object type",
                                "The loaded object whose type must be Python Dictionary is not compatible, "
                                "found {} instead.".format(type(self.output_object)))

    @property
    def output(self):
        return self.output_object

    def select_directory(self):
        directory, _ = QFileDialog.getOpenFileName(QMainWindow(), "Save as", QDir.homePath(), "All Files (*.*)",
                                                   options=QFileDialog.DontResolveSymlinks | QFileDialog.
                                                   DontUseNativeDialog)
        self.line_edit.setText(directory)

    def load_object(self):
        try:
            fd = open(self.line_edit.text(), "rb")
        except FileNotFoundError as err:
            QMessageBox.warning(
                self.dialog,
                "Error happened",
                str(err)
            )
            return
        self.output_object = pickle.load(fd)
        fd.close()
        self.return_file()

