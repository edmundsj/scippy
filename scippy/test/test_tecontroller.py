from scippy import TEC, ureg
import numpy as np
import pyvisa
import serial
import pytest
from numpy.testing import assert_equal, assert_allclose
from sciparse import assert_equal_qt

@pytest.fixture(scope='module')
def tec():
    print("Opening TEC device...")
    tec = TEC()
    yield tec
    print("Closing TEC device...")
    tec.reset()
    tec.close()

@pytest.mark.tec
def test_pyserial_init(tec):
    """
    Check that we get back the correct ID of our device
    """
    actual_type = type(tec.device)
    desired_type = serial.serialposix.Serial
    assert_equal(actual_type, desired_type)

@pytest.mark.tec
def test_identify(tec):
    desired_name = 'Arduino Nano TEC Controller'
    actual_name = tec.identify()
    assert_equal(actual_name, desired_name)

@pytest.mark.tec
def test_remote_control_default(tec):
    desired_control = False
    tec.reset()
    actual_control = tec.remote
    assert_equal(actual_control, desired_control)

@pytest.mark.tec
def test_set_remote_control(tec):
    desired_control = True
    tec.remote = desired_control
    actual_control = tec.remote
    assert_equal(actual_control, desired_control)

@pytest.mark.tec
def test_set_mode_voltage(tec):
    desired_mode = 'voltage'
    tec.control_mode = desired_mode
    actual_mode = tec.control_mode
    assert_equal(actual_mode, desired_mode)

@pytest.mark.tec
def test_set_mode_current(tec):
    desired_mode = 'current'
    tec.control_mode = desired_mode
    actual_mode = tec.control_mode
    assert_equal(actual_mode, desired_mode)

@pytest.mark.tec
def test_set_mode_temperature(tec):
    desired_mode = 'temperature'
    tec.control_mode = desired_mode
    actual_mode = tec.control_mode
    assert_equal(actual_mode, desired_mode)

@pytest.mark.tec
def test_set_voltage_setpoint(tec):
    desired_voltage = 50
    tec.voltage_setpoint = desired_voltage
    actual_voltage = tec.voltage_setpoint
    assert_equal_qt(actual_voltage, desired_voltage)

@pytest.mark.tec
def test_set_current_setpoint_units(tec):
    desired_current = 1 * ureg.A
    tec.current_setpoint = desired_current
    actual_current = tec.current_setpoint
    assert_equal_qt(actual_current, desired_current)

@pytest.mark.tec
def test_set_current_setpoint_unitless(tec):
    desired_current = 1 * ureg.A
    tec.current_setpoint = 1
    actual_current = tec.current_setpoint
    assert_equal_qt(actual_current, desired_current)

@pytest.mark.tec
def test_set_temperature_setpoint(tec):
    desired_temperature = 26.5
    tec.temperature_setpoint = desired_temperature
    actual_temperature = tec.temperature_setpoint
    assert_equal(actual_temperature, desired_temperature)

@pytest.mark.tec
def test_set_mode_temperature(tec):
    desired_mode = 'temperature'
    tec.mode = desired_mode
    actual_mode = tec.mode
    assert_equal(actual_mode, desired_mode)

@pytest.mark.tec
def test_measure_temperature(tec):
    desired_temperature_range = [19, 25]
    actual_temperature = tec.temperature
    assert actual_temperature < desired_temperature_range[1] and \
        actual_temperature > desired_temperature_range[0]

