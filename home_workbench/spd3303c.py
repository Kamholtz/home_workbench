# scpi controller
import time
from enum import Enum

import pyvisa


class SPD3303CChannels(Enum):
    CHANNEL_1 = 1
    CHANNEL_2 = 2
    CHANNEL_3 = 3


class SPD3303ChannelSupplyMode(Enum):
    CONSTANT_VOLTAGE = 0
    CONSTANT_CURRENT = 1


class SPD3303ChannelsMode(Enum):
    INDEPENDENT = 1
    PARALLEL = 2
    SERIES = 3


class SPD3303ChannelState(Enum):
    OFF = 0
    ON = 1


class SPD3303Status:
    channel_1_supply_mode: SPD3303ChannelSupplyMode
    channel_2_supply_mode: SPD3303ChannelSupplyMode
    channels_mode: SPD3303ChannelsMode
    channel_1_state: SPD3303ChannelState
    channel_2_state: SPD3303ChannelState

    CHANNEL_1_CV_CC_MASK = 0x01
    CHANNEL_2_CV_CC_MASK = 0x02
    CHANNELS_MODE_MASK = 0x0C
    CHANNEL_1_STATE_MASK = 0x10
    CHANNEL_2_STATE_MASK = 0x20

    def __init__(self, hex_status: str):
        int_status = int(hex_status, 16)
        ch_1_supply_mode_bits = (int_status & SPD3303Status.CHANNEL_1_CV_CC_MASK) >> 0
        self.channel_1_supply_mode = SPD3303ChannelSupplyMode(ch_1_supply_mode_bits)
        ch_2_supply_mode_bits = (int_status & SPD3303Status.CHANNEL_2_CV_CC_MASK) >> 1
        self.channel_2_supply_mode = SPD3303ChannelSupplyMode(ch_2_supply_mode_bits)

        chs_mode = (int_status & SPD3303Status.CHANNELS_MODE_MASK) >> 2
        self.channels_mode = SPD3303ChannelsMode(chs_mode)

        ch_1_state = (int_status & SPD3303Status.CHANNEL_1_STATE_MASK) >> 4
        self.channel_1_state = SPD3303ChannelState(ch_1_state)
        ch_2_state = (int_status & SPD3303Status.CHANNEL_2_STATE_MASK) >> 5
        self.channel_2_state = SPD3303ChannelState(ch_2_state)


class SPD3303CChannel:  # pragma: no cover
    def __init__(self, instrument, channel: int):
        self.inst = instrument
        self.channel = channel

    @property
    def voltage(self) -> float:
        resp = self.inst.query(f"MEAS:VOLT? CH{self.channel}")
        return float(resp)

    @property
    def current(self) -> float:
        resp = self.inst.query(f"MEAS:CURR? CH{self.channel}")
        return float(resp)

    def select(self) -> None:
        time.sleep(2)
        self.inst.write(f"INST CH{self.channel}")

    def on(self) -> None:
        time.sleep(1)
        self.inst.write(f"OUTP CH{self.channel},ON")

    def off(self) -> None:
        time.sleep(1)
        self.inst.write(f"OUTP CH{self.channel},OFF")


class SPD3303C:  # pragma: no cover
    # inst: USBInstrument
    # rm: ResourceManager
    channel_1: SPD3303CChannel
    channel_2: SPD3303CChannel
    channel_3: SPD3303CChannel

    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        res = self.rm.list_resources()
        res_to_use = res[0]
        self.inst = self.rm.open_resource(res_to_use)
        self.inst.write_termination = "\n"  # Modify termination character
        self.inst.read_termination = "\n"  # Modify termination character
        self.inst.query_delay = 2

        self.channel_1 = SPD3303CChannel(self.inst, 1)
        self.channel_2 = SPD3303CChannel(self.inst, 2)
        self.channel_3 = SPD3303CChannel(self.inst, 3)

    @property
    def idn(self) -> str:
        return self.inst.query("*IDN?")

    @property
    def status(self) -> SPD3303Status:
        hex_response = self.inst.query("SYST:STAT?")
        return SPD3303Status(hex_response)

    def close(self) -> None:
        self.inst.close()


if __name__ == "__main__":
    ps = SPD3303C()
    print(f"IDN: {ps.idn}")
    ps.channel_2.on()
    ps.channel_2.select()
    print(f"STATUS: {ps.status}")
    print(f"VOLTAGE: {ps.channel_1.voltage}V")
    print(f"CURRENT: {ps.channel_1.current}V")
    ps.channel_1.select()
    ps.channel_2.off()

    ps.close()
