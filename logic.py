from matplotlib.figure import Figure

from form import *
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from algorithm import Data, Model
from configuration import *
from autor import Ui_Form
from results import Ui_Dialog
from result_logic import result_logic
import json


class logic(Ui_MainWindow):

    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        self.startButton.clicked.connect(self.start)
        self.startButton.setEnabled(False)
        self.closeButton.clicked.connect(self.click_exit)

        self.stepSize.valueChanged.connect(lambda: self.stepSizeSlider.setValue(int(self.stepSize.value() * 100)))
        self.l2.valueChanged.connect(lambda: self.l2Slider.setValue(int(self.l2.value() * 100)))
        self.momentum.valueChanged.connect(lambda: self.momentumSlider.setValue(int(self.momentum.value() * 100)))
        self.epoch.valueChanged.connect(lambda: self.epochSlider.setValue(self.epoch.value()))

        self.stepSizeSlider.valueChanged.connect(
            lambda: self.stepSize.setValue(float(self.stepSizeSlider.value() / 100)))
        self.l2Slider.valueChanged.connect(lambda: self.l2.setValue(float(self.l2Slider.value() / 100)))
        self.momentumSlider.valueChanged.connect(
            lambda: self.momentum.setValue(float(self.momentumSlider.value() / 100)))
        self.epochSlider.valueChanged.connect(lambda: self.epoch.setValue(self.epochSlider.value()))

        self.trainingImageButton.clicked.connect(self.selectTrainingImagePath)
        self.trainingLabelsButton.clicked.connect(self.selectTrainingLabelPath)
        self.validationImageButton.clicked.connect(self.selectValidationImagePath)
        self.validationLabelButton.clicked.connect(self.selectValidationLabelPath)

        self.actionZapisz.triggered.connect(self.save_configuration)
        self.actionWczytaj.triggered.connect(self.open_configuration)

        Form = QtWidgets.QWidget()
        ui = Ui_Form()
        ui.setupUi(Form)
        self.actionO_projekcie.triggered.connect(lambda: Form.show())

        self.Dialog = QtWidgets.QDialog()
        self.Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.DialogUi = result_logic(self.Dialog)

        self.actionPodgl_d.triggered.connect(lambda: self.Dialog.show())

        self.loadFilesButton.clicked.connect(self.loadData)

        self.is_data_loaded = False

    def prepare_results(self, errors, data):
        self.DialogUi.init_results(errors, data )

    def print_pressed(self):
        print("pressed")

    def write_line(self, text):
        item = self.verticalLayout_3.takeAt(self.verticalLayout_3.count() - 1)
        _translate = QtCore.QCoreApplication.translate
        new = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        new.setObjectName("new")
        self.verticalLayout_3.addWidget(new)
        new.setText(_translate("MainWindow", text))
        self.verticalLayout_3.addItem(item)
        app.processEvents()

    def draw_plot(self, plot):
        item = self.verticalLayout_3.takeAt(self.verticalLayout_3.count() - 1)
        self.verticalLayout_3.addWidget(plot)
        self.verticalLayout_3.addItem(item)
        # self.scrollAreaWidgetContents.adjustSize()
        app.processEvents()

    def clear(self):
        while self.verticalLayout_3.count() > 1:
            item = self.verticalLayout_3.takeAt(0)
            item.widget().setParent(None)
            item = None
        app.processEvents()

    def save_configuration(self):
        config = configuration(self.trainingImagePath.text(), self.trainingLabelsPath.text(),
                               self.validationImagePath.text(), self.validationLabelPath.text())
        config.print()

        file = open("configuration.json", "w")
        json_data = json.dumps(config.__dict__)
        file.write(json_data)
        file.close()

    def open_configuration(self):
        filename = QFileDialog.getOpenFileName()
        if filename[0] != "" and filename[0][-5:] == '.json':
            file = open(filename[0], "r")

            json_data = file.read()
            file.close()

            new_config = (configuration(**json.loads(json_data)))
            self.load_configuration(new_config)
        else:
            self.write_line("Nieprawidłowy plik")

    def load_configuration(self, config):
        _translate = QtCore.QCoreApplication.translate
        self.trainingImagePath.setText(_translate("MainWindow", config.training_images_path))
        self.trainingLabelsPath.setText(_translate("MainWindow", config.training_labels_path))
        self.validationImagePath.setText(_translate("MainWindow", config.validation_images_path))
        self.validationLabelPath.setText(_translate("MainWindow", config.validation_labels_path))
        self.write_line("Wczytano konfigurację")

    def start(self):
        self.clear()

        model = Model(self.stepSize.value(), self.epoch.value(), self.momentum.value(), self.l2.value(), True,
                      self.write_line)
        model.fit(self.data.X[:self.trainingExampleNum.value()], self.data.y[:self.trainingExampleNum.value()])
        self.write_line(f"poprawność : {model.evaluate(self.data.v_y[:self.validationExampleNum.value()], model.predict(self.data.v_X[:self.validationExampleNum.value()]))}")
        self.canvas = FigureCanvasQTAgg(model.figure)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.canvas.setSizePolicy(sizePolicy)

        self.draw_plot(self.canvas)
        self.prepare_results(model.errors, self.data.v_X)

    def click(self):
        counter = self.verticalLayout_3.count()
        print(counter)
        self.write_line("adf")

    def selectTrainingImagePath(self):
        self.open_dialog_box(self.trainingImagePath)

    def selectTrainingLabelPath(self):
        self.open_dialog_box(self.trainingLabelsPath)

    def selectValidationImagePath(self):
        self.open_dialog_box(self.validationImagePath)

    def selectValidationLabelPath(self):
        self.open_dialog_box(self.validationLabelPath)

    def loadData(self):
        self.data = Data(self.trainingImagePath.text(), self.trainingLabelsPath.text(), self.validationImagePath.text(),
                         self.validationLabelPath.text())
        if self.data.error != "":
            self.clear()
            self.write_line(self.data.error)
            self.trainingExampleNum.setEnabled(False)
            self.validationExampleNum.setEnabled(False)
            self.startButton.setEnabled(False)
        else:
            self.trainingExampleNum.setEnabled(True)
            self.validationExampleNum.setEnabled(True)

            _translate = QtCore.QCoreApplication.translate
            self.maxTraining.setText(_translate("MainWindow", f"Max:{self.data.getSizes()[0]}"))
            self.trainingExampleNum.setMaximum(self.data.getSizes()[0])
            self.trainingExampleNum.setValue(self.data.getSizes()[0])
            self.maxValidation.setText(_translate("MainWindow", f"Max:{self.data.getSizes()[1]}"))
            self.validationExampleNum.setMaximum(self.data.getSizes()[1])
            self.validationExampleNum.setValue(self.data.getSizes()[1])
            self.maxValidation.setText(_translate("MainWindow", f"Max:{self.data.getSizes()[1]}"))
            self.startButton.setEnabled(True)
            self.is_data_loaded = True
            self.write_line("Poprawnie wczytano dane\n")

    def open_dialog_box(self, label):
        filename = QFileDialog.getOpenFileName()

        if filename[0] != "":
            _translate = QtCore.QCoreApplication.translate
            label.setText(_translate("MainWindow", filename[0]))

    def click_exit(self):
        exit()




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = logic(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
