Setting up a new Repository
===============================
[![Build](https://github.com/edmundsj/pyscpi/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/edmundsj/pyscpi/actions/workflows/python-package-conda.yml) [![docs](https://github.com/edmundsj/pyscpi/actions/workflows/build-docs.yml/badge.svg)](https://github.com/edmundsj/pyscpi/actions/workflows/build-docs.yml) [![codecov](https://codecov.io/gh/edmundsj/pyscpi/branch/main/graph/badge.svg?token=VossgkNDyW)](https://codecov.io/gh/edmundsj/pyscpi)


Getting Started
------------------

Notes
--------
pyVISA is extremely unreliable. If you don't close a resource, it gets left
occupied and is not usable. It also takes a really long time to update
available resources compared to pyserial. Sometimes I have to wait like 3
minutes for the device to be available. Sometimes it will be, and sometimes it
won't be, and eventually it becomes unusable, and I start getting
pyvisa.errors.VisAIOError: Timeout or the resource is valid, but VISA cannot
currently access it. Maybe I just try using a function generator accessible via
serial, because this is bullshit.

Using a different piece of equipment made by agilent, VISA communication
appears to be working for now, and I'm not having any issues with queries
receiving different values each time. This might actually have been an
instrumentation issue.
