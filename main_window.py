import cv2
from PyQt6.QtCore import Qt
from PyQt6 import uic, QtGui
from PyQt6.QtGui import QPixmap
from setings_form import EditSettingsForm
from face_mesh_tools import FaceMeshProcessor, FaceNotFoundError
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox


class FaceMeshForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)

        self.cur_img = None
        self.processor = FaceMeshProcessor('models/face_landmarker.task')

        self.edit_settings_form = None
        self.settings = {"connections_thickness": 1, "contours_thickness": 3,
                        "circle_radius": 1, "landmark_color": (0, 255, 0), "connection_color": (0, 255, 0),
                        "contours_color": (255, 255, 0), "draw_contours": False, "draw_landmarks": True}

        self.load_button.clicked.connect(self.process)
        self.save_button.clicked.connect(self.save)
        self.settings_button.clicked.connect(self.edit_settings)

    def edit_settings(self):
        self.edit_settings_form = EditSettingsForm(self)
        self.edit_settings_form.show()
        self.setEnabled(False)



    def process(self):
        cur_img_path = QFileDialog.getOpenFileName(self, "Выберите изображение", '/home', "Фотографии *.png *.jpg")[0]
        print(cur_img_path)

        if not cur_img_path:
            return

        try:
            self.cur_img = self.processor.process_image(cur_img_path, **self.settings)
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
