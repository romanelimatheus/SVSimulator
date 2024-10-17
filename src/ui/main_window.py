from PyQt6.QtWidgets import QDialog


class MainWindow(QDialog):
    def __init__(self: "MainWindow") -> None:
        super().__init__()
        self.setWindowTitle("SV Simulator")
        self.setGeometry(100, 100, 800, 600)

