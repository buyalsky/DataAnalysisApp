import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
sys.path.append(os.path.abspath(os.path.join("..")))
from node import Node
import xml.etree.ElementTree as ET


class CsvLoader(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Csv Loader", inputs=0, outputs=1)
        self.is_first = True
        self.node_type = "loader.csv"

    def run(self):
        print("calusuyor")
        self.df = None
        self.dialog = QDialog()
        self.setupUI(self.dialog)
        self.dialog.show()


    def setupUI(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(372, 324)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(10, 280, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QWidget(Dialog)
        self.widget.setGeometry(QRect(20, 30, 331, 41))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
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
        self.widget1 = QWidget(Dialog)
        self.widget1.setGeometry(QRect(20, 80, 331, 161))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QLabel(self.widget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox = QComboBox(self.widget1)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QLabel(self.widget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.comboBox_2 = QComboBox(self.widget1)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QLabel(self.widget1)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.comboBox_3 = QComboBox(self.widget1)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QLabel(self.widget1)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.comboBox_4 = QComboBox(self.widget1)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.horizontalLayout_5.addWidget(self.comboBox_4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.return_file)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.pushButton.clicked.connect(self.file_select_clicked)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Select file"))
        self.pushButton.setText(_translate("Dialog", "Select"))
        self.label_2.setText(_translate("Dialog", "Ayraç"))
        self.comboBox.setItemText(0, _translate("Dialog", "Virgül"))
        self.comboBox.setItemText(1, _translate("Dialog", "Noktalı Virgül"))
        self.label_3.setText(_translate("Dialog", "Bindelik ayracı"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "Virgül"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "Nokta"))
        self.label_4.setText(_translate("Dialog", "Ondalık ayıracı"))
        self.comboBox_3.setItemText(0, _translate("Dialog", "Nokta"))
        self.comboBox_3.setItemText(1, _translate("Dialog", "Virgül"))
        self.label_5.setText(_translate("Dialog", "Encoding"))
        self.comboBox_4.setItemText(0, _translate("Dialog", "utf-8"))
        self.comboBox_4.setItemText(1, _translate("Dialog", "utf-16"))
        self.comboBox_4.setItemText(2, _translate("Dialog", "utf-32"))

    def file_select_clicked(self):
        print("clicked")
        self.fname = QFileDialog.getOpenFileName(QWidget(), "Open File", "C:/", "Csv (*.csv)")
        print("clicked")
        if not self.fname[0]:
            return
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    @property
    def output(self):
        return self.df

    def return_file(self):
        self.dialog.accept()
        options = ["," if self.comboBox.currentText() == "Virgül" else ";",
                   "," if self.comboBox_2.currentText() == "Virgül" else ".",
                   "," if self.comboBox_3.currentText() == "Virgül" else ".", self.comboBox_4.currentText()]
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

    def evaluate(self):
        pass


class ExcelLoader(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Excel Loader", inputs=0, outputs=1)
        self.is_first = True
        self.node_type = "loader.excel"

    def run(self):
        print("calusuyor")
        self.df = None
        self.dialog = QDialog()
        self.setupUI(self.dialog)
        self.dialog.show()

    def setupUI(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(372, 134)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(10, 80, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QWidget(Dialog)
        self.widget.setGeometry(QRect(20, 30, 331, 41))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
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

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.return_file)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.pushButton.clicked.connect(self.file_select_clicked)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Select file"))
        self.pushButton.setText(_translate("Dialog", "Select"))


    def file_select_clicked(self):
        print("clicked")
        self.fname = QFileDialog.getOpenFileName(QWidget(), "Open File", "C:/", "Excel (*.xls *.xlsl)")
        print("clicked")
        if not self.fname[0]:
            return

        self.df = pd.read_excel(self.fname[0])
        print(self.df.head(10))

    def return_file(self):
        self.dialog.accept()
        print(type(self.df))
        if isinstance(self.df, pd.core.frame.DataFrame):
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
        return self.df

    def evaluate(self):
        pass


class XmlLoader(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Xml Loader", inputs=0, outputs=1)
        self.is_first = True
        self.node_type = "loader.xml"

    def run(self):
        print("calusuyor")
        self.df = None
        self.dialog = QDialog()
        self.setupUI(self.dialog)
        self.dialog.show()

    def setupUI(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(461, 509)
        self.widget = QWidget(Dialog)
        self.widget.setGeometry(QRect(30, 40, 401, 421))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
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
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tree_widget = QTreeWidget(self.widget)
        self.tree_widget.setObjectName("treeWidget")

        self.verticalLayout.addWidget(self.tree_widget)
        self.buttonBox = QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.print_current)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.pushButton.clicked.connect(self.file_select_clicked)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Select File"))
        self.pushButton.setText(_translate("Dialog", "PushButton"))
        self.tree_widget.headerItem().setText(0, _translate("Dialog", "1"))

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

    def return_file(self):
        self.dialog.accept()
        print(type(self.df))
        print(self.df.dtypes)
        if isinstance(self.df, pd.core.frame.DataFrame):
            self.is_finished = True
            print("completed")
            self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
            # order the nodes
            self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
            # feed the next node
            self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)
        else:
            print("not completed")

    @property
    def output(self):
        return self.df

    def evaluate(self):
        pass

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

