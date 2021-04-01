"""

"""
import pyvisa
from scippy import SCPIDevice, twos_to_voltage, twos_to_integer, MotorController
import os
import numpy as np
import pandas as pd
import json

class MCP3561(SCPIDevice, MotorController):
    def __init__(self, lib_type='pyserial',
            device_name='MCP3561 Dev Board v1', read_termination='\r\n', write_termination='\n', sampling_frequency=9765.65,
            n_samples=1, offset_voltage=1.198):
        """
        Implementation of communication device for the MCP3561 ADC and an accompanying development board.

        :param lib_type: "pyvisa" or "pyserial".
        :param device_name: Device name as it responds to the identify command
        :param read_termination: Read termination character
        :param write_termination: Write termination character
        :param n_samples: Number of samples to take
        :param offset_voltage: Calibrated zero-point voltage.
        :param sampling_frequency: Sampling frequency of the device. Not currently settable.

        """
        self.lib_type = lib_type
        super().__init__(lib_type=lib_type, device_name=device_name,
                read_termination=read_termination,
                write_termination=write_termination)
        self._n_samples = n_samples
        self._n_bytes = n_samples * 3 + 1
        self._n_synchronization_pulses = 0
        self.sampling_frequency = sampling_frequency
        self.offset_voltage = offset_voltage

        self._microsteps_per_nm = 30.3716*1.011 # calibrated from 800nm - 1700nm. Optimized for 5nm steps.
        self._microsteps_correction = -6.17*1e-6

        if(os.path.isfile('device_settings.txt')):
            with open('device_settings.txt', 'r') as settingsFile:
                data = json.load(settingsFile)
                self._wavelength = data['wavelength']
        else:
             self._wavelength = 1000

    @property
    def n_samples(self):
        """
        Number of samples the device should measure, where each sample is a single 24-bit measurement.
        """
        return self._n_samples

    @n_samples.setter
    def n_samples(self, n_samples):
        if self._n_samples != n_samples:
            self._n_samples = n_samples
            self._n_bytes= n_samples*3 + 1
            self.write_line('CONFIGURE ' + str(n_samples))

    def measure(self):
        """
        Measures data from the MCP dev board.

        :returns byte_array: Raw array of bytes as measured by the MCP
        """
        old_timeout = self.device.timeout
        measurement_time_ms = 1000*self._n_samples / self.sampling_frequency
        if(measurement_time_ms > self.device.timeout - 100):
            self.device.timeout = measurement_time_ms + 100

        bytes_written = self.write_line('MEASURE?')
        measured_data = self.read_bytes(self._n_bytes)

        if len(measured_data) == 0:
            raise ValueError(f"No data measured from device. Attempted to read {self._n_bytes} bytes.")
        verification_char = measured_data[0]
        if chr(verification_char) != '#':
            raise ValueError(
                f'Did not receive verification character #. Actual character is {verification_char}')

        measured_bytes = np.frombuffer(
                measured_data[1:], dtype=np.uint8)

        if measurement_time_ms > old_timeout:
            self.device.timeout = old_timeout

        return measured_bytes

    def sync_points(self):
        """
        Get the number of points we will use for synchronization and subsequent sampling

        :return syncPoints: The number of pulses measured from the signal generator
        """
        return int(self.query('SYNC:NUMPOINTS?'))

    def sync_data(self):
        """
        Get the measurement numbers that each synchronization pulse corresponds to.

        :returns data: an array of integers corresponding to the measurement indices of the synchronization point events.

        """
        number_points = self.sync_points()
        self.write_line('SYNC:DATA?')
        number_bytes = number_points*3 +1
        measuredData = self.read_bytes(number_bytes)
        measuredData = np.frombuffer(measuredData[1:], dtype=np.uint8) # Discard the leading # and the newline at the end
        return measuredData

    def generate_data(self, sync=True):
        """
        Generates time-series voltage data with or without synchronization points

        :param n_samples: The number of points of data to collect
        :param sync: Whether to report synchronization points from an external reference (True/False)
        :returns: data - a pandas data frame with voltages, times, and (optional) sync points
        """
        voltages = twos_to_voltage(self.measure()) - self.offset_voltage
        times = np.linspace(0, self.n_samples / self.sampling_frequency,
                          self.n_samples)
        pi_phase_indices = twos_to_integer(self.sync_data())
        pi_phase_indices = pi_phase_indices[pi_phase_indices<self.n_samples]
        sync_column = np.zeros(self.n_samples, dtype=np.int)
        sync_column[pi_phase_indices] = 1 # Sync event

        data = pd.DataFrame(data={
            'Time (s)': times,
            'Voltage (mV)': voltages*1e3,
            'Sync': sync_column})

        return data

