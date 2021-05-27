"""

"""
from scippy import SCPIDevice, ureg
import numpy as np
import pint
import warnings

class Keithley2635(SCPIDevice):
    COMPLIANCE_CEILING = 9.910000E+37


    def __init__(self, lib_type='pyvisa',
            device_name='Keithley Instruments Inc., Model 2635, 1212537, 1.4.1',
            resource_name='',
            read_termination='\n', write_termination='\n', baud_rate=57600):
        """
        Keithley 2635 measurement device

        :param device_name: Manufacturer device name
        :param read_termination: Read termination character(s)
        :param write_termination: Write termination character(s)

        """
        super().__init__(
                lib_type=lib_type, device_name=device_name,
                read_termination=read_termination,
                write_termination=write_termination,
                baud_rate=baud_rate, resource_name=resource_name)

        self._mode = 'voltage'
        self._current_compliance = 105.0*ureg.uA
        self._voltage_compliance = 21*ureg.V
        self._voltage = 0*ureg.V
        self._current = 0*ureg.mA
        self._current_range = 0*ureg.A
        self._voltage_range = 0*ureg.V

#self.mode = self._mode
#self.current_compliance = self._current_compliance
#self.voltage_compliance = self._voltage_compliance
#self.voltage_range = self.voltage_range
#self.current_range = self.current_range
#self.voltage = self._voltage
#self.current = self._current

    @property
    @ureg.wraps(ureg.V, None, False)
    def voltage(self):
        volt = float(self.query('print(smua.source.levelv)'))
        return volt

    @voltage.setter
    @ureg.wraps(None, (None, ureg.V), False)
    def voltage(self, voltage):
        self._voltage = voltage
        if self._mode == 'current':
            self.mode = 'voltage'
        if not isinstance(voltage, pint.Quantity):
            voltage_to_compare = voltage* ureg.V
        if voltage_to_compare > self._voltage_range:
            self.voltage_range = voltage
        self.write_line(f'smua.source.levelv = {voltage}')

    @property
    @ureg.wraps(ureg.A, None, False)
    def current(self):
        current = float(self.query('print(smua.source.leveli)'))
        return current

    @current.setter
    @ureg.wraps(None, (None, ureg.A), False)
    def current(self, current):
        self._current = current
        if self._mode == 'voltage':
            self.mode = 'current'
        if not isinstance(current, pint.Quantity):
            current_to_compare = current * ureg.A
        if current_to_compare > self._current_range:
            self.current_range = current

        self.write_line(f'smua.source.leveli = {current}')

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode == 'voltage':
            self.write_line('smua.source.func = smua.OUTPUT_DCVOLTS')
            self._mode = mode
        elif mode == 'current':
            self.write_line('smua.source.func = smua.OUTPUT_DCAMPS')
            self._mode = mode
        else:
            raise ValueError(f'Mode {mode} not recognized. Available modes are "voltage" and "current"')

    @property
    def output_on(self):
        output_state = float(self.query('print(smua.source.output)'))
        if output_state == 0:
            output_state = False
        elif output_state == 1:
            output_state = True

        return output_state

    @output_on.setter
    def output_on(self, output):
        if output == True:
            self.write_line('smua.source.output = 1')
        elif output == False:
            self.write_line('smua.source.output = 0')
        else:
            raise ValueError(f'Output state {output} not recognized. Available values are True and False')

    @property
    @ureg.wraps(ureg.A, None, False)
    def current_compliance(self):
        compliance = float(self.query('print(smua.source.limiti)'))
        return compliance

    @current_compliance.setter
    @ureg.wraps(None, (None, ureg.A), False)
    def current_compliance(self, compliance):
        self._current_compliance = compliance
        self.write_line(f'smua.source.limiti = {compliance}')

    @property
    @ureg.wraps(ureg.V, None, False)
    def voltage_compliance(self):
        compliance = float(self.query('print(smua.source.limitv)'))
        return compliance

    @voltage_compliance.setter
    @ureg.wraps(None, (None, ureg.V), False)
    def voltage_compliance(self, compliance):
        self._voltage_compliance = compliance
        self.write_line(f'smua.source.limitv = {compliance}')

    @property
    @ureg.wraps(ureg.V, None, False)
    def voltage_range(self):
        voltage_range = float(self.query('print(smua.source.rangev)'))
        return voltage_range

    @voltage_range.setter
    @ureg.wraps(None, (None, ureg.V), False)
    def voltage_range(self, voltage):
        if isinstance(voltage, pint.Quantity):
            voltage = voltage.to(ureg.V).m
        available_ranges = np.array([0.2, 2, 20, 200])
        for v in available_ranges:
            target_range = v
            if voltage < v: break
        self.write_line(f'smua.source.rangev = {target_range:e}')
        self._voltage_range = target_range*ureg.V

    @property
    @ureg.wraps(ureg.A, None, False)
    def current_range(self):
        current_range = float(self.query('print(smua.source.rangei)'))
        return current_range

    @current_range.setter
    @ureg.wraps(None, (None, ureg.A), False)
    def current_range(self, current):
        if isinstance(current, pint.Quantity):
            current = current.to(ureg.A).m
        available_ranges = [100e-12, 1e-9, 10e-9, 100e-9, 1e-6, 10e-6, 100e-6, \
            1e-3, 10e-3, 100e-3, 1, 1.5]
        for i in available_ranges:
            target_range = i
            if current < i: break
        self.write_line(f'smua.source.rangei {target_range:e}')
        self._current_range = target_range * ureg.A

    @property
    def at_compliance_limit(self):
        result = keith.query('print(smua.source.compliance)')
        if result == 'true':
            return True
        elif result == 'false':
            return False
        else:
            raise ValueError('Got unknown compliance value {result}.')

    def measure(self, measure_mode=None):
        """
        Returns the measured current if in voltage mode and the measured current if in voltage mode, along with the set voltage in voltage mode or the set current in current mode
        """
        result = self.query('print(smua.measure.iv())')
        current, voltage = [float(x) for x in result.split('\t')]

        return voltage*ureg.V, current*ureg.A
