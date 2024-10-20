from app.sv import SVModel
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QTableWidget, QVBoxLayout, QWidget


class SVView(QWidget):
    form_data_collected = pyqtSignal(SVModel)

    def __init__(self: "SVView") -> None:
        super().__init__()
        self.current_item = None
        self.setup_ui()

    def delete_button_clicked(self: "SVView") -> None:
        if self.current_item is not None:
            self.sv_table.removeRow(self.sv_table.row(self.current_item))

    def edit_button_clicked(self: "SVView") -> None:
        if self.current_item is not None:
            self.form_data_collected.emit(self.current_item)

    def add_button_clicked(self: "SVView") -> None:
        self.form_data_collected.emit(SVModel.default())

    def sv_table_item_clicked(self: "SVView", item: SVModel) -> None:
        self.current_item = item

    def setup_ui(self: "SVView") -> None:
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_button_clicked)
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_button_clicked)
        button_form = QHBoxLayout()
        button_form.addWidget(self.delete_button)
        button_form.addWidget(self.edit_button)
        button_form.addWidget(self.add_button)

        self.sv_table = QTableWidget()
        self.sv_table.itemClicked.connect(self.sv_table_item_clicked)
        self.sv_table.setColumnCount(5)
        self.sv_table.setHorizontalHeaderLabels(["Destination MAC", "Source MAC", "VLAN ID", "VLAN Priority", "APP_ID"])
        main_form = QVBoxLayout()
        main_form.addLayout(button_form)
        main_form.addWidget(self.sv_table)
        self.setLayout(main_form)
