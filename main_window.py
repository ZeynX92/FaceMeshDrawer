import cv2
from PyQt6.QtCore import Qt
from PyQt6 import uic, QtGui
from PyQt6.QtGui import QPixmap
from face_mesh_tools import FaceMeshProcessor, FaceNotFoundError
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox


class FaceMeshForm(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cur_img = None
        uic.loadUi('ui/main.ui', self)

        self.load_button.clicked.connect(self.process)
        self.save_button.clicked.connect(self.save)

        self.processor = FaceMeshProcessor('models/face_landmarker.task')

    def process(self):
        cur_img_path = QFileDialog.getOpenFileName(self, "Выберите изображение", '/home', "Фотографии *.png *.jpg")[0]
        print(cur_img_path)

        if not cur_img_path:
            return

        try:
            self.cur_img = self.processor.process_image(cur_img_path)
        except FaceNotFoundError:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("На фотографии не обнаружено лиц")
            msg.setWindowTitle("Ошибка распознавания!")
            msg.exec()
            return

        height, width, channels = self.cur_img.shape
        bytes_per_line = channels * width
        qt_img = QtGui.QImage(self.cur_img.data, width, height, bytes_per_line,
                              QtGui.QImage.Format.Format_RGB888).scaled(height, width,
                                                                        Qt.AspectRatioMode.KeepAspectRatio)
        self.label.setPixmap(QPixmap.fromImage(qt_img))

    def save(self):
        if self.cur_img is not None:
            path = QFileDialog.getSaveFileName(self, "Сохраните результат", "/home/untitled.png",
                                               "Фотография (*.png *.jpg)")[0]
            if path:
                cv2.imwrite(path, cv2.cvtColor(self.cur_img, cv2.COLOR_RGB2BGR))
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Вы не обработали ни одной фотографии")
            msg.setWindowTitle("Рабочее пространство пусто!")
            msg.exec()
            return
