import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

sys.path.append(os.path.abspath(os.path.join("..")))
from node import InputOutputNode


class AttributeRemover(InputOutputNode):
    check_boxes = None
    modified_df = None

    # todo remove title height kwarg for all nodes
    def __init__(self, scene):
        super().__init__(scene, title="Attribute Remover", title_height=40)
        self.df = None
        self.node_type = "filter.attribute"

    def setup_ui(self):
        self.dialog.resize(377, 357)
        grid_layout = QGridLayout(self.dialog)
        horizontal_layout = QHBoxLayout()
        push_button = QPushButton(self.dialog)
        horizontal_layout.addWidget(push_button)
        push_button2 = QPushButton(self.dialog)
        horizontal_layout.addWidget(push_button2)
        grid_layout.addLayout(horizontal_layout, 2, 0, 1, 1)
        scroll_area = QScrollArea(self.dialog)
        scroll_area.setWidgetResizable(True)
        scroll_area_widget_contents = QWidget()
        scroll_area_widget_contents.setGeometry(QRect(0, 0, 357, 279))
        vertical_layout = QVBoxLayout(scroll_area_widget_contents)
        self.check_boxes = []
        data_types = dict(self.df.dtypes)
        for i in range(len(self.df.columns)):
            c = QCheckBox(scroll_area_widget_contents)
            c.setText("{} ({})".format(self.df.columns[i], data_types[self.df.columns[i]]))
            self.check_boxes.append(c)
            vertical_layout.addWidget(c)

        scroll_area.setWidget(scroll_area_widget_contents)
        grid_layout.addWidget(scroll_area, 1, 0, 1, 1)
        label = QLabel(self.dialog)
        grid_layout.addWidget(label, 0, 0, 1, 1)

        self.dialog.setWindowTitle("Attribute Remover")
        push_button.setText("Apply")
        push_button.clicked.connect(self.remove_selected_columns)
        push_button2.setText("Cancel")
        label.setText("Select the attributes that you want to remove")

        QMetaObject.connectSlotsByName(self.dialog)

    def remove_selected_columns(self):
        self.dialog.accept()
        dropped_columns = []
        for i, checkbox in enumerate(self.check_boxes):
            if checkbox.isChecked():
                dropped_columns.append(str(self.df.columns[i]))
                print(checkbox.text())
        if dropped_columns:
            self.modified_df = self.df.drop(dropped_columns, axis=1)
        print(self.df.head())

        self.is_finished = True
        print("completed")
        self.return_file()

    @property
    def output(self):
        return self.modified_df


class Filter(InputOutputNode):
    stacked_widget = None
    combo_box = None
    line_edits = None
    check_boxes = None
    modified_df = None

    def __init__(self, scene):
        super().__init__(scene, title="Filter")
        self.df = None

    def setup_ui(self):
        self.dialog.resize(512, 300)
        grid_layout = QGridLayout(self.dialog)
        vertical_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        label = QLabel(self.dialog)
        horizontal_layout.addWidget(label)
        self.combo_box = QComboBox(self.dialog)
        horizontal_layout.addWidget(self.combo_box)
        vertical_layout.addLayout(horizontal_layout)
        frame = QFrame(self.dialog)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)

        self.stacked_widget = QStackedWidget()
        scroll_areas = []
        scroll_areas_widget_contents = []
        scroll_areas_layouts = []
        self.line_edits = []
        self.check_boxes = []

        data_types = dict(self.df.dtypes)

        for i in range(len(self.df.columns)):
            if "int" in str(data_types[self.df.columns[i]]) or "float" in str(data_types[self.df.columns[i]]):
                scroll_area = QScrollArea(frame)
                scroll_area.setWidgetResizable(True)
                contents = QWidget()
                contents.setGeometry(QRect(0, 0, 399, 259))
                scroll_area.setWidget(contents)
                self.stacked_widget.addWidget(scroll_area)
                scroll_areas.append(scroll_area)
                scroll_areas_widget_contents.append(contents)
                vertical_layout = QVBoxLayout(contents)

                label_range_selection = QLabel(contents)
                label_range_selection.setText("Range Selection")
                vertical_layout.addWidget(label_range_selection)

                line = QFrame(contents)
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                vertical_layout.addWidget(line)

                font = QFont()
                font.setPointSize(10)
                horizontal_labels = QHBoxLayout()
                label_from = QLabel(contents)
                label_from.setFont(font)
                label_from.setAlignment(Qt.AlignCenter)
                label_from.setText("From")
                label_empty = QLabel(contents)
                label_empty.setText("")
                label_to = QLabel(contents)
                label_to.setFont(font)
                label_to.setAlignment(Qt.AlignCenter)
                label_to.setText("To")
                horizontal_labels.addWidget(label_from, 40)
                horizontal_labels.addWidget(label_empty, 20)
                horizontal_labels.addWidget(label_to, 40)
                vertical_layout.addLayout(horizontal_labels)

                font.setPointSize(15)
                horizontal_line_edits = QHBoxLayout()
                line_from = QLineEdit(contents)
                line_from.setFont(font)
                label_empty2 = QLabel(contents)
                label_empty2.setText("")
                line_to = QLineEdit(contents)
                line_to.setFont(font)
                horizontal_line_edits.addWidget(line_from, 40)
                horizontal_line_edits.addWidget(label_empty2, 20)
                horizontal_line_edits.addWidget(line_to, 40)
                self.line_edits.append((line_from, line_to))
                vertical_layout.addLayout(horizontal_line_edits)

                line = QFrame(contents)
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                vertical_layout.addWidget(line)

                check_box_negate = QCheckBox(contents)
                check_box_negate.setText("Grab values without this range.")
                vertical_layout.addWidget(check_box_negate, 15)
                check_box_remove_null = QCheckBox(contents)
                check_box_remove_null.setText("Remove null values.")
                vertical_layout.addWidget(check_box_remove_null)
                self.check_boxes.append((check_box_negate, check_box_remove_null))

                scroll_areas_layouts.append(vertical_layout)
                self.combo_box.addItem("{} ({})".format(self.df.columns[i], data_types[self.df.columns[i]]))

        grid_layout2 = QGridLayout(frame)

        self.stacked_widget.setCurrentIndex(0)
        grid_layout2.addWidget(self.stacked_widget, 0, 0, 1, 1)

        vertical_layout.addWidget(frame)
        buttons_horizontal_layout = QHBoxLayout()
        reset_button = QPushButton(self.dialog)
        buttons_horizontal_layout.addWidget(reset_button)
        reset_all_button = QPushButton(self.dialog)
        buttons_horizontal_layout.addWidget(reset_all_button)
        button_box = QDialogButtonBox(self.dialog)
        button_box.setOrientation(Qt.Horizontal)
        button_box.setStandardButtons(
            QDialogButtonBox.Apply | QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttons_horizontal_layout.addWidget(button_box)
        vertical_layout.addLayout(buttons_horizontal_layout)
        grid_layout.addLayout(vertical_layout, 0, 0, 1, 1)

        self.combo_box.currentIndexChanged.connect(self.set_visible_scroll_area2)

        label.setText("Current Attribute")
        reset_button.setText("Reset")
        reset_all_button.setText("Reset All")

        button_box.accepted.connect(self.dialog.accept)
        button_box.rejected.connect(self.dialog.reject)
        apply_button = button_box.button(QDialogButtonBox.Apply)
        apply_button.clicked.connect(self.apply_clicked)
        QMetaObject.connectSlotsByName(self.dialog)

    @property
    def output(self):
        return self.modified_df

    def set_visible_scroll_area2(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def apply_clicked(self):
        self.stacked_widget.currentWidget().setEnabled(False)
        index = self.combo_box.currentIndex()
        line_from, line_to = self.line_edits[index]
        filt = (self.df[self.df.columns[index]] > int(line_from.text())) & (
                    self.df[self.df.columns[index]] < int(line_to.text()))
        if self.check_boxes[index][0].isChecked():
            self.modified_df = self.df[~filt]
        else:
            self.modified_df = self.df[filt]
        print(self.modified_df.head())


class LinearRegression(InputOutputNode):
    def __init__(self, scene):
        super().__init__(scene, title="Linear Regression")

    def setup_ui(self):
        self.dialog.resize(496, 198)
        self.grid_layout = QGridLayout(self.dialog)
        self.vertical_layout = QVBoxLayout()
        self.horizontal_layout_target = QHBoxLayout()
        self.label = QLabel(self.dialog)
        self.horizontal_layout_target.addWidget(self.label)
        self.combo_box_target = QComboBox(self.dialog)
        self.horizontal_layout_target.addWidget(self.combo_box_target)
        self.vertical_layout.addLayout(self.horizontal_layout_target)
        self.horizontal_layout_degree = QHBoxLayout()
        self.label2 = QLabel(self.dialog)
        self.horizontal_layout_degree.addWidget(self.label2)
        self.spin_box_degree = QSpinBox(self.dialog)
        self.horizontal_layout_degree.addWidget(self.spin_box_degree)
        self.vertical_layout.addLayout(self.horizontal_layout_degree)
        self.check_box = QCheckBox(self.dialog)
        self.check_box.setEnabled(False)
        self.vertical_layout.addWidget(self.check_box)
        self.label_info = QLabel(self.dialog)
        font = QFont()
        font.setPointSize(10)
        self.label_info.setFont(font)
        self.vertical_layout.addWidget(self.label_info)
        self.grid_layout.addLayout(self.vertical_layout, 0, 0, 1, 1)
        self.button_box = QDialogButtonBox(self.dialog)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.grid_layout.addWidget(self.button_box, 1, 0, 1, 1)

        self.dialog.setWindowTitle("Linear Regression")
        self.spin_box_degree.setMinimum(1)
        self.label.setText("Target")
        self.label2.setText("Degree")
        self.check_box.setText("Include Bias")

        self.label_info.setText("Classic linear regression will be used If you do not specify degree. \n"
                                "Using high degree parameter might lead overfitting. Additionally, \n"
                                "for lower degrees the model will underfit the training data.")

        self.spin_box_degree.valueChanged.connect(lambda val: self.check_box.setEnabled(val >= 2))

        self.button_box.accepted.connect(self.dialog.accept)
        self.button_box.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_linear_regression(self):
        from sklearn.linear_model import LinearRegression
        if self.spin_box_degree.value() >= 2:
            from sklearn.preprocessing import PolynomialFeatures
            polynomial_regression = PolynomialFeatures(degree=self.spin_box_degree.value())
            self.X = polynomial_regression.fit_transform(self.X)
        self.model = LinearRegression()
        self.model.fit(self.X, self.y)


    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.combo_box_target.currentText()])
        self.y = self.df[self.combo_box_target.currentText()].values


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

    def setup_ui(self):
        self.dialog.resize(450, 155)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.dialog.sizePolicy().hasHeightForWidth())
        self.dialog.setSizePolicy(size_policy)
        self.button_box = QDialogButtonBox(self.dialog)
        self.button_box.setGeometry(QRect(100, 110, 341, 32))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.layout_widget = QWidget(self.dialog)
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
        self.dialog.setWindowTitle("Naive Bayes Classify")
        self.label_2.setText("Target selection")
        self.label_3.setText("Test size percentage")

        for i in range(len(self.df.columns)):
            self.combo_box.addItem(str(self.df.columns[i]))

        self.button_box.accepted.connect(self.apply_naive_bayes_classify)
        self.button_box.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_naive_bayes_classify(self):
        self.dialog.accept()
        print("apply naive bayes classify")
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.naive_bayes import GaussianNB
            from sklearn.model_selection import train_test_split

            X_train, self.X_test, y_train, self.y_test = train_test_split(self.X, self.y,
                                                                          test_size=int(self.line_edit_2.text()) / 100,
                                                                          random_state=1, stratify=self.y)

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

    def setup_ui(self):
        self.dialog.setObjectName("self.Dialog")
        self.dialog.resize(451, 205)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dialog.sizePolicy().hasHeightForWidth())
        self.dialog.setSizePolicy(sizePolicy)
        self.button_box = QDialogButtonBox(self.dialog)
        self.button_box.setGeometry(QRect(100, 150, 341, 32))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setObjectName("buttonBox")
        self.widget = QWidget(self.dialog)
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
        self.dialog.setWindowTitle("self.Dialog")
        self.label.setText("Number of neighbors")
        self.label2.setText("Target selection")
        self.label3.setText("Test size percentage")
        for i in range(len(self.df.columns)):
            self.comboBox.addItem(str(self.df.columns[i]))

        self.button_box.accepted.connect(self.apply_knn_classify)
        self.button_box.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_knn_classify(self):
        self.dialog.accept()
        print("apply knn classify")
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.neighbors import KNeighborsClassifier
            from sklearn.model_selection import train_test_split

            X_train, self.X_test, y_train, self.y_test = train_test_split(self.X, self.y,
                                                                          test_size=int(self.line_edit2.text()) / 100,
                                                                          random_state=1, stratify=self.y)

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

    def setup_ui(self):
        self.dialog.resize(450, 155)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.dialog.sizePolicy().hasHeightForWidth())
        self.dialog.setSizePolicy(size_policy)
        self.buttonBox = QDialogButtonBox(self.dialog)
        self.buttonBox.setGeometry(QRect(100, 110, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.layoutWidget = QWidget(self.dialog)
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

        self.dialog.setWindowTitle("Support Vector Machine")
        self.label_2.setText("Target selection")
        self.label_3.setText("Test size percentage")
        for i in range(len(self.df.columns)):
            self.comboBox.addItem(str(self.df.columns[i]))

        self.buttonBox.accepted.connect(self.apply_svm_classify)
        self.buttonBox.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_svm_classify(self):
        self.dialog.accept()
        print("apply svm classify")
        print(self.df.head())
        try:
            self.split_target_and_inputs()
            from sklearn.svm import SVC
            from sklearn.model_selection import train_test_split

            X_train, self.X_test, y_train, self.y_test = train_test_split(self.X, self.y,
                                                                          test_size=int(self.lineEdit_2.text()) / 100,
                                                                          random_state=1, stratify=self.y)

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

    def setup_ui(self):
        self.dialog.resize(450, 155)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.dialog.sizePolicy().hasHeightForWidth())
        self.dialog.setSizePolicy(size_policy)
        self.buttonBox = QDialogButtonBox(self.dialog)
        self.buttonBox.setGeometry(QRect(100, 110, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.layoutWidget = QWidget(self.dialog)
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
        self.dialog.setWindowTitle("self.Dialog")
        self.label2.setText("Target selection")
        self.label3.setText("Test size percentage")
        for i in range(len(self.df.columns)):
            self.combo_box.addItem(str(self.df.columns[i]))
        self.buttonBox.accepted.connect(self.apply_decision_tree_classify)
        self.buttonBox.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

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
