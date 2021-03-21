from scippy import SCPIDevice
import numpy as np
import pyvisa
import pytest
from numpy.testing import assert_equal, assert_allclose

@pytest.fixture
def agilent():
    print("Opening Agilent device...")
    agilent_parameters = {
        'device': SCPIDevice(),
        'id': 'Agilent Technologies,33210A,MY48005679,1.04-1.04-22-2',
    }
    yield agilent_parameters
    print("Closing Agilent device...")
    agilent_parameters['device'].close()

@pytest.mark.agilent
def test_visa_init(agilent):
    """
    Check that we get back the correct ID of our device
    """
    actual_device = agilent['device'].device
    desired_type = pyvisa.resources.usb.USBInstrument
    assert_equal(type(actual_device), desired_type)

@pytest.mark.agilent
def test_identify(agilent):
    desired_name = agilent['id']
    actual_name = agilent['device'].identify()
    assert_equal(actual_name, desired_name)

@pytest.mark.agilent
def test_read_termination(agilent):
    desired_termination = '\n'
