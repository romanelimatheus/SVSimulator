from app.sv.model import SVModel
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QWidget


class SVFormView(QDialog):
    def __init__(self: "SVFormView", item: SVModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.item: SVModel = item
        self.setup_ui()

    def setup_ui(self: "SVFormView") -> None:
        self.setWindowTitle("SV Form")
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.button_box)
        self.setLayout(layout)

