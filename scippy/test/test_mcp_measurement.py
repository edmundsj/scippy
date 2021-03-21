import pytest
from scippy import MCP, Agilent, twos_to_integer
from numpy.testing import assert_equal
import numpy as np
import pandas as pd

@pytest.fixture
def mcp():
    device = MCP()
    device.reset()
    yield {'device': device}
    device.reset()
    device.close()

@pytest.fixture
def agilent():
    device = Agilent()
    device.reset()
    yield {'device': device}
    device.reset()
    device.close()

@pytest.mark.mcp
def test_measure_simple(mcp):
    """
    Asserts that the result of a measurement is a set of three bytes, and that no more than 3 bytes are returned
    """
    desiredMeasurements = 1
    measuredData = mcp['device'].measure()
    assert_equal(len(measuredData), 3)


@pytest.mark.mcp
def test_measure_byte_count(mcp):
    """
    Asserts that the Configure() function can be used to measure between 1 and 100,000 measurements without
    dropping a single byte.
    """
    desiredMeasurementsList = [1, 10, 100, 1000, 10000]

    for desiredMeasurements in desiredMeasurementsList:
        desiredBytes = desiredMeasurements * 3
        mcp['device'].n_samples = desiredMeasurements
        data = mcp['device'].measure()
        actualBytes = len(data)
        assert_equal(actualBytes, desiredBytes)

@pytest.mark.skip
@pytest.mark.mcp
def test_measure_large_byte_count(mcp):
    """
    Asserts that we can measure very large numbers of measurements (1 million in this test) without dropping
    any bytes.
    """
    desiredMeasurements = 500000
    desiredBytes = desiredMeasurements * 3
    mcp['device'].n_samples = desiredMeasurements
    data = mcp['device'].measure() # If this isn't blocking, it should probably be made blocking.
    actualBytes = len(data)
    assert_equal(actualBytes, desiredBytes)

@pytest.mark.mcp
def test_synchronization_points(mcp, agilent):
    """
    Confirm that we get the expected number of data synchronization events when we sample in a given time period.
    Assumes an external 1kHz square wave is being applied to pin 20 on the Teensy.
    """
    f_sync = 105
    desired_sync_pulses = 8
    n_samples = int(mcp['device'].sampling_frequency/f_sync * desired_sync_pulses)

    agilent['device'].frequency = f_sync
    agilent['device'].output_on = True
    agilent['device'].verify()

    mcp['device'].n_samples = n_samples
    mcp['device'].measure()

    actual_sync_pulses = mcp['device'].sync_points()
    assert_equal(actual_sync_pulses, desired_sync_pulses)

@pytest.mark.mcp
def test_synchronization_data(mcp, agilent):
    """
    Verify that the synchronization data we get is "reasonable" - that is that points are separated by very close
    to their expected frequency of 1kHz. This assumes there is a square wave at 1kHz sending data to the Teensy.
    """
    f_sync = 105
    desired_sync_pulses = 3
    n_samples = int(
            mcp['device'].sampling_frequency/f_sync * desired_sync_pulses)

    agilent['device'].frequency = f_sync
    agilent['device'].output_on = True
    agilent['device'].verify()

    mcp['device'].n_samples = n_samples
    mcp['device'].measure()
    actual_sync_pulses = mcp['device'].sync_points()
    syncData = mcp['device'].sync_data()
    bytesPerDataPoint = 3
    desiredSyncBytes = bytesPerDataPoint * desired_sync_pulses

    # check that the data has the right number of bytes in it
    assert_equal(len(syncData), desiredSyncBytes)
    measurementPoints = twos_to_integer(syncData)
    measurementDeltas = np.diff(measurementPoints)
    timeDeltas = 1 / mcp['device'].sampling_frequency * measurementDeltas
    approxFrequencies = np.reciprocal(timeDeltas)
    approx_frequency = np.mean(approxFrequencies)
    np.testing.assert_allclose(approx_frequency, f_sync, atol=1e-2)

@pytest.mark.mcp
def test_generate_data(mcp):
    n_samples = 1111
    mcp['device'].n_samples = n_samples
    data = mcp['device'].generate_data()

    fs = mcp['device'].sampling_frequency
    time_data_desired = np.arange(0, n_samples/fs, 1/fs)

    assert_equal(data.shape, (n_samples, 3))
    assert_equal(type(data), pd.DataFrame)
    same_names = (data.columns.values == ['Time (s)', 'Voltage (mV)', 'Sync'])
    assert_equal(all(same_names), True)

@pytest.mark.mcp
def test_generate_data_long(mcp):
    n_samples = 10000
    mcp['device'].n_samples = n_samples
    data = mcp['device'].generate_data()

    fs = mcp['device'].sampling_frequency
    time_data_desired = np.arange(0, n_samples/fs, 1/fs)

    assert_equal(data.shape, (n_samples, 3))
    assert_equal(type(data), pd.DataFrame)
    same_names = (data.columns.values == ['Time (s)', 'Voltage (mV)', 'Sync'])
    assert_equal(all(same_names), True)
