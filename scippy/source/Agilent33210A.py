from scippy import SCPIDevice
import numpy as np

class Agilent33210A(SCPIDevice):
    MIN_AMPLITUDE = 0.01

    def __init__(self, lib_type='pyvisa',
            device_name='Agilent Technologies,33210A,MY48005679,1.04-1.04-22-2', read_termination='\n', write_termination='\n'):
        super().__init__(
                lib_type=lib_type, device_name=device_name,
                read_termination=read_termination,
                write_termination=write_termination)
        self._frequency = 1000 # Default frequency
        self._amplitude = 0.1
        self._offset_voltage = 0
        self._output_on = False

    @property
    def frequency(self):
        freq = self.query('FREQUENCY?')
        return float(freq)

    @frequency.setter
    def frequency(self, frequency):
        self._frequency = frequency
        self.write_line('FREQUENCY ' + str(frequency) + 'HZ')

    @property
    def amplitude(self, mode='amp'):
        amplitude = float(self.query('VOLTAGE?'))
        if mode == 'rms':
            amplitude /= np.sqrt(2)
        elif mode == 'pkpk':
            amplitude *= 2
        elif mode == 'amp':
            amplitude *= 1


        return float(amplitude)

    @amplitude.setter
    def amplitude(self, amplitude, mode='amp'):
        """ Sets the amplitude of the excitation (Vpp)

        :param amplitude: Amplitude of excitation (Vpp)
        """
        if mode == 'rms':
            amplitude *= np.sqrt(2)
        elif mode == 'pkpk':
            amplitude *= 0.5
        elif mode == 'amp':
            amplitude *= 1
        if amplitude < 0.01:
            amplitude = 0.01
            self._amplitude = amplitude
            self.write_line('VOLTAGE ' + str(amplitude) + 'V')
            raise UserWarning(f'Attempted to set amplitude to {amplitude}. Lowest possible amplitude for this device is {self.MIN_AMPLITUDE}. Setting amplitude to {self.MIN_AMPLITUDE}')

        self._amplitude = amplitude
        self.write_line('VOLTAGE ' + str(amplitude) + 'V')

    @property
    def offset_voltage(self):
        volt = self.query('VOLTAGE:OFFSET?')
        return float(volt)

    @offset_voltage.setter
    def offset_voltage(self, offset):
        self._offset_voltage = offset
        self.write_line('VOLTAGE:OFFSET ' + str(offset) + 'V')

    @property
    def output_on(self):
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
        Verifies that our system state matches our believed state
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
