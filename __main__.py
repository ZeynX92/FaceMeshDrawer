import sys
from main_window import FaceMeshForm
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FaceMeshForm()
    ex.show()
    sys.exit(app.exec())
