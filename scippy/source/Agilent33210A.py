"""

"""
from scippy import SCPIDevice, ureg
import numpy as np
import pint

class Agilent33210A(SCPIDevice):
    MIN_AMPLITUDE = 0.01

    def __init__(self, lib_type='pyvisa',
            device_name='Agilent Technologies,33210A,MY48005679,1.04-1.04-22-2', read_termination='\n', write_termination='\n'):
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
        self._frequency = 1000*ureg.Hz # Default frequency
        self._amplitude = 0.1*ureg.V
        self._offset_voltage = 0*ureg.V
        self._output_on = False

    @property
    @ureg.wraps(ureg.Hz, None, strict=False)
    def frequency(self):
        """
        Frequency of the applied signal
        """
        freq = self.query('FREQUENCY?')
        return float(freq)

    @frequency.setter
    @ureg.wraps(None, (None, ureg.Hz), strict=False)
    def frequency(self, frequency):
        if isinstance(frequency, pint.Quantity):
            self._frequency = frequency
        else:
            self._frequency = frequency * ureg.Hz
        self.write_line('FREQUENCY ' + str(frequency) + 'HZ')

    @property
    @ureg.wraps(ureg.V, None, strict=False)
    def amplitude(self):
        """
        Amplitude of the applied signal. Input is in volts (amplitude)
        """
        amplitude = float(self.query('VOLTAGE?'))
        return amplitude

    @amplitude.setter
    @ureg.wraps(None, (None, ureg.V), strict=False)
    def amplitude(self, amplitude):
        if amplitude < 0.01:
            amplitude = 0.01
            self._amplitude = amplitude
            self.write_line('VOLTAGE ' + str(amplitude) + 'V')
            raise UserWarning(f'Attempted to set amplitude to {amplitude}. Lowest possible amplitude for this device is {self.MIN_AMPLITUDE}. Setting amplitude to {self.MIN_AMPLITUDE}')

        if isinstance(amplitude, pint.Quantity):
            self._amplitude = amplitude
        else:
            self._amplitude = amplitude * ureg.V

        self.write_line('VOLTAGE ' + str(amplitude) + 'V')

    @property
    @ureg.wraps(ureg.V, None, strict=False)
    def offset_voltage(self):
        """
        DC offset voltage of the applied signal
        """
        volt = self.query('VOLTAGE:OFFSET?')
        return float(volt)

    @offset_voltage.setter
    @ureg.wraps(None, (None, ureg.V), strict=False)
    def offset_voltage(self, offset):
        if isinstance(offset, pint.Quantity):
            self._offset_voltage = offset
        else:
            self._offset_voltage = offset * ureg.V

        self.write_line('VOLTAGE:OFFSET ' + str(offset) + 'V')

    @property
    def output_on(self):
        """
        Whether the output is on (True) or off (False)
        """
        return bool(int(self.query('OUTPUT?')))

    @output_on.setter
    def output_on(self, output):
        self._output_on = output
        if output == True:
            output_string = 'ON'
        else:
            output_string = 'OFF'
        self.write_line('OUTPUT ' + output_string)

    def verify(self):
        """
        Verifies that our system state matches our believed state.
        """
        actual_amplitude = self.amplitude
        actual_frequency = self.frequency
        actual_output_on = self.output_on
        actual_offset_voltage = self.offset_voltage
        if actual_amplitude != self._amplitude:
            raise AssertionError(f'Amplitudes not correct. Actual: {actual_amplitude} vs desired: {self._amplitude}')
        if actual_frequency != self._frequency:
            raise AssertionError(f'Frequency not correct. Actual: {actual_frequency} vs desired: {self._frequency}')
        if actual_output_on != self._output_on:
            raise AssertionError(f'Output state not correct. Actual: {actual_output_on}, desired: {self._output_on}')
        if actual_offset_voltage != self._offset_voltage:
            raise AssertionError(f'Offset voltage not correct. Actual {actual_offset_voltage}, desired: {self._offset_voltage}')
        return True
