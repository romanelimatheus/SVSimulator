from dataclasses import dataclass

from PyQt6.QtWidgets import QTableWidgetItem


@dataclass
class ASDUModel:
    sv_id: str
    conf_rev: int
    smp_synch: int

    dataset: str | None = None
    smp_rate: int | None = None
    smp_mode: int | None = None

    @classmethod
    def default(cls: type["ASDUModel"]) -> "ASDUModel":
        return ASDUModel(sv_id="xxxx", conf_rev=0, smp_synch=0)


@dataclass
class SVModel(QTableWidgetItem):
    app_id: str
    simulation: bool
    asdu: list[ASDUModel]

    @property
    def no_asdu(self: "SVModel") -> int:
        return len(self.asdu)

    @classmethod
    def default(cls: type["SVModel"]) -> "SVModel":
        return cls(app_id="xxxx", simulation=False, asdu=[ASDUModel.default()])
