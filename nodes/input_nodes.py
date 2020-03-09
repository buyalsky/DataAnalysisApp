import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
sys.path.append(os.path.abspath(os.path.join("..")))
from node import Node


class CsvLoader(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Csv Loader", inputs=0, outputs=1)
        self.is_first = True

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
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Dosya seç"))
        self.pushButton.setText(_translate("Dialog", "Seç"))
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
        options = ["," if self.comboBox.currentText() == "Virgül" else ";",
                   "," if self.comboBox_2.currentText() == "Virgül" else ".",
                   "," if self.comboBox_3.currentText() == "Virgül" else ".", self.comboBox_4.currentText()]
        self.df = pd.read_csv(self.fname[0], sep=options[0], thousands=options[1],
                              decimal=options[2], encoding=options[3])
        print(self.df.head(10))

    def return_file(self):
        self.dialog.accept()
        if isinstance(self.df, pd.core.frame.DataFrame):
            self.is_finished = True
            print("completed")
        else:
            print("not completed")


    def evaluate(self):
        pass


class ExcelLoader(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Excel Loader", inputs=0, outputs=1)
        self.is_first = True

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
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Dosya seç"))
        self.pushButton.setText(_translate("Dialog", "Seç"))
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
        options = ["," if self.comboBox.currentText() == "Virgül" else ";",
                   "," if self.comboBox_2.currentText() == "Virgül" else ".",
                   "," if self.comboBox_3.currentText() == "Virgül" else ".", self.comboBox_4.currentText()]
        self.df = pd.read_csv(self.fname[0], sep=options[0], thousands=options[1],
                              decimal=options[2], encoding=options[3])
        print(self.df.head(10))

    def return_file(self):
        self.dialog.accept()
        if isinstance(self.df, pd.core.frame.DataFrame):
            self.is_finished = True
            print("completed")
        else:
            print("not completed")

    def evaluate(self):
        pass
