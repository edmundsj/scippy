"""

"""
import pyvisa
from sciparse import to_standard_quantity, quantity_to_title
from scippy import SCPIDevice, twos_to_voltage, twos_to_integer, MotorController, ureg
import os
import time
import numpy as np
import pandas as pd

class TEController(SCPIDevice):
    def __init__(self, lib_type='pyserial',
            device_name='Arduino Nano TEC Controller',
            read_termination='\r\n', write_termination='\n',
            baud_rate=115200):
        """
        Implementation of communication device for my temperature controller.

        :param lib_type: "pyvisa" or "pyserial".
        :param device_name: Device name as it responds to the identify command
        :param read_termination: Read termination character
        :param write_termination: Write termination character

        """
        self.lib_type = lib_type
        super().__init__(lib_type=lib_type, device_name=device_name,
                read_termination=read_termination,
                write_termination=write_termination,
                baud_rate=baud_rate)
        self._mode = 'temperature'
        self._remote = False
        time.sleep(2) # Wait for Arduino initialization

    @property
    def mode(self):
        """
        Control mode of the device. Can be in one of three modes: "voltage", "current", and "temperature".
        """
        mode = self.query('MODE?')
        return mode

    @mode.setter
    def mode(self, mode):
        if mode not in ['voltage', 'current', 'temp', 'temperature']:
            raise ValueError(f'mode {mode} is not valid. Available modes are "voltage", "current", and "temperature"')
        self.write_line('MODE ' + mode)

    @property
    def voltage_setpoint(self):
        """
        Voltage (PWM value) being applied to the MOSFET base. Between -255 and +255.
        """
        data = int(self.query('SOURCE:VOLTAGE?'))
        return data

    @voltage_setpoint.setter
    def voltage_setpoint(self, voltage):
        self.remote = True
        self.mode = 'voltage'
        if voltage > 255:
            warnings.warn('Attempted to set voltage to {voltage}. Min value is -255. Setting to the min value of -255.')
            voltage  = 255
        elif voltage < -255:
            warnings.warn('Attempted to set voltage to {voltage}. Max value is 255. Setting to the max value of 255.')
            voltage  = -255
        self.write_line('SOURCE:VOLTAGE ' + str(voltage))
        self._voltage_setpoint = voltage

    @property
    def voltage(self):
        data = float(self.query('VOLTAGE?'))
        self._voltage = data
        return data

    @property
    @ureg.wraps(ureg.A, None, strict=False)
    def current_setpoint(self):
        data = float(self.query('SOURCE:CURRENT?'))
        return data

    @current_setpoint.setter
    @ureg.wraps(None, (None, ureg.A), strict=False)
    def current_setpoint(self, current):
        self.remote = True
        self.mode = 'current'
        self.write_line('SOURCE:CURRENT {:.2f}'.format(current))
        self._current_setpoint = current

    @property
    @ureg.wraps(ureg.A, None, strict=False)
    def current(self):
        data = float(self.query('CURRENT?'))
        return data

    @property
    def temperature_setpoint(self):
        data = float(self.query('SOURCE:TEMPERATURE?'))
        self._temperature = data
        return data

    @temperature_setpoint.setter
    def temperature_setpoint(self, temp):
        self.remote = True
        self.mode = 'temperature'
        self.write_line('SOURCE:TEMPERATURE {:.1f}'.format(temp))
        self._temperature = temp

    @property
    def temperature(self):
        data = float(self.query('TEMPERATURE?'))
        return data

    def reset(self):
        super().reset()
        self._remote = False

    @property
    def remote(self):
        rem = self.query('REMOTE?')
        if rem == '0':
            return False
        elif rem == '1':
            return True

    @remote.setter
    def remote(self, rem):
        if rem == True:
            rem_str = '1'
        elif rem == False:
            rem_str = '0'
        self.write_line('REMOTE ' + rem_str)
        self._remote = rem

    def measure_temperature(self):
        return float(self.query('MEASURE:TEMPERATURE?'))

    def measure_current(self):
        return float(self.query('MEASURE:CURRENT?'))

    @property
    def ready(self):
        rdy = self.query('READY?')
        if rdy == '1':
            return True
        else:
            return False
