from dataclasses import dataclass


@dataclass
class Fuzzer:
    def start(self: "Fuzzer", iface: str) -> None:
        print("Fuzzing interface", iface)
