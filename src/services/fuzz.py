from dataclasses import dataclass

from app.sv.model import SVModel


@dataclass
class Fuzzer:
    def start(self: "Fuzzer", iface: str, sv_list: list[SVModel]) -> None:
        print("Fuzzing interface", iface)
        print("SV list", sv_list)
