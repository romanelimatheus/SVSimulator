from PyQt6.QtWidgets import QAbstractItemView, QHBoxLayout, QPushButton, QTableWidget, QVBoxLayout, QWidget


class SVView(QWidget):

    def __init__(self: "SVView") -> None:
        super().__init__()
        self.setup_ui()

    def setup_ui(self: "SVView") -> None:
        self.delete_button = QPushButton("Delete")
        self.edit_button = QPushButton("Edit")
        self.add_button = QPushButton("Add")
        button_form = QHBoxLayout()
        button_form.addWidget(self.delete_button)
        button_form.addWidget(self.edit_button)
        button_form.addWidget(self.add_button)

        self.sv_table = QTableWidget()
        self.sv_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.sv_table.setColumnCount(5)
        self.sv_table.setHorizontalHeaderLabels(["Destination MAC", "Source MAC", "VLAN ID", "VLAN Priority", "APP_ID"])

        main_form = QVBoxLayout()
        main_form.addLayout(button_form)
        main_form.addWidget(self.sv_table)
        self.setLayout(main_form)
