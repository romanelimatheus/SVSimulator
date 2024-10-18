import sys

from PyQt6.QtWidgets import QApplication

from src.app.ui.main_window import MainWindow

app = QApplication(sys.argv)
view = MainWindow()
view.show()
app.exec()
