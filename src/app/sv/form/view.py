from app.sv.model import SVFields
from PyQt6.QtCore import Qt, pyqtSignal
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
    submit_signal = pyqtSignal()
    field_changed_signal = pyqtSignal(SVFields, str)

    def __init__(self: "SVFormView", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setup_ui()
        self.dst_mac.textChanged.connect(lambda: self.on_field_changed(SVFields.DST_MAC, self.dst_mac.text()))
        self.src_mac.textChanged.connect(lambda: self.on_field_changed(SVFields.SRC_MAC, self.src_mac.text()))
        self.vlan_id.textChanged.connect(lambda: self.on_field_changed(SVFields.VLAN_ID, self.vlan_id.text()))
        self.vlan_priority.textChanged.connect(
            lambda: self.on_field_changed(SVFields.VLAN_PRIORITY, self.vlan_priority.text()),
        )
        self.app_id.textChanged.connect(lambda: self.on_field_changed(SVFields.APP_ID, self.app_id.text()))
        self.simulation.stateChanged.connect(
            lambda: self.on_field_changed(SVFields.SIMULATION, str(self.simulation.isChecked())),
        )
        self.sv_id.textChanged.connect(lambda: self.on_field_changed(SVFields.SV_ID, self.sv_id.text()))
        self.conf_rev.textChanged.connect(lambda: self.on_field_changed(SVFields.CONF_REV, self.conf_rev.text()))
        self.smp_synch.currentTextChanged.connect(
            lambda: self.on_field_changed(SVFields.SMP_SYNCH, self.smp_synch.currentText()),
        )
        self.dataset.textChanged.connect(lambda: self.on_field_changed(SVFields.DATASET, self.dataset.text()))
        self.smp_rate.textChanged.connect(lambda: self.on_field_changed(SVFields.SMP_RATE, self.smp_rate.text()))
        self.smp_mode.currentTextChanged.connect(
            lambda: self.on_field_changed(SVFields.SMP_MODE, self.smp_mode.currentText()),
        )

    def submit(self: "SVFormView") -> None:
        self.submit_signal.emit()
        self.accept()

    def on_field_changed(self: "SVFormView", field: SVFields, value: str | bool) -> None:
        self.field_changed_signal.emit(field, value)

    def setup_ui(self: "SVFormView") -> None:
        self.setWindowTitle("SV Form")
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.submit)
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
        self.dst_mac = QLineEdit()
        self.dst_mac.setInputMask("HH:HH:HH:HH:HH:HH")
        eth_form_layout.addRow("Destination MAC:", self.dst_mac)
        self.src_mac = QLineEdit()
        self.src_mac.setInputMask("HH:HH:HH:HH:HH:HH")
        eth_form_layout.addRow("Source MAC:", self.src_mac)
        eth_form.setLayout(eth_form_layout)
        return eth_form

    def setup_vlan_form(self: "SVFormView") -> QGroupBox:
        vlan_form = QGroupBox("VLAN", checkable=True)
        vlan_form_layout = QFormLayout()
        self.vlan_id = QLineEdit()
        self.vlan_id.setInputMask("0000")
        vlan_form_layout.addRow("VLAN ID:", self.vlan_id)
        self.vlan_priority = QLineEdit()
        self.vlan_priority.setInputMask("00")
        vlan_form_layout.addRow("VLAN Priority:", self.vlan_priority)
        vlan_form.setLayout(vlan_form_layout)
        return vlan_form

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

        sv_form_optional = QGroupBox("Optional fields", checkable=True)
        sv_form_optional_layout = QFormLayout()
        self.dataset = QLineEdit()
        sv_form_optional_layout.addRow("Dataset:", self.dataset)
        self.smp_rate = QLineEdit()
        self.smp_rate.setValidator(QIntValidator(0, 65535))
        sv_form_optional_layout.addRow("SmpRate:", self.smp_rate)
        self.smp_mode = QComboBox()
        self.smp_mode.addItems(["0", "1", "2"])
        sv_form_optional_layout.addRow("SmpMode:", self.smp_mode)
        sv_form_optional.setLayout(sv_form_optional_layout)

        sv_form = QGroupBox("SV PDU")
        sv_form_layout = QVBoxLayout()
        sv_form_layout.addWidget(sv_form_must)
        sv_form_layout.addWidget(sv_form_optional)
        sv_form.setLayout(sv_form_layout)
        return sv_form
