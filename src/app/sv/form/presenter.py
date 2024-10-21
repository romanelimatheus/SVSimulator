from app.sv.form.view import SVFormView
from app.sv.model import SVFields, SVModel
from PyQt6.QtCore import QObject, pyqtSignal


class SVFormPresenter(QObject):
    submit_signal = pyqtSignal(SVModel)

    def __init__(self: "SVFormPresenter", model: SVModel, view: SVFormView) -> None:
        super().__init__()
        self.model = model
        self.view = view

        self.view.button_box.accepted.connect(self.submit)
        self.view.button_box.rejected.connect(self.view.reject)

        self.view.dst_mac.textChanged.connect(lambda: self.on_field_changed(SVFields.DST_MAC, self.view.dst_mac.text()))
        self.view.src_mac.textChanged.connect(lambda: self.on_field_changed(SVFields.SRC_MAC, self.view.src_mac.text()))
        self.view.vlan_id.textChanged.connect(lambda: self.on_field_changed(SVFields.VLAN_ID, self.view.vlan_id.text()))
        self.view.vlan_priority.textChanged.connect(
            lambda: self.on_field_changed(SVFields.VLAN_PRIORITY, self.view.vlan_priority.text()),
        )
        self.view.app_id.textChanged.connect(lambda: self.on_field_changed(SVFields.APP_ID, self.view.app_id.text()))
        self.view.simulation.stateChanged.connect(
            lambda: self.on_field_changed(SVFields.SIMULATION, str(self.view.simulation.isChecked())),
        )
        self.view.sv_id.textChanged.connect(lambda: self.on_field_changed(SVFields.SV_ID, self.view.sv_id.text()))
        self.view.conf_rev.textChanged.connect(
            lambda: self.on_field_changed(SVFields.CONF_REV, self.view.conf_rev.text()),
        )
        self.view.smp_synch.currentTextChanged.connect(
            lambda: self.on_field_changed(SVFields.SMP_SYNCH, self.view.smp_synch.currentText()),
        )
        self.view.dataset.textChanged.connect(
            lambda: self.on_field_changed(SVFields.DATASET, self.view.dataset.text()),
        )
        self.view.smp_rate.textChanged.connect(
            lambda: self.on_field_changed(SVFields.SMP_RATE, self.view.smp_rate.text()),
        )
        self.view.smp_mode.currentTextChanged.connect(
            lambda: self.on_field_changed(SVFields.SMP_MODE, self.view.smp_mode.currentText()),
        )


    def submit(self: "SVFormPresenter") -> None:
        self.view.accept()
        self.submit_signal.emit(self.model)

    def on_field_changed(self: "SVFormPresenter", field: SVFields, value: str | bool) -> None:
        self.model.__setattr__(field.value, value)
