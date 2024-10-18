from app.sv.form_dialog import SVFormView
from app.sv.model import SVModel
from app.sv.view import SVView


class SVPresenter:
    def __init__(self: "SVPresenter", model: type[SVModel], view: SVView) -> None:
        self.model = model
        self.view = view
        self.view.form_data_collected.connect(self.form_dialog)

    def form_dialog(self: "SVPresenter", item: SVModel) -> None:
        SVFormView(item=item, parent=self.view).exec()
