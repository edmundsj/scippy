import numpy as np

"""
Convert a twos-complement set of bytes (1, 2, 3, etc.) into a floating-point value.
"""
def twos_to_integer(twosBytes, firstByte='msb', bytesPerInteger=3):
    number = 0.0
    numberBytes = len(twosBytes)
    numberIntegers = int(numberBytes / bytesPerInteger)
    twosBytes = twosBytes.reshape(numberIntegers, bytesPerInteger)

    if(firstByte == 'msb'):
        for i in range(bytesPerInteger):
            number += np.power(256, bytesPerInteger - 1 - i) * twosBytes[:, i]

        isNegative = (twosBytes[:, 0] & 0b10000000) != 0 # checks the MSB of the twos complement number
        number -= np.power(2, 8*bytesPerInteger)*isNegative
    elif(firstByte == 'lsb'):
        for i in range(bytesPerInteger):
            number += np.power(256, i) * twosBytes[i]

        isNegative = bool(twosBytes[-1] & 0b10000000)
        number -= np.power(2, 8*bytesPerInteger)*isNegative

    if isinstance(number, np.ndarray):
        number = number.astype(int)
    return number


"""
Converts the AD7766 count to a differential voltage

:param maxVoltage: The maximum voltage that can be seen at either ADC input (5V for the AD7766)
:param numberBits: The number of bits the ADC uses.
"""
def count_to_voltage(data, numberBits=24, maxVoltage=3.3, differential=False):
    # The maximum representable unsigned number is 2^24, but the maximum representable twos complement
    # number is half that, or 2^24 / 2
    conversionFactor = maxVoltage / (pow(2.0, numberBits-1))
    return np.multiply(data, conversionFactor)

def twos_to_voltage(data, bytesPerInteger=3, maxVoltage=3.3, firstByte='msb', differential=False):
    intermediateData = twos_to_integer(data, firstByte=firstByte, bytesPerInteger=bytesPerInteger)
    voltages = count_to_voltage(intermediateData, maxVoltage=maxVoltage, differential=differential)
    return voltages
