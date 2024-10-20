from app.sv import SVModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class SVFormView(QDialog):
    def __init__(self: "SVFormView", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self: "SVFormView") -> None:
        self.setWindowTitle("SV Form")
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.fields_layout())
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        layout.addWidget(scroll_area)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def fields_layout(self: "SVFormView") -> QVBoxLayout:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.setup_eth_form())
        layout.addWidget(self.setup_vlan_form())
        layout.addWidget(self.setup_sv_header_form())
        layout.addWidget(self.setup_sv_pdu_form())
        widget.setLayout(layout)
        return widget

    def setup_eth_form(self: "SVFormView") -> QGroupBox:
        eth_form = QGroupBox("Ethernet")
        eth_form_layout = QFormLayout()
        dst_mac = QLineEdit()
        dst_mac.setInputMask("HH:HH:HH:HH:HH:HH")
        eth_form_layout.addRow("Destination MAC:", dst_mac)
        src_mac = QLineEdit()
        src_mac.setInputMask("HH:HH:HH:HH:HH:HH")
        eth_form_layout.addRow("Source MAC:", src_mac)
        eth_form.setLayout(eth_form_layout)
        return eth_form

    def setup_vlan_form(self: "SVFormView") -> QGroupBox:
        vlan_form = QGroupBox("VLAN", checkable=True)
        vlan_form_layout = QFormLayout()
        vlan_id = QLineEdit()
        vlan_id.setInputMask("0000")
        vlan_form_layout.addRow("VLAN ID:", vlan_id)
        vlan_priority = QLineEdit()
        vlan_priority.setInputMask("00")
        vlan_form_layout.addRow("VLAN Priority:", vlan_priority)
        vlan_form.setLayout(vlan_form_layout)
        return vlan_form

    def setup_sv_header_form(self: "SVFormView") -> QGroupBox:
        sv_form = QGroupBox("SV Header")
        sv_form_layout = QFormLayout()
        app_id = QLineEdit()
        app_id.setInputMask("HHHH")
        sv_form_layout.addRow("APP_ID:", app_id)
        sv_form_layout.addRow("Simulation:", QCheckBox())
        sv_form.setLayout(sv_form_layout)
        return sv_form

    def setup_sv_pdu_form(self: "SVFormView") -> QGroupBox:
        sv_form_must = QGroupBox("ASDU fields")
        sv_form_must_layout = QFormLayout()
        sv_form_must_layout.addRow("svID", QLineEdit())
        sv_form_must_layout.addRow("ConfRev:", QLineEdit())
        smp_synch = QComboBox()
        smp_synch.addItems(["0", "1", "2"])
        sv_form_must_layout.addRow("SmpSynch:", smp_synch)
        sv_form_must.setLayout(sv_form_must_layout)

        sv_form_optional = QGroupBox("Optional fields", checkable=True)
        sv_form_optional_layout = QFormLayout()
        sv_form_optional_layout.addRow("Dataset:", QLineEdit())
        smp_rate = QLineEdit()
        smp_rate.setValidator(QIntValidator(0, 65535))
        sv_form_optional_layout.addRow("SmpRate:", smp_rate)
        smp_mode = QComboBox()
        smp_mode.addItems(["0", "1", "2"])
        sv_form_optional_layout.addRow("SmpMode:", smp_mode)
        sv_form_optional.setLayout(sv_form_optional_layout)

        sv_form = QGroupBox("SV PDU")
        sv_form_layout = QVBoxLayout()
        sv_form_layout.addWidget(sv_form_must)
        sv_form_layout.addWidget(sv_form_optional)
        sv_form.setLayout(sv_form_layout)
        return sv_form
