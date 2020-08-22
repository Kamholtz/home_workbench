# scpi controller
import time

import easy_scpi as scpi
import pyvisa


class PowerSupply(scpi.Instrument):
    def __init__(self, port):
        scpi.SCPI_Instrument.__init__(
            self, port=port, timeout=5, read_termination="\n", write_termination="\n"
        )

        # other initialization code...

    # --- public methods ---

    @property
    def voltage(self):
        """
        Returns the voltage setting
        """
        return self.source.volt.level()

    @voltage.setter
    def voltage(self, volts):
        """
        Sets the voltage of the instrument
        """
        self.source.volt.level(volts)

    @property
    def current(self):
        """
        Returns the current setting in Amps
        """
        return self.source.current.level()

    @current.setter
    def current(self, amps):
        """
        Set the current of the instrument
        """
        self.source.current.level(amps)

    def on(self):
        """
        Turns the output on
        """
        self.output.state("on")

    def off(self):
        """
        Turns the output off
        """
        self.output.state("off")


if __name__ == "__main__":
    # ps = PowerSupply('USB0::0x0483::0x7540::SPD3EDCC4R0010::INSTR')
    # ps.connect()
    # print("voltage = " + ps.voltage)

    rm = pyvisa.ResourceManager()
    res = rm.list_resources()
    res_to_use = res[0]
    inst = rm.open_resource(res_to_use)
    # print (res_to_use)
    # inst.send_end = True
    # inst.timeout = 2000
    inst.write_termination = "\n"  # Modify termination character
    inst.read_termination = "\n"  # Modify termination character
    print(f"Write termination: {inst.write_termination}")
    print(f"Read termination: {inst.read_termination}")
    inst.query_delay = 2
    print("QUERY: " + inst.query("*IDN?"))
    # inst.query_delay=3
    print("QUERY: " + inst.query("MEAS:VOLT? CH1"))
    print("QUERY: " + inst.query("MEAS:CURR? CH1"))

    time.sleep(0.04)  # Wait
    # inst.write('OUTP CH1,ON') #Turn on output
    time.sleep(2)  # Wait
    # inst.write('OUTP CH1,OFF') #Turn off output
    time.sleep(2)  # Wait
    inst.write("*IDN?")  # Write instrument and ask for identification string

    time.sleep(1)  # Wait
    qStr = inst.read()  # Read instrument response
    print(str(qStr))  # Print returned string
    inst.close()  # Close instrument VISA session
