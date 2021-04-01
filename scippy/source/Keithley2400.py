"""

"""
from scippy import SCPIDevice, ureg
import numpy as np
import pint

class Keithley2400(SCPIDevice):
    MIN_AMPLITUDE = 0.01

    def __init__(self, lib_type='pyvisa',
            device_name='KEITHLEY INSTRUMENTS INC.,MODEL 2400,1207317,C30   Mar 17 2006 09:29:29/A02  /K/J', read_termination='\r', write_termination='\r'):
        """
        Agilent 33210A function generator object

        :param device_name: Manufacturer device name
        :param read_termination: Read termination character(s)
        :param write_termination: Write termination character(s)

        """
        super().__init__(
                lib_type=lib_type, device_name=device_name,
                read_termination=read_termination,
                write_termination=write_termination)

        self._mode = 'voltage'
        self._current_compliance = 105.0*ureg.uA
        self._voltage_compliance = 21*ureg.V
        self._voltage = 0*ureg.V
        self._current = 0*ureg.mA

        self.mode = self._mode
        self.current_compliance = self._current_compliance
        self.voltage_compliance = self._voltage_compliance
        self.voltage = self._voltage
        self.current = self._current

    @property
    @ureg.wraps(ureg.V, None, False)
    def voltage(self):
        volt = float(self.query('source:voltage:level?'))
        return volt

    @voltage.setter
    @ureg.wraps(None, (None, ureg.V), False)
    def voltage(self, voltage):
        self._voltage = voltage
        if self._mode == 'current':
            self.mode = 'voltage'
        self.write_line(f'source:voltage:level {voltage}')

    @property
    @ureg.wraps(ureg.A, None, False)
    def current(self):
        current = float(self.query('source:current:level?'))
        return current

    @current.setter
    @ureg.wraps(None, (None, ureg.A), False)
    def current(self, current):
        self._current = current
        if self._mode == 'voltage':
            self.mode = 'current'
        self.write_line(f'source:current:level {current}')

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode == 'voltage':
            self.write_line('source:function voltage')
            self._mode = mode
        elif mode == 'current':
            self.write_line('source:function current')
            self._mode = mode
        else:
            raise ValueError(f'Mode {mode} not recognized. Available modes are "voltage" and "current"')

    @property
    def output_on(self):
        output_state = self.query('output:state?')
        if output_state == '0':
            output_state = False
        elif output_state == '1':
            output_state = True

        return output_state

    @output_on.setter
    def output_on(self, output):
        if output == True:
            self.write_line('output:state on')
        elif output == False:
            self.write_line('output:state off')
        else:
            raise ValueError(f'Output state {output} not recognized. Available values are True and False')

    @property
    @ureg.wraps(ureg.A, None, False)
    def current_compliance(self):
        compliance = float(self.query('sense:current:protection:level?'))
        return compliance

    @current_compliance.setter
    @ureg.wraps(None, (None, ureg.A), False)
    def current_compliance(self, compliance):
        self._current_compliance = compliance
        self.write_line(f'sense:current:protection:level {compliance}')

    @property
    @ureg.wraps(ureg.V, None, False)
    def voltage_compliance(self):
        compliance = float(self.query('sense:voltage:protection:level?'))
        return compliance

    @voltage_compliance.setter
    @ureg.wraps(None, (None, ureg.V), False)
    def voltage_compliance(self, compliance):
        self._voltage_compliance = compliance
        self.write_line(f'sense:voltage:protection:level {compliance}')
