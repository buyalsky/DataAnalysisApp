import os
import sys

import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

sys.path.append(os.path.abspath(os.path.join("..")))
from node import InputOutputNode


class AttributeRemover(InputOutputNode):
    def __init__(self, scene):
        super().__init__(scene, title="Attribute Remover", title_height=40)
        self.df = None
        self.node_type = "filter.attribute"

    def setup_ui(self, dialog):
        dialog.resize(377, 357)
        self.gridLayout = QGridLayout(dialog)
        self.horizontalLayout = QHBoxLayout()
        self.push_button = QPushButton(dialog)
        self.horizontalLayout.addWidget(self.push_button)
        self.push_button2 = QPushButton(dialog)
        self.horizontalLayout.addWidget(self.push_button2)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.scroll_area = QScrollArea(dialog)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 357, 279))
        self.verticalLayout = QVBoxLayout(self.scroll_area_widget_contents)
        self.check_boxes = []
        data_types = dict(self.df.dtypes)
        for i in range(len(self.df.columns)):
            c = QCheckBox(self.scroll_area_widget_contents)
            c.setText("{} ({})".format(self.df.columns[i], data_types[self.df.columns[i]]))
            self.check_boxes.append(c)
            self.verticalLayout.addWidget(c)

        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.gridLayout.addWidget(self.scroll_area, 1, 0, 1, 1)
        self.label = QLabel(dialog)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        dialog.setWindowTitle("Attribute Remover")
        self.push_button.setText("Apply")
        self.push_button.clicked.connect(self.remove_selected_columns)
        self.push_button2.setText("Cancel")
        self.label.setText("Select the attributes that you want to remove")

        QMetaObject.connectSlotsByName(dialog)

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
        self.return_file()


class NaiveBayesClassify(InputOutputNode):
    dialog = None
    button_box = None
    layout_widget = None
    horizontal_layout = None
    vertical_layout = None
    label_2 = None
    combo_box = None
    label_3 = None
    vertical_layout_2 = None
    line_edit_2 = None

    def __init__(self, scene):
        super().__init__(scene, title="Naive Bayes Classify", title_height=40)
        self.node_type = "supervised.naivebayes"

    def setup_ui(self, dialog):
        dialog.resize(450, 155)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(size_policy)
        self.button_box = QDialogButtonBox(dialog)
        self.button_box.setGeometry(QRect(100, 110, 341, 32))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.layout_widget = QWidget(dialog)
        self.layout_widget.setGeometry(QRect(20, 30, 401, 71))
        self.horizontal_layout = QHBoxLayout(self.layout_widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout = QVBoxLayout()
        self.label_2 = QLabel(self.layout_widget)
        self.vertical_layout.addWidget(self.label_2)
        self.label_3 = QLabel(self.layout_widget)
        self.vertical_layout.addWidget(self.label_3)
        self.horizontal_layout.addLayout(self.vertical_layout)
        self.vertical_layout_2 = QVBoxLayout()
        self.combo_box = QComboBox(self.layout_widget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.combo_box.sizePolicy().hasHeightForWidth())
        self.combo_box.setSizePolicy(size_policy)
        self.vertical_layout_2.addWidget(self.combo_box)
        self.line_edit_2 = QLineEdit(self.layout_widget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.line_edit_2.sizePolicy().hasHeightForWidth())
        self.line_edit_2.setSizePolicy(size_policy)
        self.vertical_layout_2.addWidget(self.line_edit_2)
        self.horizontal_layout.addLayout(self.vertical_layout_2)

        _translate = QCoreApplication.translate
        dialog.setWindowTitle("Naive Bayes Classify")
        self.label_2.setText("Target selection")
        self.label_3.setText("Test size percentage")

        for i in range(len(self.df.columns)):
            self.combo_box.addItem(str(self.df.columns[i]))

        self.button_box.accepted.connect(self.apply_naive_bayes_classify)
        self.button_box.rejected.connect(dialog.reject)
        QMetaObject.connectSlotsByName(dialog)

    def apply_naive_bayes_classify(self):
        self.dialog.accept()
        print("apply naive bayes classify")
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.naive_bayes import GaussianNB
            from sklearn.model_selection import train_test_split

            X_train, self.X_test, y_train, self.y_test = train_test_split(self.X, self.y, test_size=int(self.line_edit_2.text()) / 100, random_state=1, stratify=self.y)

            self.model = GaussianNB()
            self.model.fit(X_train, y_train)
            print(self.model.score(self.X_test, self.y_test))
        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.is_finished = True
            print("completed")
            self.return_file()

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.combo_box.currentText()])
        self.y = self.df[self.combo_box.currentText()].values

    @property
    def output(self):
        # TODO: return target selection
        data = {"model": self.model, "data_frame": self.df, "test_data": (self.X_test, self.y_test)}
        return data


class Knn(InputOutputNode):
    button_box = None
    widget = None
    horizontal_layout = None
    vertical_layout = None
    vertical_layout2 = None
    label = None
    label2 = None
    label3 = None
    line_edit = None
    line_edit2 = None

    def __init__(self, scene):
        super().__init__(scene, title="Knn")
        self.df = None
        self.node_type = "supervised.knn"

    def setup_ui(self, dialog):
        dialog.setObjectName("Dialog")
        dialog.resize(451, 205)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        self.button_box = QDialogButtonBox(dialog)
        self.button_box.setGeometry(QRect(100, 150, 341, 32))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setObjectName("buttonBox")
        self.widget = QWidget(dialog)
        self.widget.setGeometry(QRect(20, 30, 401, 111))
        self.widget.setObjectName("widget")
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setObjectName("horizontalLayout")
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName("verticalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.vertical_layout.addWidget(self.label)
        self.label2 = QLabel(self.widget)
        self.label2.setObjectName("label_2")
        self.vertical_layout.addWidget(self.label2)
        self.label3 = QLabel(self.widget)
        self.label3.setObjectName("label_3")
        self.vertical_layout.addWidget(self.label3)
        self.horizontal_layout.addLayout(self.vertical_layout)
        self.vertical_layout2 = QVBoxLayout()
        self.vertical_layout2.setObjectName("verticalLayout_2")
        self.line_edit = QLineEdit(self.widget)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_edit.sizePolicy().hasHeightForWidth())
        self.line_edit.setSizePolicy(sizePolicy)
        self.line_edit.setObjectName("lineEdit")
        self.vertical_layout2.addWidget(self.line_edit)
        self.comboBox = QComboBox(self.widget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.vertical_layout2.addWidget(self.comboBox)
        self.line_edit2 = QLineEdit(self.widget)
        self.line_edit2.setValidator(QIntValidator(0, 100, self.line_edit2))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_edit2.sizePolicy().hasHeightForWidth())
        self.line_edit2.setSizePolicy(sizePolicy)
        self.vertical_layout2.addWidget(self.line_edit2)
        self.horizontal_layout.addLayout(self.vertical_layout2)

        _translate = QCoreApplication.translate
        dialog.setWindowTitle("Dialog")
        self.label.setText("Number of neighbors")
        self.label2.setText("Target selection")
        self.label3.setText("Test size percentage")
        for i in range(len(self.df.columns)):
            self.comboBox.addItem(str(self.df.columns[i]))

        self.button_box.accepted.connect(self.apply_knn_classify)
        self.button_box.rejected.connect(dialog.reject)
        QMetaObject.connectSlotsByName(dialog)

    def apply_knn_classify(self):
        self.dialog.accept()
        print("apply knn classify")
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.neighbors import KNeighborsClassifier
            from sklearn.model_selection import train_test_split

            X_train, self.X_test, y_train, self.y_test = train_test_split(self.X, self.y, test_size=int(self.line_edit2.text()) / 100, random_state=1, stratify=self.y)

            self.model = KNeighborsClassifier(n_neighbors=int(self.line_edit.text()))
            self.model.fit(X_train, y_train)
            print(self.model.score(self.X_test, self.y_test))
        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.is_finished = True
            print("completed")
            self.return_file()

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.comboBox.currentText()])
        self.y = self.df[self.comboBox.currentText()].values

    @property
    def output(self):
        return {"model": self.model, "data_frame": self.df, "test_data": (self.X_test, self.y_test),
                "target_label": self.comboBox.currentText()}


class SVM(InputOutputNode):
    def __init__(self, scene):
        super().__init__(scene, title="SVM")
        self.node_type = "supervised.svm"

    def setup_ui(self, dialog):
        dialog.resize(450, 155)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(size_policy)
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setGeometry(QRect(100, 110, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.layoutWidget = QWidget(dialog)
        self.layoutWidget.setGeometry(QRect(20, 30, 401, 71))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.label_2 = QLabel(self.layoutWidget)
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.comboBox = QComboBox(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(size_policy)
        self.verticalLayout_2.addWidget(self.comboBox)
        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(size_policy)
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        dialog.setWindowTitle("Support Vector Machine")
        self.label_2.setText("Target selection")
        self.label_3.setText("Test size percentage")
        for i in range(len(self.df.columns)):
            self.comboBox.addItem(str(self.df.columns[i]))

        self.buttonBox.accepted.connect(self.apply_svm_classify)
        self.buttonBox.rejected.connect(dialog.reject)
        QMetaObject.connectSlotsByName(dialog)

    def apply_svm_classify(self):
        self.dialog.accept()
        print("apply svm classify")
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.svm import SVC
            from sklearn.model_selection import train_test_split

            X_train, self.X_test, y_train, self.y_test = train_test_split(self.X, self.y, test_size=int(self.lineEdit_2.text())/100, random_state=1, stratify=self.y)

            self.model = SVC(random_state=1)
            self.model.fit(X_train, y_train)
            print(self.model.score(self.X_test, self.y_test))
        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.is_finished = True
            print("completed")
            self.return_file()

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.comboBox.currentText()])
        self.y = self.df[self.comboBox.currentText()].values

    @property
    def output(self):
        return self.model, self.X_test, self.y_test


class DecisionTree(InputOutputNode):
    buttonBox = None
    layoutWidget = None
    horizontal_layout = None
    vertical_layout = None
    vertical_layout2 = None
    label2 = None
    label3 = None
    combo_box = None
    line_edit2 = None

    def __init__(self, scene):
        super().__init__(scene, title="Decision Tree")
        self.node_type = "supervised.decisiontree"

    def setup_ui(self, dialog):
        dialog.resize(450, 155)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(size_policy)
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setGeometry(QRect(100, 110, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.layoutWidget = QWidget(dialog)
        self.layoutWidget.setGeometry(QRect(20, 30, 401, 71))
        self.horizontal_layout = QHBoxLayout(self.layoutWidget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout = QVBoxLayout()
        self.label2 = QLabel(self.layoutWidget)
        self.vertical_layout.addWidget(self.label2)
        self.label3 = QLabel(self.layoutWidget)
        self.vertical_layout.addWidget(self.label3)
        self.horizontal_layout.addLayout(self.vertical_layout)
        self.vertical_layout2 = QVBoxLayout()
        self.combo_box = QComboBox(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.combo_box.sizePolicy().hasHeightForWidth())
        self.combo_box.setSizePolicy(size_policy)
        self.vertical_layout2.addWidget(self.combo_box)
        self.line_edit2 = QLineEdit(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.line_edit2.sizePolicy().hasHeightForWidth())
        self.line_edit2.setSizePolicy(size_policy)
        self.vertical_layout2.addWidget(self.line_edit2)
        self.horizontal_layout.addLayout(self.vertical_layout2)

        _translate = QCoreApplication.translate
        dialog.setWindowTitle("Dialog")
        self.label2.setText("Target selection")
        self.label3.setText("Test size percentage")
        for i in range(len(self.df.columns)):
            self.combo_box.addItem(str(self.df.columns[i]))
        self.buttonBox.accepted.connect(self.apply_decision_tree_classify)
        self.buttonBox.rejected.connect(dialog.reject)
        QMetaObject.connectSlotsByName(dialog)

    def apply_decision_tree_classify(self):
        self.dialog.accept()
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.tree import DecisionTreeClassifier
            from sklearn.model_selection import train_test_split

            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,
                                                                test_size=int(self.line_edit2.text()) / 100,
                                                                random_state=1,
                                                                stratify=self.y)

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
            self.return_file()

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.combo_box.currentText()])
        self.y = self.df[self.combo_box.currentText()].values


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AttributeRemover()

    sys.exit(app.exec_())
