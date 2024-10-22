from app.sv.model import SVModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
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

        layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.fields_layout())
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        layout.addWidget(scroll_area)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def setup_model(self: "SVFormView", model: SVModel) -> None:
        self.dst_mac.setText(model.dst_mac)
        self.src_mac.setText(model.src_mac)
        self.vlan_form.setChecked(bool(model.vlan_enabled))
        self.vlan_id.setText(model.vlan_id)
        self.vlan_priority.setText(model.vlan_priority)
        self.app_id.setText(model.app_id)
        self.simulation.setChecked(bool(model.simulation))
        self.sv_id.setText(model.sv_id)
        self.conf_rev.setText(str(model.conf_rev))
        self.smp_synch.setCurrentText(str(model.smp_synch))
        self.dataset_enabled.setChecked(bool(model.dataset_enabled))
        self.dataset.setText(model.dataset)
        self.smp_rate_enabled.setChecked(bool(model.smp_rate_enabled))
        self.smp_rate.setText(str(model.smp_rate))
        self.smp_mode_enabled.setChecked(bool(model.smp_mode_enabled))
        self.smp_mode.setCurrentText(str(model.smp_mode))

    def fields_layout(self: "SVFormView") -> QWidget:
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
        self.dst_mac = QLineEdit()
        self.dst_mac.setInputMask("HH:HH:HH:HH:HH:HH")
        eth_form_layout.addRow("Destination MAC:", self.dst_mac)
        self.src_mac = QLineEdit()
        self.src_mac.setInputMask("HH:HH:HH:HH:HH:HH")
        eth_form_layout.addRow("Source MAC:", self.src_mac)
        eth_form.setLayout(eth_form_layout)
        return eth_form

    def setup_vlan_form(self: "SVFormView") -> QGroupBox:
        self.vlan_form = QGroupBox("VLAN")
        self.vlan_form.setCheckable(True)
        vlan_form_layout = QFormLayout()
        self.vlan_id = QLineEdit()
        self.vlan_id.setInputMask("0000")
        vlan_form_layout.addRow("VLAN ID:", self.vlan_id)
        self.vlan_priority = QLineEdit()
        self.vlan_priority.setInputMask("00")
        vlan_form_layout.addRow("VLAN Priority:", self.vlan_priority)
        self.vlan_form.setLayout(vlan_form_layout)
        return self.vlan_form

    def setup_sv_header_form(self: "SVFormView") -> QGroupBox:
        sv_form = QGroupBox("SV Header")
        sv_form_layout = QFormLayout()
        self.app_id = QLineEdit()
        self.app_id.setInputMask("HHHH")
        sv_form_layout.addRow("APP_ID:", self.app_id)
        self.simulation = QCheckBox()
        sv_form_layout.addRow("Simulation:", self.simulation)
        sv_form.setLayout(sv_form_layout)
        return sv_form

    def setup_sv_pdu_form(self: "SVFormView") -> QGroupBox:
        sv_form_must = QGroupBox("ASDU fields")
        sv_form_must_layout = QFormLayout()
        self.sv_id = QLineEdit()
        sv_form_must_layout.addRow("svID", self.sv_id)
        self.conf_rev = QLineEdit()
        sv_form_must_layout.addRow("ConfRev:", self.conf_rev)
        self.smp_synch = QComboBox()
        self.smp_synch.addItems(["0", "1", "2"])
        sv_form_must_layout.addRow("SmpSynch:", self.smp_synch)
        sv_form_must.setLayout(sv_form_must_layout)

        sv_form_optional = QGroupBox("Optional fields")

        dataset_layout = QHBoxLayout()
        dataset_label = QLabel("Dataset:")
        self.dataset_enabled = QCheckBox()
        self.dataset_enabled.setChecked(True)
        self.dataset = QLineEdit()
        dataset_layout.addWidget(self.dataset_enabled)
        dataset_layout.addWidget(dataset_label)
        dataset_layout.addWidget(self.dataset)
        self.dataset_enabled.toggled.connect(lambda: self.dataset.setEnabled(self.dataset_enabled.isChecked()))
        smp_rate_layout = QHBoxLayout()
        smp_rate_label = QLabel("SmpRate:")
        self.smp_rate = QLineEdit()
        self.smp_rate_enabled = QCheckBox()
        self.smp_rate_enabled.setChecked(True)
        self.smp_rate.setValidator(QIntValidator(0, 65535))
        smp_rate_layout.addWidget(self.smp_rate_enabled)
        smp_rate_layout.addWidget(smp_rate_label)
        smp_rate_layout.addWidget(self.smp_rate)
        self.smp_rate_enabled.toggled.connect(lambda: self.smp_rate.setEnabled(self.smp_rate_enabled.isChecked()))

        smp_mode_layout = QHBoxLayout()
        smp_mode_label = QLabel("SmpMode:")
        self.smp_mode = QComboBox()
        self.smp_mode.addItems(["0", "1", "2"])
        self.smp_mode_enabled = QCheckBox()
        self.smp_mode_enabled.setChecked(True)
        smp_mode_layout.addWidget(self.smp_mode_enabled)
        smp_mode_layout.addWidget(smp_mode_label)
        smp_mode_layout.addWidget(self.smp_mode)
        self.smp_mode_enabled.toggled.connect(lambda: self.smp_mode.setEnabled(self.smp_mode_enabled.isChecked()))
        sv_form_optional_layout = QVBoxLayout()
        sv_form_optional_layout.addLayout(dataset_layout)
        sv_form_optional_layout.addLayout(smp_rate_layout)
        sv_form_optional_layout.addLayout(smp_mode_layout)
        sv_form_optional.setLayout(sv_form_optional_layout)

        sv_form = QGroupBox("SV PDU")
        sv_form_layout = QVBoxLayout()
        sv_form_layout.addWidget(sv_form_must)
        sv_form_layout.addWidget(sv_form_optional)
        sv_form.setLayout(sv_form_layout)
        return sv_form
