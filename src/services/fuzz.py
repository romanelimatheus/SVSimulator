from dataclasses import dataclass
from multiprocessing import Process
from pathlib import Path

import pysv.c_package as c_pub
from app.sv.model import SVModel
from pysv.sv import SamplesSynchronized, SVConfig
from utils.threaded import threaded


@dataclass
class Fuzzer:
    process: Process | None = None

    def sender(self: "Fuzzer", iface: str, sv_list: list[SVModel]) -> None:
        for sv in sv_list:
            t = self.send(iface, sv)
            t.join()

    @threaded
    def start(self: "Fuzzer", iface: str, sv_list: list[SVModel]) -> None:
        if self.process is not None:
            self.stop()
            return
        self.process = Process(target=self.sender, args=(iface, sv_list))
        self.process.start()
        self.process.join()
        self.stop()

    def stop(self: "Fuzzer") -> None:
        if self.process is None:
            return
        self.process.terminate()
        self.process = None

    @threaded
    def send(self: "Fuzzer", iface: str, sv: SVModel) -> None:
        config = SVConfig(
            dst_mac=sv.dst_mac,
            src_mac=sv.src_mac,
            app_id=sv.app_id,
            sv_id=sv.sv_id,
            conf_rev=int(sv.conf_rev),
            smp_sync=SamplesSynchronized(int(sv.smp_synch)),
        )

        c_pub.publisher_default(iface, Path("data/default_phs_meas.csv"), config)
