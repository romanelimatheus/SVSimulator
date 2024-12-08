import decimal
from dataclasses import dataclass
from logging import getLogger
from multiprocessing import Process
from pathlib import Path
from random import randint
from struct import pack
from typing import TYPE_CHECKING

from app.sv.model import SVModel
from pysn1.triplet import Triplet
from pysv.c_package import _publisher, _send_default_sv, c_pub
from pysv.sv import SamplesSynchronized, SVConfig, parse_neutral, parse_sample, read_sample
from utils.threaded import threaded

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = getLogger(__name__)


@dataclass
class Fuzzer:
    process: Process | None = None

    def sender(self: "Fuzzer", iface: str, sv_list: list[SVModel]) -> None:
        threads = [self.send(iface, sv) for sv in sv_list]
        for thread in threads:
            thread.join()

    @threaded
    def start(self: "Fuzzer", iface: str, sv_list: list[SVModel]) -> None:
        if self.process is not None:
            self.stop()
            return
        logger.info("Starting fuzzer...")
        self.process = Process(target=self.sender, args=(iface, sv_list))
        self.process.start()
        self.process.join()
        self.stop()

    def stop(self: "Fuzzer") -> None:
        if self.process is None:
            return
        logger.info("Stopping fuzzer...")
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
        self.publisher_default(iface, config)

    def mutate_config(
        self: "Fuzzer", config: SVConfig, mutation_rating: int = 5, mutation_field: int = 20,
    ) -> SVConfig:
        if mutation_rating not in range(1,101,1):
            msg = "mutation_rating must be between 1 and 100"
            raise ValueError(msg)
        new_config = SVConfig(**config.__dict__) # copy config
        if randint(0, 100) <= mutation_rating:
        # Chance to mutate packet
            if randint(0, 100) <= mutation_field:
                new_config.dst_mac = str(randint(0, 0xffffffffffff))
            if randint(0, 100) <= mutation_field:
                new_config.src_mac = str(randint(0, 0xffffffffffff))
            if randint(0, 100) <= mutation_field:
                new_config.app_id = str(hex(randint(0, 0x9fff))[2:])
            if randint(0, 100) <= mutation_field:
                new_config.sv_id = config.sv_id + "_mutated"
            if randint(0, 100) <= mutation_field:
                new_config.conf_rev = randint(0, 0xffff)
            if randint(0, 100) <= mutation_field:
                new_config.smp_sync = SamplesSynchronized(randint(0, 2))
        return new_config

    def generate_mutated_sv(
        self: "Fuzzer",
        sv_config: SVConfig,
        path: Path,
        mutation_rating: int = 50,
        mutation_field: int = 20,
        frequency:int = 4000,
    ) -> "Iterator[tuple[int, int, bytes]]":

        no_asdu = b"\x80\x01\x01"

        previous_sleep_time = decimal.Decimal(0)
        for index, (sleep_time, i_as, i_bs, i_cs, v_as, v_bs, v_cs) in enumerate(read_sample(path)):
            new_config = self.mutate_config(sv_config, mutation_rating, mutation_field)
            dst_mac = new_config.dst_mac_bytes
            src_mac = new_config.src_mac_bytes
            ether_type = b"\x88\xba"
            header = dst_mac + src_mac + ether_type

            app_id = new_config.app_id_bytes
            reserved1 = b"\x00\x00"
            reserved2 = b"\x00\x00"

            sv_id = new_config.sv_id_bytes
            conf_rev = new_config.conf_rev_bytes
            smp_sync = new_config.smp_sync_bytes
            current_sleep_time = decimal.Decimal(sleep_time)
            time2sleep = current_sleep_time - previous_sleep_time
            previous_sleep_time = current_sleep_time

            i_ai, i_a = parse_sample(i_as)
            i_bi, i_b = parse_sample(i_bs)
            i_ci, i_c = parse_sample(i_cs)
            i_n = parse_neutral(i_ai + i_bi + i_ci)

            v_ai, v_a = parse_sample(v_as)
            v_bi, v_b = parse_sample(v_bs)
            v_ci, v_c = parse_sample(v_cs)
            v_n = parse_neutral(v_ai + v_bi + v_ci)

            smp_cnt_int = int(index % frequency)
            smp_cnt = bytes(Triplet.build(tag=0x82, value=pack("!H", smp_cnt_int)))
            phs_meas = bytes(Triplet.build(tag=0x87, value=i_a + i_b + i_c + i_n + v_a + v_b + v_c + v_n))
            asdu_fields = [sv_id, smp_cnt, conf_rev, smp_sync]
            asdu_header = b"".join(field for field in asdu_fields if randint(0, 100) <= mutation_field)
            asdu = bytes(Triplet.build(tag=0x30, value=asdu_header + phs_meas))

            seq_asdu = bytes(Triplet.build(tag=0xa2, value=asdu))
            sav_pdu = bytes(Triplet.build(tag=0x60, value=no_asdu + seq_asdu))

            length = pack("!H", len(sav_pdu) + 8)
            sv = app_id + length + reserved1 + reserved2 + sav_pdu

            yield int(time2sleep), smp_cnt_int, header + sv

    def publisher_default(self: "Fuzzer", iface: str, config: SVConfig) -> None:
        socket_num, interface_index = _publisher(iface)
        logger.info("Sending SV frames...")
        for time2sleep, _, sv in self.generate_mutated_sv(config, Path("data/default_phs_meas.csv")):
            _send_default_sv(socket_num, interface_index, c_pub.send_sv, sv, 1, len(sv), time2sleep)
        c_pub.close_socket(socket_num)
