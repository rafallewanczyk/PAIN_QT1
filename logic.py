from form import *
from PyQt5.QtWidgets import QFileDialog
from algorithm import Data
from configuration import *
import json


class logic(Ui_MainWindow):
    # self.startButton.clicked.connect(self.click)
    # self.closeButton.clicked.connect(self.click_exit);

    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        self.startButton.clicked.connect(self.click)
        self.startButton.setEnabled(False)
        self.closeButton.clicked.connect(self.click_exit)

        self.maxTrainingValidator = QtGui.QIntValidator()
        self.maxValidationValidator = QtGui.QIntValidator()
        self.epochValidator = QtGui.QIntValidator()

        self.trainingExampleNum.setValidator(self.maxTrainingValidator)
        self.validationExampleNum.setValidator(self.maxValidationValidator)
        self.epochNumber.setValidator(self.epochValidator)

        self.stepSize.valueChanged.connect(lambda : self.stepSizeSlider.setValue(int(self.stepSize.value() * 100)))
        self.l2.valueChanged.connect(lambda : self.l2Slider.setValue(int(self.l2.value() * 100)))
        self.momentum.valueChanged.connect(lambda : self.momentumSlider.setValue(int(self.momentum.value() * 100)))

        self.stepSizeSlider.valueChanged.connect(lambda: self.stepSize.setValue(float(self.stepSizeSlider.value()/100)))
        self.l2Slider.valueChanged.connect(lambda: self.l2.setValue(float(self.l2Slider.value()/100)))
        self.momentumSlider.valueChanged.connect(lambda: self.momentum.setValue(float(self.momentumSlider.value()/100)))


        # self.trainingExampleNum.textChanged.connect(self.check_state)
        # self.trainingExampleNum.textChanged.emit(self.trainingExampleNum.text())
        # self.validationExampleNum.textChanged.connect(self.check_state)

        self.trainingImageButton.clicked.connect(self.selectTrainingImagePath)
        self.trainingLabelsButton.clicked.connect(self.selectTrainingLabelPath)
        self.validationImageButton.clicked.connect(self.selectValidationImagePath)
        self.validationLabelButton.clicked.connect(self.selectValidationLabelPath)

        self.actionZapisz.triggered.connect(self.save_configuration)
        self.actionWczytaj.triggered.connect(self.open_configuration)

        self.loadFilesButton.clicked.connect(self.loadData)

        self.is_data_loaded = False;

        # self.stepSize.textChanged.emit(self.stepSize.text())

    def print_pressed(self):
        print("pressed")




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
            print("nieprawidlowy plik")

    def load_configuration(self, config):
        _translate = QtCore.QCoreApplication.translate
        self.trainingImagePath.setText(_translate("MainWindow", config.training_images_path))
        self.trainingLabelsPath.setText(_translate("MainWindow", config.training_labels_path))
        self.validationImagePath.setText(_translate("MainWindow", config.validation_images_path))
        self.validationLabelPath.setText(_translate("MainWindow", config.validation_labels_path))

    def click(self):
        item = self.verticalLayout_3.itemAt(self.counter + 2)
        print(item)
        self.verticalLayout_3.removeItem(item)
        # self.spacerItem.setParent(-1)
        _translate = QtCore.QCoreApplication.translate
        new = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        new.setObjectName("new")
        self.verticalLayout_3.addWidget(new)
        new.setText(_translate("MainWindow", f"nowy label{self.counter}"))
        self.counter += 1

        self.verticalLayout_3.addItem(item)

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
            print(self.data.error)
            self.trainingExampleNum.setEnabled(False)
            self.validationExampleNum.setEnabled(False)
        else:
            self.trainingExampleNum.setEnabled(True)
            self.validationExampleNum.setEnabled(True)

            _translate = QtCore.QCoreApplication.translate
            self.maxTraining.setText(_translate("MainWindow", f"Max:{self.data.getSizes()[0]}"))
            self.maxValidation.setText(_translate("MainWindow", f"Max:{self.data.getSizes()[1]}"))
            self.maxTrainingValidator.setRange(0, self.data.getSizes()[0])
            self.maxValidationValidator.setRange(1, self.data.getSizes()[1])
            self.is_data_loaded = True

    def open_dialog_box(self, label):
        filename = QFileDialog.getOpenFileName()

        _translate = QtCore.QCoreApplication.translate
        label.setText(_translate("MainWindow", filename[0]))

    def click_exit(self):
        exit()

    def check_state(self, *args, **kwargs):
        print("check state works")
        sender = self.sender()
        print(sender)
        # state = validator.validate(self.stepSize.text(), 0)[0]
        # if state == QtGui.QValidator.Acceptable:
        #     color = '#c4df9b'  # green
        # elif state == QtGui.QValidator.Intermediate:
        #     color = '#fff79a'  # yellow
        # else:
        #     color = '#f6989d'  # red
        # self.stepSize.setStyleSheet('QLineEdit { background-color: %s }' % color)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = logic(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
