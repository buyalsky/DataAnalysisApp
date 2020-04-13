import os
import sys

import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

sys.path.append(os.path.abspath(os.path.join("..")))
from node import Node


class AttributeRemover(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Attribute Remover", inputs=1, outputs=1)
        self.df = None
        self.node_type = "filter.attribute"
        # self.df = pd.read_csv("C:/Users/Burak/OneDrive/Masaüstü/Python/Demo Machine Learning/column_2C_weka.csv")

    def run(self):
        if not isinstance(self.df, pd.core.frame.DataFrame):
            QMessageBox.about(
                self.scene.parent_widget,
                "Warning!",
                "You need to complete preceding nodes first."
            )
            return
        self.dialog = QDialog()
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setupUI(self.dialog)
        print(self.df.columns)
        self.dialog.show()

    def setupUI(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QRect(80, 20, 500, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.check_boxes = []
        for i in range(len(self.df.columns)):
            c = QCheckBox(self.verticalLayoutWidget)
            self.check_boxes.append(c)
            self.verticalLayout.addWidget(c)

        self.widget = QWidget(Dialog)
        self.widget.setGeometry(QRect(110, 260, 158, 26))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_apply = QPushButton(self.widget)
        self.pushButton_apply.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton_apply)
        self.pushButton_cancel = QPushButton(self.widget)
        self.pushButton_cancel.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.pushButton_apply.clicked.connect(self.remove_selected_columns)

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        data_types = dict(self.df.dtypes)
        for i, check_box in enumerate(self.check_boxes):
            check_box.setText(_translate("Dialog", "{} ({})".format(self.df.columns[i], data_types[self.df.columns[i]])))
        self.pushButton_apply.setText(_translate("Dialog", "Uygula"))
        self.pushButton_cancel.setText(_translate("Dialog", "İptal"))

    def remove_selected_columns(self):
        self.dialog.accept()
        dropped_columns = []
        for i, checkbox in enumerate(self.check_boxes):
            if checkbox.isChecked():
                dropped_columns.append(str(self.df.columns[i]))
                print(checkbox.text())
        if dropped_columns:
            self.df.drop(dropped_columns, axis=1, inplace=True)
        print(self.df.head())

        self.is_finished = True
        print("completed")
        self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
        # order the nodes
        self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
        # feed the next node
        self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)

    @property
    def output(self):
        return self.df

    def feed(self, df):
        self.df = df


class NaiveBayesClassify(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Naive Bayes Classify", inputs=1, outputs=1)
        self.node_type = "supervised.naivebayes"

    def run(self):
        if not isinstance(self.df, pd.core.frame.DataFrame):
            QMessageBox.about(
                self.scene.parent_widget,
                "Warning!",
                "You need to complete preceding nodes first."
            )
            return
        self.dialog = QDialog()
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setupUi(self.dialog)
        print(self.df.columns)
        self.dialog.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 155)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(100, 110, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setGeometry(QRect(20, 30, 401, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.comboBox = QComboBox(self.layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_2.addWidget(self.comboBox)
        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.apply_naive_bayes_classify)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Target selection"))
        self.label_3.setText(_translate("Dialog", "Test size percentage"))
        for i in range(len(self.df.columns)):
            self.comboBox.addItem(str(self.df.columns[i]))

    def apply_naive_bayes_classify(self):
        self.dialog.accept()
        print("apply naive bayes classify")
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.naive_bayes import GaussianNB
            from sklearn.model_selection import train_test_split

            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=int(self.lineEdit_2.text())/100, random_state=1, stratify=self.y)

            nb = GaussianNB()
            nb.fit(X_train, y_train)
            print(nb.score(X_test, y_test))
        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.is_finished = True
            print("completed")
            self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
            # order the nodes
            self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
            # feed the next node
            #self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.comboBox.currentText()])
        self.y = self.df[self.comboBox.currentText()].values

    def feed(self, df):
        self.df = df


class Knn(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Knn", inputs=1, outputs=1)
        self.df = None
        self.node_type = "supervised.knn"

    def run(self):
        if not isinstance(self.df, pd.core.frame.DataFrame):
            QMessageBox.about(
                self.scene.parent_widget,
                "Warning!",
                "You need to complete preceding nodes first."
            )
            return
        self.dialog = QDialog()
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setupUi(self.dialog)
        print(self.df.columns)
        self.dialog.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(451, 205)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(100, 150, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QWidget(Dialog)
        self.widget.setGeometry(QRect(20, 30, 401, 111))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QLineEdit(self.widget)
        #self.lineEdit.setValidator()
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.comboBox = QComboBox(self.widget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")

        self.verticalLayout_2.addWidget(self.comboBox)
        self.lineEdit_2 = QLineEdit(self.widget)
        self.lineEdit_2.setValidator(QIntValidator(0, 100, self.lineEdit_2))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.apply_knn_classify)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Number of neighbors"))
        self.label_2.setText(_translate("Dialog", "Target selection"))
        self.label_3.setText(_translate("Dialog", "Test size percentage"))
        for i in range(len(self.df.columns)):
            self.comboBox.addItem(str(self.df.columns[i]))

    def apply_knn_classify(self):
        self.dialog.accept()
        print("apply knn classify")
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.neighbors import KNeighborsClassifier
            from sklearn.model_selection import train_test_split

            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=int(self.lineEdit_2.text())/100, random_state=1, stratify=self.y)

            knn = KNeighborsClassifier(n_neighbors=int(self.lineEdit.text()))
            knn.fit(X_train, y_train)
            print(knn.score(X_test, y_test))
        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.is_finished = True
            print("completed")
            self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
            # order the nodes
            self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
            # feed the next node
            #self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.comboBox.currentText()])
        self.y = self.df[self.comboBox.currentText()].values

    def feed(self, df):
        self.df = df


class SVM(Node):
    def __init__(self, scene):
        super().__init__(scene, title="SVM", inputs=1, outputs=1)
        self.node_type = "supervised.svm"

    def run(self):
        if not isinstance(self.df, pd.core.frame.DataFrame):
            QMessageBox.about(
                self.scene.parent_widget,
                "Warning!",
                "You need to complete preceding nodes first."
            )
            return
        self.dialog = QDialog()
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setupUi(self.dialog)
        print(self.df.columns)
        self.dialog.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 155)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(100, 110, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setGeometry(QRect(20, 30, 401, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.comboBox = QComboBox(self.layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_2.addWidget(self.comboBox)
        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.apply_svm_classify)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Target selection"))
        self.label_3.setText(_translate("Dialog", "Test size percentage"))
        for i in range(len(self.df.columns)):
            self.comboBox.addItem(str(self.df.columns[i]))

    def apply_svm_classify(self):
        self.dialog.accept()
        print("apply svm classify")
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.svm import SVC
            from sklearn.model_selection import train_test_split

            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=int(self.lineEdit_2.text())/100, random_state=1, stratify=self.y)

            svm = SVC(random_state=1)
            svm.fit(X_train, y_train)
            print(svm.score(X_test, y_test))
        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.is_finished = True
            print("completed")
            self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
            # order the nodes
            self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
            # feed the next node
            #self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.comboBox.currentText()])
        self.y = self.df[self.comboBox.currentText()].values

    def feed(self, df):
        self.df = df

class DecisionTree(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Decision Tree", inputs=1, outputs=1)
        self.node_type = "supervised.decisiontree"

    def run(self):
        if not isinstance(self.df, pd.core.frame.DataFrame):
            QMessageBox.about(
                self.scene.parent_widget,
                "Warning!",
                "You need to complete preceding nodes first."
            )
            return
        self.dialog = QDialog()
        self.dialog.setWindowFlags(Qt.WindowTitleHint)
        self.setupUi(self.dialog)
        print(self.df.columns)
        self.dialog.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 155)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(100, 110, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setGeometry(QRect(20, 30, 401, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.comboBox = QComboBox(self.layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_2.addWidget(self.comboBox)
        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.apply_decision_tree_classify)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Target selection"))
        self.label_3.setText(_translate("Dialog", "Test size percentage"))
        for i in range(len(self.df.columns)):
            self.comboBox.addItem(str(self.df.columns[i]))

    def apply_decision_tree_classify(self):
        self.dialog.accept()
        print("apply svm classify")
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.tree import DecisionTreeClassifier
            from sklearn.model_selection import train_test_split

            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=int(self.lineEdit_2.text())/100, random_state=1, stratify=self.y)

            dt = DecisionTreeClassifier()
            dt.fit(X_train, y_train)
            print(dt.score(X_test, y_test))
        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.is_finished = True
            print("completed")
            self.graphic_node.scene().scene.parent_widget.parent_window.change_statusbar_text()
            # order the nodes
            self.graphic_node.scene().scene.parent_widget.parent_window.order_path()
            # feed the next node
            #self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.comboBox.currentText()])
        self.y = self.df[self.comboBox.currentText()].values

    def feed(self, df):
        self.df = df




if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AttributeRemover()

    sys.exit(app.exec_())
