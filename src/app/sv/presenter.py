from app.sv.form.presenter import SVFormPresenter
from app.sv.form.view import SVFormView
from app.sv.model import SVModel
from app.sv.view import SVView
from PyQt6.QtWidgets import QDialog


class SVPresenter:
    def __init__(self: "SVPresenter", view: SVView) -> None:
        self.items: list[SVModel] = []

        self.current_item: SVModel | None = None
        self.view = view

        self.view.delete_button.clicked.connect(self.delete_button_clicked)
        self.view.edit_button.clicked.connect(self.edit_button_clicked)
        self.view.add_button.clicked.connect(self.add_button_clicked)
        self.view.sv_table.itemClicked.connect(self.sv_table_item_clicked)
        self.view.form_data_collected.connect(self.form_dialog)

    def delete_button_clicked(self: "SVPresenter") -> None:
        if self.current_item is not None:
            self.items.remove(self.current_item)
            self.view.sv_table.removeRow(self.view.sv_table.row(self.current_item))
            self.current_item = None

    def edit_button_clicked(self: "SVPresenter") -> None:
        if self.current_item is not None:
            self.view.form_data_collected.emit(self.current_item)

    def add_button_clicked(self: "SVPresenter") -> None:
        self.view.form_data_collected.emit(SVModel.default())

    def sv_table_item_clicked(self: "SVPresenter", item: SVModel) -> None:
        print("CLICKED", item.__dict__)
        self.current_item = item

    def add_item(self: "SVPresenter", item: SVModel) -> None:
        self.items.append(item)
        self.view.sv_table.insertRow(self.view.sv_table.rowCount())

    def form_dialog(self: "SVPresenter", model: SVModel) -> None:
        presenter = SVFormPresenter(model=model, view=SVFormView(parent=self.view))
        result = presenter.view.exec()
        if result == QDialog.DialogCode.Accepted:
            self.add_item(model)
