from app.sv.form.presenter import SVFormPresenter
from app.sv.form.view import SVFormView
from app.sv.model import SVModel
from app.sv.view import SVView


class SVPresenter:
    def __init__(self: "SVPresenter", model: type[SVModel], view: SVView) -> None:
        self.model = model
        self.view = view
        self.view.form_data_collected.connect(self.form_dialog)

    def form_dialog(self: "SVPresenter", model: SVModel) -> None:
        presenter = SVFormPresenter(model=model, view=SVFormView(parent=self.view))
        presenter.view.exec()

