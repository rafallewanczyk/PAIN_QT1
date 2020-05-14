import gzip
import numpy as np
import time
import matplotlib.pyplot as plt


class Data:
    IMAGE_SIZE = 28
    error = ""

    def __init__(self, train_images_path, train_labels_path, validation_images_path, validation_labels_path):

        self.is_prime = np.vectorize(self.is_prime)

        if train_images_path[-3:] == '.gz':
            self.train_images = gzip.open(train_images_path, "r")
            if int.from_bytes(self.train_images.read(4), 'big') == 2051:
                self.train_images.read(12);
                self.X = self.generate_matrices(self.train_images.read(), self.IMAGE_SIZE)
            else:
                self.error += "Zbiór treningowy obrazów - niepoprwany header plikui\n"
        else:
            self.error += "Zbiór treningowy obrazów - niepoprawne rozszerzenie pliku\n"

        if train_labels_path[-3:] == '.gz':
            self.train_labels = gzip.open(train_labels_path, "r")
            if int.from_bytes(self.train_labels.read(4), 'big') == 2049:
                self.train_labels.read(4);
                self.y = self.is_prime(self.generate_matrices(self.train_labels.read(), 1))
            else:
                self.error += "Zbiór treningowy etykiet- niepoprwany header plikui\n"
        else:
            self.error += "Zbiór treningowy etykiet - niepoprawne rozszerzenie pliku\n"

        if validation_images_path[-3:] == '.gz':
            self.validation_images = gzip.open(validation_images_path, "r")
            if int.from_bytes(self.validation_images.read(4), 'big') == 2051:
                self.validation_images.read(12);
                self.v_X = self.generate_matrices(self.validation_images.read(), self.IMAGE_SIZE)
            else:
                self.error += "Zbiór walidacyjny obrazów - niepoprwany header plikui\n"
        else:
            self.error += "Zbiór walidacyjny obrazów- niepoprawne rozszerzenie pliku\n"

        if validation_labels_path[-3:] == '.gz':
            self.validation_labels = gzip.open(validation_labels_path, "r")
            if int.from_bytes(self.validation_labels.read(4), 'big') == 2049:
                self.validation_labels.read(4);
                self.v_y = self.is_prime(self.generate_matrices(self.validation_labels.read(), 1))
            else:
                self.error += "Zbiór walidacyjny etykiet- niepoprwany header plikui\n"
        else:
            self.error += "Zbiór walidacyjny etykiet- niepoprawne rozszerzenie pliku\n"

        if (self.error == ""):
            if self.X.shape[0] != self.y.shape[0]:
                self.error += "Dane treningowe - niezgodne wymiary tablic\n"
            if self.v_X.shape[0] != self.v_y.shape[0]:
                self.error += "Dane walidacyjne- niezgodne wymiary tablic\n"

        if self.error == "":
            y_map = self.generate_map(self.y)
            vy_map = self.generate_map(self.v_y)
            self.X = np.delete(self.X, y_map, 0)
            self.y = np.delete(self.y, y_map, 0)
            self.v_X = np.delete(self.v_X, vy_map, 0)
            self.v_y = np.delete(self.v_y, vy_map, 0)

            # todo clear data

    def getSizes(self):
        return self.X.shape[0], self.v_X.shape[0]


    def is_prime(self, x):
        if x in [2, 3, 5, 7]:
            return 1
        elif x in [4, 6, 8]:
            return 0
        return -1

    def generate_matrices(self, buffer, length):
        M = np.frombuffer(buffer, dtype=np.uint8)
        M = M.reshape(int(M.shape[0] / (length ** 2)), -1)

        return M

    def generate_map(self, labels):
        map = np.argwhere(labels == -1)
        return map.T[0]


class Model():
    IMAGE_SIZE = 28

    def __init__(self, step_size=0.1, epochs=8, momentum=0.9, reg=0.00001, verbose=True, write_line = None):
        self.theta = np.random.rand(self.IMAGE_SIZE ** 2, 1)
        self.V = np.random.rand(self.IMAGE_SIZE ** 2, 1)
        self.step_size = step_size
        self.epochs = epochs
        self.momentum = momentum
        self.reg = reg
        self.verbose = verbose
        self.write_line = write_line

    def __sigma(self, z):
        return 1 / (1 + np.exp(-z))

    def __cost(self, theta, X, y):
        cost = y * np.log(self.__sigma(np.matmul(X, self.theta)) + 1e-7) + (1 - y) * np.log(
            1 - self.__sigma(np.matmul(X, self.theta)) + 1e-7)
        reg_cost = self.reg / 2 * self.theta ** 2
        return cost.mean() - reg_cost.sum() / X.shape[0]

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        self.write_line(f"Zaczynam trening, szacowany czas {self.epochs * 2}s")
        y_axis = [self.__cost(self.theta, X, y)]

        start = time.time()
        iteration_start = start
        permutation = np.arange(X.shape[0])

        for epoch in range(1, self.epochs + 1):
            np.random.shuffle(permutation)
            for i in permutation:
                gradient = (y[i] - self.__sigma(np.matmul(self.theta.T, X[i]))) * X[i].reshape(self.IMAGE_SIZE ** 2,
                                                                                               1) - 2 * self.reg * self.theta
                self.V = self.momentum * self.V + (1 - self.momentum) * gradient
                self.theta = self.theta + self.step_size * self.V

            self.write_line(f"{epoch}/{self.epochs} iteracja zakonczona po {time.time() - iteration_start}")
            iteration_start = time.time()

            if (self.verbose == True):
                y_axis.append(self.__cost(self.theta, X, y))

        if (self.verbose == True):
            x_axis = np.arange(0, len(y_axis))
            self.figure = plt.Figure()
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x_axis, y_axis)
            self.figure.suptitle(f'epochs:{self.epochs}, step_size:{self.step_size}, momentum:{self.momentum},l2:{self.reg}')

            # plt.show()


        self.write_line(f"trening zakonczony po {time.time() - start}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.__sigma(X @ self.theta)

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        self.errors = []
        correct = 0
        total = 0
        for i in range(y_true.shape[0]):
            if y_true[i] == np.rint(y_pred[i]):
                correct += 1
            else:
                self.errors.append(i)
            total += 1
        return correct / total

    def confiuson_matrix(self, y_true, y_pred):
        true_positive = true_negative = false_positive = false_negative = 0
        for i in range(y_true.shape[0]):
            if y_true[i] == np.rint(y_pred[i]) and y_true[i] == 1:
                true_positive += 1
            elif y_true[i] == np.rint(y_pred[i]) and y_true[i] == 0:
                true_negative += 1
            elif y_true[i] != np.rint(y_pred[i]) and y_true[i] == 1:
                false_negative += 1
            elif y_true[i] != np.rint(y_pred[i]) and y_true[i] == 0:
                false_positive += 1
        return true_positive, true_negative, false_positive, false_negative
