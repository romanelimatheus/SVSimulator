from dataclasses import dataclass
from pathlib import Path

import pysv.c_package as c_pub
from app.sv.model import SVModel
from pysv.sv import SamplesSynchronized, SVConfig


@dataclass
class Fuzzer:
    def start(self: "Fuzzer", iface: str, sv_list: list[SVModel]) -> None:
        print("Fuzzing interface", iface)
        print("SV list", sv_list)
        sv=sv_list[0]
        config = SVConfig(
            dst_mac=sv.dst_mac,
            src_mac=sv.src_mac,
            app_id=sv.app_id,
            sv_id=sv.sv_id,
            conf_rev=int(sv.conf_rev),
            smp_sync=SamplesSynchronized(int(sv.smp_synch)),
        )

        c_pub.publisher_default(iface, Path("data/default_phs_meas.csv"), config)

