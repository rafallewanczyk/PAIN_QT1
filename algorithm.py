import gzip
import numpy as np
import time
import matplotlib.pyplot as plt


class Data:
    IMAGE_SIZE = 28
    error = ""

    def __init__(self, train_images_path, train_labels_path, validation_images_path, validation_labels_path):

        if train_images_path[-3:] == '.gz':
            self.train_images= gzip.open(train_images_path, "r")
            if int.from_bytes(self.train_images.read(4), 'big') == 2051:
                self.train_images.read(12);
                self.X = self.generate_matrices(self.train_images.read(), self.IMAGE_SIZE)
            else:
                self.error += "Zbiór treningowy obrazów - niepoprwany header plikui\n"
        else:
            self.error += "Zbiór treningowy obrazów - niepoprawne rozszerzenie pliku\n"

        if train_labels_path[-3:] == '.gz':
            self.train_labels= gzip.open(train_labels_path, "r")
            if int.from_bytes(self.train_labels.read(4), 'big') == 2049:
                self.train_labels.read(4);
                self.y = self.generate_matrices(self.train_labels.read(), 1)
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
                self.v_y = self.generate_matrices(self.validation_labels.read(), 1)
            else:
                self.error += "Zbiór walidacyjny etykiet- niepoprwany header plikui\n"
        else:
            self.error += "Zbiór walidacyjny etykiet- niepoprawne rozszerzenie pliku\n"


        if(self.error == ""):
            if self.X.shape[0] != self.y.shape[0]:
               self.error += "Dane treningowe - niezgodne wymiary tablic\n"
            if self.v_X.shape[0] != self.v_y.shape[0]:
                self.error += "Dane walidacyjne- niezgodne wymiary tablic\n"

        if self.error == "":
            print("poprawnie wczytano dane")
            #todo clear data

    def getSizes(self):
        return self.X.shape[0], self.v_X.shape[0]

    def is_prime(self, x):
        if x in [2, 3, 5, 7]:
            return 1
        elif x in [4, 6, 8]:
            return 0
        return -1

    # is_prime = np.vectorize(is_prime)

    def generate_matrices(self, buffer, length):
        M = np.frombuffer(buffer, dtype=np.uint8)
        M = M.reshape(int(M.shape[0] / (length ** 2)), -1)

        return M

    def generate(self):
        print(self.y)
#
# def generate_map(labels):
#     map = np.argwhere(labels == -1)
#     return map.T[0]
#
#
# X = generate_matrices(train_image.read(), IMAGE_SIZE)
# y = is_prime(generate_matrices(train_labels.read(), 1))
# map = generate_map(y)
#
# X = np.delete(X, map, 0)
# y = np.delete(y, map, 0)
#
#
#
# v_X = generate_matrices(validation_image.read(), IMAGE_SIZE)
# v_y = is_prime(generate_matrices(validation_labels.read(), 1))
# map = generate_map(v_y)
#
# v_X = np.delete(v_X, map, 0)
# v_y = np.delete(v_y, map, 0)
#
# print(X.shape)
# print(y.shape)
