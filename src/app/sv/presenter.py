from app.sv.form.presenter import SVFormPresenter
from app.sv.form.view import SVFormView
from app.sv.model import SVModel
from app.sv.view import SVView
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QDialog, QTableWidgetItem


class SVPresenter(QObject):
    def __init__(self: "SVPresenter", view: SVView) -> None:
        super().__init__()
        self.items: list[SVModel] = []

        self.current_item: SVModel | None = None
        self.current_row = 0
        self.view = view

        self.view.delete_button.clicked.connect(self.delete_button_clicked)
        self.view.edit_button.clicked.connect(self.edit_button_clicked)
        self.view.add_button.clicked.connect(self.add_button_clicked)
        self.view.sv_table.itemClicked.connect(self.sv_table_item_clicked)

    def delete_button_clicked(self: "SVPresenter") -> None:
        if self.current_item is not None:
            self.items.remove(self.current_item)
            self.view.sv_table.removeRow(self.current_row)
            self.current_item = None

    def edit_button_clicked(self: "SVPresenter") -> None:
        if self.current_item is not None:
            model = self.current_item
            presenter = SVFormPresenter(model=model, view=SVFormView(parent=self.view))
            result = presenter.view.exec()
            if result == QDialog.DialogCode.Accepted:
                self.current_item = model
                self.update_row(self.current_row, model)

    def add_button_clicked(self: "SVPresenter") -> None:
        model = SVModel.default()
        presenter = SVFormPresenter(model=model, view=SVFormView(parent=self.view))
        result = presenter.view.exec()
        if result == QDialog.DialogCode.Accepted:
            self.add_item(model)

    def sv_table_item_clicked(self: "SVPresenter", item: QTableWidgetItem) -> None:
        self.current_item = self.items[item.row()]
        self.current_row = item.row()

    def add_item(self: "SVPresenter", item: SVModel) -> None:
        self.items.append(item)
        row_count = self.view.sv_table.rowCount()
        self.view.sv_table.insertRow(row_count)
        self.update_row(row_count, item)

    def update_row(self: "SVPresenter", row: int, item: SVModel) -> None:
        self.view.sv_table.setItem(row, 0, QTableWidgetItem(item.dst_mac))
        self.view.sv_table.setItem(row, 1, QTableWidgetItem(item.src_mac))
        self.view.sv_table.setItem(row, 2, QTableWidgetItem(item.app_id))
        self.view.sv_table.setItem(row, 3, QTableWidgetItem(item.sv_id))
        self.view.sv_table.setItem(row, 4, QTableWidgetItem(item.conf_rev))
        self.view.sv_table.setItem(row, 5, QTableWidgetItem(item.smp_synch))
