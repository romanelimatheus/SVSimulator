from app.sv.form.view import SVFormView
from app.sv.model import SVModel


class SVFormPresenter:
    def __init__(self: "SVFormPresenter", model: SVModel, view: SVFormView) -> None:
        self.model = model
        self.view = view
