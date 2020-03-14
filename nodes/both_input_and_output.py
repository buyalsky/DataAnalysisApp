import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd

sys.path.append(os.path.abspath(os.path.join("..")))
from node import Node


class AttributeRemover(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Attribute Remover", inputs=1, outputs=1)
        self.df = None

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
        print("ar" + self.df.columns)
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
        for checkbox in self.check_boxes:
            if checkbox.isChecked():
                dropped_columns.append(checkbox.text())
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
        # self.graphic_node.scene().scene.parent_widget.parent_window.feed_next_node(self)

    def feed(self, df):
        self.df = df


class NaiveBayesClassify(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Naive Bayes Classify", inputs=1, outputs=1)


class Knn(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Knn", inputs=1, outputs=1)


class SVM(Node):
    def __init__(self, scene):
        super().__init__(scene, title="SVM", inputs=1, outputs=1)


class DecisionTree(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Decision Tree", inputs=1, outputs=1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AttributeRemover()

    sys.exit(app.exec_())
