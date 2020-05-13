class configuration:
    def __init__(self, training_images_path, training_labels_path, validation_images_path, validation_labels_path):
        self.training_images_path = training_images_path
        self.training_labels_path = training_labels_path
        self.validation_images_path = validation_images_path
        self.validation_labels_path = validation_labels_path

    def print(self):
        print(self.__dict__)


