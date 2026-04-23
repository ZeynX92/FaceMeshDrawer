import re
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMessageBox

pattern = re.compile(
    r'^(?:(?:1?\d{1,2}|2[0-4]\d|25[0-5])|0),'
    r'(?:(?:1?\d{1,2}|2[0-4]\d|25[0-5])|0),'
    r'(?:(?:1?\d{1,2}|2[0-4]\d|25[0-5])|0)$'
)


def is_valid_rgb(s):
    return bool(pattern.match(s))


class EditSettingsForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('ui/settings.ui', self)

        self.cancel_button.clicked.connect(self.cancel_process)
        self.save_button.clicked.connect(self.save_process)

        self.lineEdit_connections_thickness.setText(str(self.parent.settings["connections_thickness"]))
        self.lineEdit_contours_thickness.setText(str(self.parent.settings["contours_thickness"]))
        self.lineEdit_circle_radius.setText(str(self.parent.settings["circle_radius"]))
        self.lineEdit_landmark_color.setText(','.join([str(x) for x in self.parent.settings["landmark_color"]]))
        self.lineEdit_connection_color.setText(','.join([str(x) for x in self.parent.settings["connection_color"]]))
        self.lineEdit_contours_color.setText(','.join([str(x) for x in self.parent.settings["contours_color"]]))
        self.checkBox_draw_contours.setCheckState(
            Qt.CheckState.Checked if self.parent.settings["draw_contours"] else Qt.CheckState.Unchecked)
        self.checkBox_draw_landmarks.setCheckState(
            Qt.CheckState.Checked if self.parent.settings["draw_landmarks"] else Qt.CheckState.Unchecked)

    def cancel_process(self):
        self.parent.setEnabled(True)
        self.hide()

    def save_process(self):
        connections_thickness = self.lineEdit_connections_thickness.text()
        contours_thickness = self.lineEdit_contours_thickness.text()
        circle_radius = self.lineEdit_circle_radius.text()
        landmark_color = self.lineEdit_landmark_color.text()
        connection_color = self.lineEdit_connection_color.text()
        contours_color = self.lineEdit_contours_color.text()
        draw_contours = self.checkBox_draw_contours.checkState()
        draw_landmarks = self.checkBox_draw_landmarks.checkState()

        if not str(connections_thickness).isdigit() or not str(contours_thickness).isdigit() or not str(
                circle_radius).isdigit():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Неверный формат линейных размеров!")
            msg.setText("Как толщину линий или радиус меток можно ввести только целое число!")
            msg.exec()
            return

        if not is_valid_rgb(landmark_color) or not is_valid_rgb(connection_color) or not is_valid_rgb(contours_color):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Неверный формат цвета!")
            msg.setText("Укажите 3 числа от 0 до 255 через запятые в формате R,G,B!")
            msg.exec()
            return

        draw_contours = draw_contours == Qt.CheckState.Checked
        draw_landmarks = draw_landmarks == Qt.CheckState.Checked

        self.parent.settings = {"connections_thickness": int(connections_thickness),
                                "contours_thickness": int(contours_thickness), "circle_radius": int(circle_radius),
                                "landmark_color": tuple(map(int, landmark_color.split(','))),
                                "connection_color": tuple(map(int, connection_color.split(','))),
                                "contours_color": tuple(map(int, contours_color.split(','))),
                                "draw_contours": draw_contours,
                                "draw_landmarks": draw_landmarks}
        self.cancel_process()

    def closeEvent(self, event):
        self.cancel_process()
