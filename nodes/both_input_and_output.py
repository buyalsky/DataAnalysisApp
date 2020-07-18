import sys

from node import InputOutputNode

try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *

sys.path.append("..")


class AttributeRemover(InputOutputNode):
    check_boxes = None
    df = None

    def __init__(self, scene):
        super().__init__(scene, title="Attribute Remover", icon_name="icons/preprocessing128.png")
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
        self.df = self.fed_data["data_frame"]
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
        if dropped_columns:
            self.modified_data["data_frame"] = self.df.drop(dropped_columns, axis=1)

        self.is_finished = True
        self.return_file()


class Filter(InputOutputNode):
    df = None
    stacked_widget = None
    combo_box = None
    line_edits = None
    check_boxes = None

    def __init__(self, scene):
        super().__init__(scene, title="Filter", icon_name="icons/filter128.png")
        self.node_type = "filter.filter"

    def setup_ui(self):
        self.dialog.resize(548, 268)
        self.gridLayout = QGridLayout(self.dialog)
        self.horizontal_layout = QHBoxLayout()
        self.label = QLabel(self.dialog)
        self.horizontal_layout.addWidget(self.label)
        self.combo_box = QComboBox(self.dialog)
        self.horizontal_layout.addWidget(self.combo_box)
        self.gridLayout.addLayout(self.horizontal_layout, 0, 0, 1, 1)

        self.scroll_area = QScrollArea(self.dialog)
        self.scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 590, 349))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.stacked_widget = QStackedWidget(self.scrollAreaWidgetContents)

        scroll_areas = []
        scroll_areas_widget_contents = []
        scroll_areas_layouts = []
        self.line_edits = []
        self.check_boxes = []
        self.df = self.fed_data["data_frame"]
        data_types = dict(self.df.dtypes)
        self.filtered_columns = []

        for i in range(len(self.df.columns)):
            if "int" in str(data_types[self.df.columns[i]]) or "float" in str(data_types[self.df.columns[i]]):
                scroll_area = QScrollArea(self.dialog)
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

                check_box_negate = QCheckBox(contents)
                check_box_negate.setText("Grab values without this range.")
                vertical_layout.addWidget(check_box_negate, 15)
                # check_box_remove_null = QCheckBox(contents)
                # check_box_remove_null.setText("Remove null values.")
                # vertical_layout.addWidget(check_box_remove_null)
                self.check_boxes.append((check_box_negate, None))

                scroll_areas_layouts.append(vertical_layout)
                self.combo_box.addItem("{} ({})".format(self.df.columns[i], data_types[self.df.columns[i]]))
                self.filtered_columns.append(self.df.columns[i])

        self.page = QWidget()
        self.stacked_widget.addWidget(self.page)
        self.page_2 = QWidget()
        self.stacked_widget.addWidget(self.page_2)
        self.gridLayout_3.addWidget(self.stacked_widget, 0, 0, 1, 1)

        self.scroll_area.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scroll_area, 1, 0, 1, 1)
        horizontal_layout_button = QHBoxLayout()
        reset_button = QPushButton(self.dialog)
        horizontal_layout_button.addWidget(reset_button)
        reset_all_button = QPushButton(self.dialog)
        horizontal_layout_button.addWidget(reset_all_button)
        self.buttonBox = QDialogButtonBox(self.dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Apply | QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        horizontal_layout_button.addWidget(self.buttonBox)
        self.gridLayout.addLayout(horizontal_layout_button, 2, 0, 1, 1)

        self.dialog.setWindowTitle("Filter")
        self.label.setText("Attribute")
        reset_button.setText("Reset")
        reset_all_button.setText("Reset All")

        reset_all_button.clicked.connect(self.remove_all_filters)
        reset_button.clicked.connect(self.remove_filter)

        self.stacked_widget.setCurrentIndex(0)

        self.combo_box.currentIndexChanged.connect(self.set_visible_scroll_area2)

        self.buttonBox.accepted.connect(self.apply_filters)
        self.buttonBox.rejected.connect(self.dialog.reject)
        apply_button = self.buttonBox.button(QDialogButtonBox.Apply)
        apply_button.clicked.connect(self.add_filter)
        QMetaObject.connectSlotsByName(self.dialog)

        self.filters = {}

    def set_visible_scroll_area2(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def add_filter(self):
        self.stacked_widget.currentWidget().setEnabled(False)
        index = self.combo_box.currentIndex()
        line_from, line_to = self.line_edits[index]

        filt = (self.df[self.filtered_columns[index]] > int(line_from.text())) & (
                self.df[self.filtered_columns[index]] < int(line_to.text()))

        self.filters[self.stacked_widget.currentIndex()] = (self.check_boxes[index][0].isChecked(), filt)

    def apply_filters(self):
        if self.filters:
            filters = list(self.filters.values())
            flt = filters.pop()
            cumulative_filter = ~flt[1] if flt[0] else flt[1]

            for t in filters:
                if t[0]:
                    cumulative_filter &= ~t[1]
                else:
                    cumulative_filter &= t[1]

            self.modified_data["data_frame"] = self.df[cumulative_filter]

            print(self.modified_data["data_frame"].head())

        self.return_file()

    def remove_filter(self):
        self.filters.pop(self.stacked_widget.currentIndex(), None)
        self.stacked_widget.currentWidget().setEnabled(True)

    def remove_all_filters(self):
        for value in self.filters.values():
            value = None
        self.modified_data["data_frame"] = self.df
        for i in range(self.stacked_widget.count()):
            self.stacked_widget.widget(i).setEnabled(True)


class LinearRegression(InputOutputNode):
    def __init__(self, scene):
        super().__init__(scene, title="Linear Regression", icon_name="icons/linear-reg128.png")

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

        self.df = self.fed_data["data_frame"]

        for i in range(len(self.df.columns)):
            self.combo_box_target.addItem(str(self.df.columns[i]))

        self.dialog.setWindowTitle("Linear Regression")
        self.spin_box_degree.setMinimum(1)
        self.label.setText("Target")
        self.label2.setText("Degree")
        self.check_box.setText("Include Bias")

        self.label_info.setText("Classic linear regression will be used If you do not specify degree. \n"
                                "Using high degree parameter might lead overfitting. Additionally, \n"
                                "for lower degrees the model likely underfit the training data.")

        self.spin_box_degree.valueChanged.connect(lambda val: self.check_box.setEnabled(val >= 2))

        self.button_box.accepted.connect(self.apply_linear_regression)
        self.button_box.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_linear_regression(self):
        columns_to_drop = []
        columns_to_transform = []
        data_types = dict(self.df.dtypes)
        for i in range(len(self.df.columns)):
            if "object" in str(data_types[self.df.columns[i]]) or "category" in str(data_types[self.df.columns[i]]):
                columns_to_transform.append(self.df.columns[i])
            elif not("int" in str(data_types[self.df.columns[i]]) or "float" in str(data_types[self.df.columns[i]])):
                    columns_to_drop.append(self.df.columns[i])

        if columns_to_drop:
            self.df = self.df.drop(columns=columns_to_drop)

        self.split_target_and_inputs()
        from sklearn.linear_model import LinearRegression

        if columns_to_transform:
            from sklearn.compose import ColumnTransformer
            from sklearn.preprocessing import OneHotEncoder

            t = ColumnTransformer(transformers=[("onehot", OneHotEncoder(), columns_to_transform)],
                                  remainder="passthrough")
            t.fit_transform(self.df)
            self.X = t.fit_transform(self.X)
            self.modified_data["column_transformer"] = t

        elif self.spin_box_degree.value() >= 2:
            from sklearn.preprocessing import PolynomialFeatures
            polynomial_regression = PolynomialFeatures(degree=self.spin_box_degree.value())
            self.X = polynomial_regression.fit_transform(self.X)

        model = LinearRegression()
        model.fit(self.X, self.y)

        self.is_finished = True
        self.modified_data["model"] = model
        self.modified_data["target_label"] = self.combo_box_target.currentText()

        self.return_file()

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.combo_box_target.currentText()])
        self.y = self.df[self.combo_box_target.currentText()].values


class NaiveBayesClassify(InputOutputNode):
    button_box = None
    layout_widget = None
    horizontal_layout = None
    vertical_layout = None
    label_2 = None
    combo_box = None
    label_3 = None
    vertical_layout_2 = None
    train_percentage = None

    def __init__(self, scene):
        super().__init__(scene, title="Naive Bayes Classifier", icon_name="icons/classification128.png")
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
        self.train_percentage = QDoubleSpinBox(self.layout_widget)
        self.train_percentage.setMinimum(0.05)
        self.train_percentage.setMaximum(0.95)
        self.train_percentage.setSingleStep(0.05)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.train_percentage.sizePolicy().hasHeightForWidth())
        self.train_percentage.setSizePolicy(size_policy)
        self.vertical_layout_2.addWidget(self.train_percentage)
        self.horizontal_layout.addLayout(self.vertical_layout_2)

        self.dialog.setWindowTitle("Naive Bayes Classifier")
        self.label_2.setText("Target selection")
        self.label_3.setText("Test size percentage")

        self.df = self.fed_data["data_frame"]

        for i in range(len(self.df.columns)):
            self.combo_box.addItem(str(self.df.columns[i]))

        self.button_box.accepted.connect(self.apply_naive_bayes_classify)
        self.button_box.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_naive_bayes_classify(self):
        self.dialog.accept()
        try:
            self.split_target_and_inputs()
            from sklearn.naive_bayes import GaussianNB
            from sklearn.model_selection import train_test_split

            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,
                                                                test_size=self.train_percentage.value(),
                                                                random_state=1, stratify=self.y)

            model = GaussianNB()
            model.fit(X_train, y_train)
        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.is_finished = True
            self.modified_data["model"] = model
            self.modified_data["test_data"] = (X_test, y_test)
            self.modified_data["target_label"] = self.combo_box.currentText()
            self.modified_data["classification_type"] = "Naive Bayes Classification"
            self.return_file()

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.combo_box.currentText()])
        self.y = self.df[self.combo_box.currentText()].values


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
    train_percentage = None

    def __init__(self, scene):
        super().__init__(scene, title="Knn", icon_name="icons/classification128.png")
        self.node_type = "supervised.knn"

    def setup_ui(self):
        self.dialog.resize(451, 205)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.dialog.sizePolicy().hasHeightForWidth())
        self.dialog.setSizePolicy(size_policy)
        self.button_box = QDialogButtonBox(self.dialog)
        self.button_box.setGeometry(QRect(100, 150, 341, 32))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.widget = QWidget(self.dialog)
        self.widget.setGeometry(QRect(20, 30, 401, 111))
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout = QVBoxLayout()
        self.label = QLabel(self.widget)
        self.vertical_layout.addWidget(self.label)
        self.label2 = QLabel(self.widget)
        self.vertical_layout.addWidget(self.label2)
        self.label3 = QLabel(self.widget)
        self.vertical_layout.addWidget(self.label3)
        self.horizontal_layout.addLayout(self.vertical_layout)
        self.vertical_layout2 = QVBoxLayout()
        self.line_edit = QSpinBox(self.widget)
        self.line_edit.setMinimum(1)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.line_edit.sizePolicy().hasHeightForWidth())
        self.line_edit.setSizePolicy(size_policy)
        self.vertical_layout2.addWidget(self.line_edit)
        self.combo_box = QComboBox(self.widget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.combo_box.sizePolicy().hasHeightForWidth())
        self.combo_box.setSizePolicy(size_policy)
        self.vertical_layout2.addWidget(self.combo_box)
        self.train_percentage = QDoubleSpinBox(self.widget)
        self.train_percentage.setMinimum(0.05)
        self.train_percentage.setMaximum(0.95)
        self.train_percentage.setSingleStep(0.05)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.train_percentage.sizePolicy().hasHeightForWidth())
        self.train_percentage.setSizePolicy(size_policy)
        self.vertical_layout2.addWidget(self.train_percentage)
        self.horizontal_layout.addLayout(self.vertical_layout2)

        self.dialog.setWindowTitle("KNN Classifier")
        self.label.setText("Number of neighbors")
        self.label2.setText("Target selection")
        self.label3.setText("Test size percentage")
        self.df = self.fed_data["data_frame"]
        for i in range(len(self.df.columns)):
            self.combo_box.addItem(str(self.df.columns[i]))

        self.button_box.accepted.connect(self.apply_knn_classify)
        self.button_box.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_knn_classify(self):
        self.dialog.accept()
        try:
            self.split_target_and_inputs()
            from sklearn.neighbors import KNeighborsClassifier
            from sklearn.model_selection import train_test_split

            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,
                                                                test_size=self.train_percentage.value(),
                                                                random_state=1, stratify=self.y)

            model = KNeighborsClassifier(n_neighbors=self.line_edit.value())
            model.fit(X_train, y_train)
        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.modified_data["model"] = model
            self.modified_data["test_data"] = (X_test, y_test)
            self.modified_data["target_label"] = self.combo_box.currentText()
            self.modified_data["classification_type"] = "K-Nearest Neighbors Classification"
            self.is_finished = True
            self.return_file()

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.combo_box.currentText()])
        self.y = self.df[self.combo_box.currentText()].values


class SVM(InputOutputNode):
    def __init__(self, scene):
        super().__init__(scene, title="SVM", icon_name="icons/classification128.png")
        self.node_type = "supervised.svm"

    def setup_ui(self):
        self.dialog.resize(450, 155)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.dialog.sizePolicy().hasHeightForWidth())
        self.dialog.setSizePolicy(size_policy)
        button_box = QDialogButtonBox(self.dialog)
        button_box.setGeometry(QRect(100, 110, 341, 32))
        button_box.setOrientation(Qt.Horizontal)
        button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
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
        self.train_percentage = QDoubleSpinBox(self.layoutWidget)
        self.train_percentage.setMinimum(0.05)
        self.train_percentage.setMaximum(0.95)
        self.train_percentage.setSingleStep(0.05)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.train_percentage.sizePolicy().hasHeightForWidth())
        self.train_percentage.setSizePolicy(size_policy)
        self.verticalLayout_2.addWidget(self.train_percentage)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.dialog.setWindowTitle("Support Vector Machine")
        self.label_2.setText("Target selection")
        self.label_3.setText("Test size percentage")
        self.df = self.fed_data["data_frame"]

        for i in range(len(self.df.columns)):
            self.comboBox.addItem(str(self.df.columns[i]))

        button_box.accepted.connect(self.apply_svm_classify)
        button_box.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_svm_classify(self):
        self.dialog.accept()
        try:
            self.split_target_and_inputs()
            from sklearn.svm import SVC
            from sklearn.model_selection import train_test_split

            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,
                                                                test_size=self.train_percentage.value(),
                                                                random_state=1, stratify=self.y)

            model = SVC(random_state=1)
            model.fit(X_train, y_train)
        except Exception as e:
            QMessageBox.warning(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.modified_data["model"] = model
            self.modified_data["test_data"] = (X_test, y_test)
            self.modified_data["target_label"] = self.comboBox.currentText()
            self.modified_data["classification_type"] = "Support Vector Machine Classification"
            self.is_finished = True
            self.return_file()

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.comboBox.currentText()])
        self.y = self.df[self.comboBox.currentText()].values


class DecisionTree(InputOutputNode):
    buttonBox = None
    layoutWidget = None
    horizontal_layout = None
    vertical_layout = None
    vertical_layout2 = None
    label2 = None
    label3 = None
    combo_box = None
    train_percentage_input = None

    def __init__(self, scene):
        super().__init__(scene, title="Decision Tree Classifier", icon_name="icons/decision-tree128.png")
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
        self.train_percentage_input = QDoubleSpinBox(self.layoutWidget)
        self.train_percentage_input.setMinimum(0.05)
        self.train_percentage_input.setMaximum(0.95)
        self.train_percentage_input.setSingleStep(0.05)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.train_percentage_input.sizePolicy().hasHeightForWidth())
        self.train_percentage_input.setSizePolicy(size_policy)
        self.vertical_layout2.addWidget(self.train_percentage_input)
        self.horizontal_layout.addLayout(self.vertical_layout2)

        self.dialog.setWindowTitle("Decision Tree Classifier")
        self.label2.setText("Target selection")
        self.label3.setText("Test size percentage")

        self.df = self.fed_data["data_frame"]
        for i in range(len(self.df.columns)):
            self.combo_box.addItem(str(self.df.columns[i]))
        self.buttonBox.accepted.connect(self.apply_decision_tree_classify)
        self.buttonBox.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_decision_tree_classify(self):
        self.dialog.accept()
        try:
            self.split_target_and_inputs()
            from sklearn.tree import DecisionTreeClassifier
            from sklearn.model_selection import train_test_split

            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,
                                                                test_size=self.train_percentage_input.value(),
                                                                random_state=1,
                                                                stratify=self.y)

            model = DecisionTreeClassifier()
            model.fit(X_train, y_train)
        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.modified_data["model"] = model
            self.modified_data["test_data"] = (X_test, y_test)
            self.modified_data["target_label"] = self.combo_box.currentText()
            self.modified_data["classification_type"] = "Decision Tree Classification"
            self.is_finished = True
            self.return_file()

    def split_target_and_inputs(self):
        self.X = self.df.drop(columns=[self.combo_box.currentText()])
        self.y = self.df[self.combo_box.currentText()].values


class KmeansClustering(InputOutputNode):
    def __init__(self, scene):
        super().__init__(scene, title="K-Means Clustering", icon_name="icons/clustering128.png")

    def setup_ui(self):
        self.dialog.resize(451, 130)
        self.grid_layout = QGridLayout(self.dialog)
        label = QLabel(self.dialog)
        self.grid_layout.addWidget(label, 0, 0, 1, 1)
        self.spin_box = QSpinBox(self.dialog)
        self.spin_box.setMinimum(1)
        self.grid_layout.addWidget(self.spin_box, 0, 1, 1, 1)
        self.button_box = QDialogButtonBox(self.dialog)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.grid_layout.addWidget(self.button_box, 1, 0, 1, 2)
        self.dialog.setWindowTitle("K-Means Clustering")
        label.setText("Number of cluster")
        self.button_box.accepted.connect(self.apply_kmeans_clustering)
        self.button_box.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_kmeans_clustering(self):
        try:
            from sklearn.cluster import KMeans
            model = KMeans(n_clusters=self.spin_box.value())
            clusters = model.fit_predict(self.fed_data["data_frame"])

        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.modified_data["model"] = model
            self.modified_data["data_frame"]["label"] = clusters
            self.modified_data["data_frame"]["label"] = self.modified_data["data_frame"]["label"].astype("category")
            self.modified_data["target_label"] = "label"
            self.modified_data["clustering_algorithm"] = "K-Means Clustering"
            self.is_finished = True
            self.return_file()


class HierarchicalClustering(InputOutputNode):
    def __init__(self, scene):
        super().__init__(scene, title="Hierarchical Clustering", icon_name="icons/clustering128.png")

    def setup_ui(self):
        self.dialog.resize(451, 130)
        self.grid_layout = QGridLayout(self.dialog)
        label = QLabel(self.dialog)
        self.grid_layout.addWidget(label, 0, 0, 1, 1)
        self.spin_box = QSpinBox(self.dialog)
        self.spin_box.setMinimum(1)
        self.grid_layout.addWidget(self.spin_box, 0, 1, 1, 1)
        self.button_box = QDialogButtonBox(self.dialog)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.grid_layout.addWidget(self.button_box, 1, 0, 1, 2)
        self.dialog.setWindowTitle("Hierarchical Clustering")
        label.setText("Number of cluster")
        self.button_box.accepted.connect(self.apply_hierarchical_clustering)
        self.button_box.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def apply_hierarchical_clustering(self):
        try:
            from sklearn.cluster import AgglomerativeClustering
            model = AgglomerativeClustering(n_clusters=self.spin_box.value())
            clusters = model.fit_predict(self.fed_data["data_frame"])

        except Exception as e:
            QMessageBox.about(
                self.scene.parent_widget,
                "Error happened",
                str(e)
            )
        else:
            self.modified_data["data_frame"]["label"] = clusters
            self.modified_data["data_frame"]["label"] = self.modified_data["data_frame"]["label"].astype("category")
            self.modified_data["target_label"] = "label"
            self.modified_data["clustering_algorithm"] = "Agglomerative Clustering"
            self.is_finished = True
            self.return_file()
