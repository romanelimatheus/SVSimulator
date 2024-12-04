from dataclasses import dataclass
from enum import Enum


class SVFields(Enum):
    DST_MAC = "dst_mac"
    SRC_MAC = "src_mac"
    VLAN_ENABLED = "vlan_enabled"
    VLAN_ID = "vlan_id"
    VLAN_PRIORITY = "vlan_priority"
    APP_ID = "app_id"
    SIMULATION = "simulation"
    SV_ID = "sv_id"
    CONF_REV = "conf_rev"
    SMP_SYNCH = "smp_synch"
    DATASET = "dataset"
    DATASET_ENABLED = "dataset_enabled"
    SMP_RATE = "smp_rate"
    SMP_RATE_ENABLED = "smp_rate_enabled"
    SMP_MODE = "smp_mode"
    SMP_MODE_ENABLED = "smp_mode_enabled"

@dataclass
class SVModel:
    dst_mac: str
    src_mac: str

    app_id: str
    simulation: bool
    sv_id: str
    conf_rev: int
    smp_synch: int

    vlan_enabled: bool = False

    vlan_id: int | None = None
    vlan_priority: int | None = None

    dataset_enabled: bool = False
    dataset: str | None = None

    smp_rate_enabled: bool = False
    smp_rate: int | None = None

    smp_mode_enabled: bool = False
    smp_mode: int | None = None

    no_asdu: int = 1

    @classmethod
    def default(cls: type["SVModel"]) -> "SVModel":
        return cls(
            src_mac="ffffffffffff",
            dst_mac="ffffffffffff",
            app_id="4000",
            simulation=False,
            sv_id="asdf",
            conf_rev=0,
            smp_synch=0,
        )
