# scpi controller
from enum import Enum

import pyvisa


class SPD3303CChannels(Enum):
    CHANNEL_1 = (1,)
    CHANNEL_2 = (2,)
    CHANNEL_3 = 3


class SPD3303CChannel:
    def __init__(self, instrument, channel: int):
        self.inst = instrument
        self.channel = channel

    @property
    def voltage(self) -> str:
        resp = self.inst.query(f"MEAS:VOLT? CH{self.channel}")
        # voltage = int(resp.split('\n')[0])
        return resp


class SPD3303C:
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

    def close(self) -> None:
        self.inst.close()


if __name__ == "__main__":
    ps = SPD3303C()
    print(f"IDN: {ps.idn}")
    print(f"VOLTAGE: {ps.channel_1.voltage}V")

    ps.close()
    # # print (res_to_use)
    # # inst.send_end = True
    # # inst.timeout = 2000
    # print("QUERY: " + )
    # # inst.query_delay=3
    # print("QUERY: " + inst.query("MEAS:VOLT? CH1"))
    # print("QUERY: " + inst.query("MEAS:CURR? CH1"))

    # time.sleep(0.04)  # Wait
    # # inst.write('OUTP CH1,ON') #Turn on output
    # time.sleep(2)  # Wait
    # # inst.write('OUTP CH1,OFF') #Turn off output
    # time.sleep(2)  # Wait
    # inst.close()  # Close instrument VISA session
