from socket import if_nameindex

from app.sv import SVModel, SVPresenter, SVView
from PyQt6.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from services import Fuzzer


class MainWindow(QDialog):
    def __init__(self: "MainWindow") -> None:
        super().__init__()
        self.fuzzer = Fuzzer()
        self.setWindowTitle("SV Simulator")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    @property
    def iface(self: "MainWindow") -> str:
        return self.interface_input.currentText()

    def start(self: "MainWindow") -> None:
        self.fuzzer.start(self.iface)

    def setup_ui(self: "MainWindow") -> None:
        self.interface_input = QComboBox()
        for _, name in if_nameindex():
            self.interface_input.addItem(name)

        self.start_stop_button = QPushButton("Start/Stop")
        self.start_stop_button.clicked.connect(self.start)

        form = QHBoxLayout()
        form.addWidget(QLabel("Interface:"))
        form.addWidget(self.interface_input, stretch=1)
        form.addWidget(self.start_stop_button)

        self.sv_view = SVView()
        self.sv_presenter = SVPresenter(SVModel, self.sv_view)
        self.sv_view.show()

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.sv_view)

        self.setLayout(layout)
