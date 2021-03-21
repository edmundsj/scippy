from scippy import MCP
import numpy as np
import pyvisa
import serial
import pytest
from numpy.testing import assert_equal, assert_allclose

@pytest.fixture
def mcp():
    print("Opening MCP device...")
    mcp_parameters = {
        'device': MCP(),
        'id': 'MCP3561 Dev Board v1',
    }
    yield mcp_parameters
    print("Closing MCP device...")
    mcp_parameters['device'].reset()
    mcp_parameters['device'].close()

@pytest.mark.mcp
def test_pyserial_init(mcp):
    """
    Check that we get back the correct ID of our device
    """
    actual_device = mcp['device'].device
    desired_type = serial.serialposix.Serial
    assert_equal(type(actual_device), desired_type)

@pytest.mark.mcp
def test_identify(mcp):
    desired_name = mcp['id']
    actual_name = mcp['device'].identify()
    assert_equal(actual_name, desired_name)

@pytest.mark.mcp
def test_reset(mcp):
    pass

@pytest.mark.mcp
def test_verify(mcp):
    pass
