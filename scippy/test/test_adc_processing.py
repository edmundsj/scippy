from scippy import twos_to_integer, twos_to_voltage, count_to_voltage
import pytest
from numpy.testing import assert_equal, assert_allclose
import numpy as np

@pytest.mark.remote
def testTwosToInteger():
    """
    Check that this function converts a set of three bytes in twos complement to a signed integer. Checks
    two 3-byte arrays and one 6-byte array.
    """
    testBytes = np.array([255, 255, 255]) # check for proper sign conversion
    desiredInteger = -1
    actualInteger = twos_to_integer(testBytes)
    assert_equal(desiredInteger, actualInteger)

    testBytes = np.array([100, 255, 255])
    desiredInteger = 6619135
    actualInteger = twos_to_integer(testBytes)
    assert_equal(desiredInteger, actualInteger)

    testBytes = np.array([255, 255, 255, 100, 255, 255])
    desiredIntegers = np.array([-1, 6619135])
    actualIntegers = twos_to_integer(testBytes)
    assert_allclose(desiredIntegers, actualIntegers, atol=1e-5)

@pytest.mark.remote
def testCountToVoltage():
    """
    Test converting a raw ADC count into a voltage
    """
    desiredValue = 5.0
    actualCount = pow(2, 23)
    actualValue = count_to_voltage(actualCount, maxVoltage=5)
    assert_allclose(desiredValue, actualValue)

@pytest.mark.remote
def testTwosToVoltage():
    desiredVoltage = np.array([5.0])
    testBytes = np.array([127, 255, 255])
    actualVoltage = twos_to_voltage(testBytes, maxVoltage=5, differential=True)
    assert_allclose(desiredVoltage, actualVoltage, atol=1e-5)
