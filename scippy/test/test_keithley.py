"""
The Keithley doesn't like having its interface open and closed rapidly, so we can't do tests the way we normally would. In fact, this equipment's communication interface appears to be complete garbage, and terribly unreliable. The manufacturer should be ashamed. Agilent doesn't have the same issues. Neither does my garage-level equipment. Tsk tsk.
"""
from scippy import Keithley, ureg
from sciparse import assert_equal_qt
import time
import numpy as np
import pyvisa
import pytest
import pint
import serial
from numpy.testing import assert_equal, assert_allclose

@pytest.fixture
def timeout(keithley):
    time.sleep(0.2)
    yield None
    time.sleep(0.2)
    keithley['device'].output_on = False

@pytest.fixture(scope='session')
def keithley():
    print("Opening Keithley 2400 device...")
    keith = Keithley()
    keithley_parameters = {
        'device': keith,
        'id': 'KEITHLEY INSTRUMENTS INC.,MODEL 2400,1207317,C30   Mar 17 2006 09:29:29/A02  /K/J',
    }
    yield keithley_parameters
    print("Closing Keithley2400 device...")
    keithley_parameters['device'].reset()
    keithley_parameters['device'].close()

@pytest.mark.keithley
def test_visa_init(keithley, timeout):
    """
    Check that we get back the correct ID of our device
    """
    actual_device = keithley['device'].device
    desired_type = pyvisa.resources.serial.SerialInstrument
    assert_equal(type(actual_device), desired_type)

@pytest.mark.keithley
def test_identify(keithley, timeout):
    desired_name = keithley['id']
    actual_name = keithley['device'].identify()
    assert_equal(actual_name, desired_name)

@pytest.mark.keithley
def test_reset(keithley, timeout):
    keithley['device'].reset()
    desired_voltage = 0*ureg.V
    desired_current = 0*ureg.uA
    desired_voltage_compliance = 21*ureg.V
    desired_current_compliance = 105*ureg.uA

    actual_voltage = keithley['device'].voltage
    actual_current = keithley['device'].current.to(ureg.uA)
    actual_voltage_compliance = keithley['device'].voltage_compliance
    actual_current_compliance = keithley['device'].current_compliance.to(ureg.uA)

    assert_equal_qt(actual_voltage, desired_voltage)
    assert_equal_qt(actual_current, desired_current)
    assert_equal_qt(actual_current_compliance, desired_current_compliance)
    assert_equal_qt(actual_voltage_compliance, desired_voltage_compliance)

@pytest.mark.keithley
def test_set_voltage(keithley, timeout):
    desired_voltage = 10*ureg.V
    keithley['device'].voltage = 10
    keithley['device'].output_on = True
    actual_voltage = keithley['device'].voltage
    assert_equal_qt(actual_voltage, desired_voltage)

@pytest.mark.keithley
def test_set_voltage_units(keithley, timeout):
    desired_voltage = 10*ureg.V
    keithley['device'].voltage = desired_voltage
    keithley['device'].output_on = True
    actual_voltage = keithley['device'].voltage
    assert_equal_qt(actual_voltage, desired_voltage)

@pytest.mark.keithley
def test_set_current(keithley, timeout):
    desired_current = 10*ureg.mA
    keithley['device'].current = 0.01
    keithley['device'].output_on = True
    actual_current = keithley['device'].current
    assert_equal_qt(actual_current, desired_current)

@pytest.mark.keithley
def test_set_current_units(keithley, timeout):
    desired_current = 10*ureg.mA
    keithley['device'].current = desired_current
    keithley['device'].output_on = True
    actual_current = keithley['device'].current
    assert_equal_qt(actual_current, desired_current)

@pytest.mark.keithley
def test_set_current_compliance(keithley, timeout):
    desired_compliance = 1*ureg.mA
    keithley['device'].current_compliance = 0.001
    actual_compliance = keithley['device'].current_compliance
    assert_equal_qt(actual_compliance, desired_compliance)

@pytest.mark.keithley
def test_set_current_compliance_units(keithley, timeout):
    desired_compliance = 1*ureg.mA
    keithley['device'].current_compliance = desired_compliance
    actual_compliance = keithley['device'].current_compliance
    assert_equal_qt(actual_compliance, desired_compliance)

@pytest.mark.keithley
def test_set_voltage_compliance(keithley, timeout):
    desired_compliance = 1*ureg.V
    keithley['device'].voltage_compliance = 1
    actual_compliance = keithley['device'].voltage_compliance
    assert_equal_qt(actual_compliance, desired_compliance)

@pytest.mark.keithley
def test_set_voltage_compliance_units(keithley, timeout):
    desired_compliance = 1*ureg.V
    keithley['device'].voltage_compliance = desired_compliance
    actual_compliance = keithley['device'].voltage_compliance
    assert_equal_qt(actual_compliance, desired_compliance)

@pytest.mark.keithley
def test_set_voltage_to_current(keithley, timeout):
    """
    Check that we are switching from voltage mode to current mode when we assign a current.
    """
    keithley['device'].voltage = 1
    actual_mode = keithley['device'].mode
    desired_mode = 'voltage'
    assert_equal(actual_mode, desired_mode)

    keithley['device'].current = 1 * ureg.mA
    actual_mode = keithley['device'].mode
    desired_mode = 'current'
    assert_equal(actual_mode, desired_mode)

@pytest.mark.keithley
def test_set_current_to_voltage(keithley, timeout):
    """
    Check that we are switching from current mode to voltage mode when we assign a current.
    """
    keithley['device'].current = 1 * ureg.mA
    actual_mode = keithley['device'].mode
    desired_mode = 'current'
    assert_equal(actual_mode, desired_mode)

    keithley['device'].voltage = 1
    actual_mode = keithley['device'].mode
    desired_mode = 'voltage'
    assert_equal(actual_mode, desired_mode)

@pytest.mark.keithley
def test_measure_voltage(keithley, timeout):
    desired_voltage = 1 * ureg.V
    keithley['device'].voltage = desired_voltage
    actual_voltage, actual_current = keithley['device'].measure()
    assert_equal_qt(actual_voltage, desired_voltage)
    assert abs(actual_current) < 0.1*ureg.nA

@pytest.mark.keithley
def test_measure_current(keithley, timeout):
    desired_voltage = 21 * ureg.V
    keithley['device'].voltage_compliance = desired_voltage
    keithley['device'].current = 10*ureg.mA
    actual_voltage, actual_current = keithley['device'].measure()
    assert_equal_qt(actual_voltage, desired_voltage)
    assert abs(actual_current) < 0.01*ureg.mA

@pytest.mark.keithley
def test_measure_warning(keithley, timeout):
    with pytest.warns(UserWarning):
        keithley['device'].current = 0.01
        voltage, current = keithley['device'].measure()
