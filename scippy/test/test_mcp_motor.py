import pytest
from scippy import MCP, ureg
from numpy.testing import assert_allclose, assert_equal
import time

@pytest.fixture
def mcp():
    device = MCP()
    device.reset()
    yield device

    device.reset()
    device.close()

@pytest.mark.mcp
def testMotorPositionDefault(mcp):
    """
    Check that the motor position defaults to its expected value (0)
    """
    motor_position_desired = 0
    motor_position_actual = mcp.motor_position
    assert_equal(motor_position_desired, motor_position_actual)
    """
    Check that the motor direction defaults to 0
    """
    motor_direction_desired = 0
    motor_direction_actual = mcp.motor_direction
    assert_equal(motor_direction_actual, motor_direction_desired)

    motor_enable_desired = False
    motor_enable_actual = mcp.motor_enable
    assert_equal(motor_enable_actual, motor_enable_desired)

@pytest.mark.mcp
def testMotorPositionCommunication(mcp):
    """
    Check that we can read and then write a motor position to the motor.
    """
    motor_position_desired = 100
    mcp.motor_position = motor_position_desired
    motor_position_actual = mcp.motor_position
    assert_equal(motor_position_actual, motor_position_desired)

@pytest.mark.mcp
def testMotorRotatingDefault(mcp):
    """
    Check that by default the motor does not think it is rotating
    """
    motor_rotating_desired = False
    motor_rotatingActual = mcp.motor_rotating
    assert_equal(motor_rotatingActual, motor_rotating_desired)

@pytest.mark.mcp
def testMotorRotation(mcp):
    """
    Attempts to rotate the motor forward some, checks that the motor rotated, then attempts to rotate
    the motor backwards by some, and checks that it rotates. Also checks to see that the motor is in fact rotating
    after we give it the command.
    """
    motorRotationDesired = 100
    motor_position_desired = 0 + motorRotationDesired
    mcp.rotate_motor(motorRotationDesired)
    motor_position_actual = mcp.motor_position
    assert_equal(motor_position_actual, motor_position_desired)

    motorRotationDesired = -100
    motor_position_desired += motorRotationDesired
    mcp.rotate_motor(motorRotationDesired)
    motor_position_actual = mcp.motor_position
    assert_equal(motor_position_actual, motor_position_desired)

@pytest.mark.mcp
def testMotorAbortRotation(mcp):
    """
    Checks that after sending a motor rotation command we can abort that rotation successfully prior to the completion
    of the rotation.
    """
    motorRotation = 200
    mcp.rotate_motor(motorRotation)
    mcp.motor_enable = False
    motor_rotating_actual = mcp.motor_rotating # check that the motor is no longer rotating
    assert_equal(motor_rotating_actual, False)
    mcp.rotate_motor(-1*motorRotation) # Put back in original position

@pytest.mark.mcp
def testMotorSpeedDefault(mcp):
    """
    Check the default settings for motor speed.
    """
    motor_period_desired = 2
    motor_period_actual = mcp.motor_period
    assert_equal(motor_period_actual, motor_period_desired)

@pytest.mark.mcp
def testMotorSpeed(mcp):
    """
    Check that we can successfully change the motor's period (and hence its speed)
    """
    motor_period_desired = 5;
    mcp.motor_period = motor_period_desired
    motor_period_actual = mcp.motor_period
    assert_equal(motor_period_actual, motor_period_desired)

@pytest.mark.mcp
def testMotorEnableDisableDefault(mcp):
    """
    Check that the motor is enabled by default
    """
    motor_enable_desired = False
    motor_enable_actual = mcp.motor_enable
    assert_equal(motor_enable_actual, motor_enable_desired)

@pytest.mark.mcp
def testMotorEnableDisable(mcp):
    """
    Test enabling and disabling of the motor
    """
    motor_enable_desired = False
    mcp.motor_enable = motor_enable_desired
    motor_enable_actual = mcp.motor_enable
    assert_equal(motor_enable_actual, motor_enable_desired)

    motor_enable_desired = True
    mcp.motor_enable = motor_enable_desired
    motor_enable_actual = mcp.motor_enable
    assert_equal(motor_enable_actual, motor_enable_desired)

@pytest.mark.mcp
def test_motor_wavelength_steps(mcp):
    mcp.motor_enable = True
    motor_position_initial = mcp.motor_position
    mcp.wavelength = mcp.wavelength + 5*ureg.nm

    motor_position_final = mcp.motor_position
    actual_delta_position = motor_position_final - motor_position_initial
    desired_delta_position = 153
    assert_equal(actual_delta_position, desired_delta_position)

    mcp.wavelength = mcp.wavelength - 5*ureg.nm
    motor_position_final = mcp.motor_position
    actual_delta_position = motor_position_final - motor_position_initial
    desired_delta_position = 0
    assert_equal(actual_delta_position, desired_delta_position)

