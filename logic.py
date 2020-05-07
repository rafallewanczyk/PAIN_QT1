from form import *

class logic (Ui_MainWindow):
    # self.startButton.clicked.connect(self.click)
    # self.closeButton.clicked.connect(self.click_exit);

    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        self.startButton.clicked.connect(self.click)
        self.startButton.setEnabled(False)
        self.closeButton.clicked.connect(self.click_exit)
        self.validator = QtGui.QDoubleValidator()
        self.validator.setRange(0, 1, 5)
        self.stepSize.setValidator(self.validator)

        self.stepSize.textChanged.connect(self.check_state)
        # self.stepSize.textChanged.emit(self.stepSize.text())


    def click(self):
        item = self.verticalLayout_3.itemAt(self.counter+2)
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


    def click_exit(self):
        exit()

    def check_state(self, *args, **kwargs):
        print("check state works")
        # sender = self.sender()
        validator =self.stepSize.validator()
        state = validator.validate(self.stepSize.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#c4df9b'  # green
        elif state == QtGui.QValidator.Intermediate:
            color = '#fff79a'  # yellow
        else:
            color = '#f6989d'  # red
        self.stepSize.setStyleSheet('QLineEdit { background-color: %s }' % color)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui =logic(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
