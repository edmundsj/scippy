#Setting up a new Repository
[![Build](https://github.com/edmundsj/pyscpi/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/edmundsj/pyscpi/actions/workflows/python-package-conda.yml) [![docs](https://github.com/edmundsj/pyscpi/actions/workflows/build-docs.yml/badge.svg)](https://github.com/edmundsj/pyscpi/actions/workflows/build-docs.yml) [![codecov](https://codecov.io/gh/edmundsj/pyscpi/branch/main/graph/badge.svg?token=VossgkNDyW)](https://codecov.io/gh/edmundsj/pyscpi)

Pronounced "skippy". Module for instrument communication via SCPI, implemented using pyvisa and pyserial (depending on the device)

## Features
- Communicate with devices over GPIB, RS232, or USB via SCPI protocol
- Several common instruments (Agilent 33210A, Keithley 2400 sourcemeter) already have dedicated classes
- Create new instruments with the SCPIDevice class

## Getting Started

### Installation

This package can be installed directly with pip from [pypi](https://pypi.org/project/scippy/): 
```
pip install scippy
```

### Simple Example
The following example sets the frequency, amplitude, and output state of an Agilent 33210A instrument, and verifies that the parameters match the ones you set.

```
from scippy import Agilent

agilent = Agilent()
agilent.frequency = 2500
agilent.amplitude = 0.5
agilent.output_on = True
agilent.verify()
