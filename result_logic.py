from PyQt5 import QtWidgets
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from results import Ui_Dialog
import matplotlib.pyplot as plt

class result_logic(Ui_Dialog):

    def __init__(self, Window):
        self.setupUi(Window)
        self.results.currentIndexChanged.connect(self.results_changed)

    def init_results(self, content, data):
        self.data = data
        self.results.clear()
        self.results.addItems([str(i) for i in content])


    def clear(self):
        while self.verticalLayout_2.count() > 0:
            item = self.verticalLayout_2.takeAt(0)
            item.widget().setParent(None)
            item = None

    def results_changed(self):
        if(self.results.count() > 0):
            self.clear()
            self.figure = plt.Figure()
            self.figure.clear()
            print(self.results.currentText())
            image = np.asarray(self.data[int(self.results.currentText())])
            image = image.reshape((28,28))
            ax = self.figure.add_subplot(111)
            ax.imshow(image)
            plt.imshow(image)
            self.canvas = FigureCanvasQTAgg(self.figure)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            self.canvas.setSizePolicy(sizePolicy)

            self.draw_plot(self.canvas)



    def draw_plot(self, plot):
        self.verticalLayout_2.addWidget(plot)
