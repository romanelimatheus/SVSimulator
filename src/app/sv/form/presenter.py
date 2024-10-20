from app.sv.form.view import SVFormView
from app.sv.model import SVFields, SVModel
from PyQt6.QtCore import pyqtSignal


class SVFormPresenter:
    submit_signal = pyqtSignal(SVModel)

    def __init__(self: "SVFormPresenter", model: SVModel, view: SVFormView) -> None:
        self.model = model
        self.view = view
        self.view.submit_signal.connect(self.submit)
        self.view.field_changed_signal.connect(self.on_field_changed)

    def submit(self: "SVFormPresenter") -> None:
        self.submit_signal.emit(self.model)

    def on_field_changed(self: "SVFormPresenter", field: SVFields, value: str | bool) -> None:
        self.model.__setattr__(field.value, value)
        print(self.model.__dict__)
