# PlutoStudio - A Python based GUI for the ADALM-PlutoSDR
# Copyright (c) 2023 Sebastian Oberschwendtner, sebastian.oberschwendtner@gmail.com
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
""" Interact with the ADALM Pluto device.

## Description
Handles the device connection and data acquisition. Different devices are
supported by inheriting from the DeviceBase class.

### Details
- *File:*     `app.py`
- *Details:*  Python 3.11
- *Date:*     2023-06-11
- *Version:*  v1.0.0

### Author
Sebastian Oberschwendtner, :email: sebastian.oberschwendtner@gmail.com

---
## Code

---
"""
# === Imports ===
import numpy as np
import iio
import adi


# === Functions ===
def list_devices() -> tuple:
    """List all available devices.

    Returns:
        tuple: A list of all available devices.
    """
    return tuple(iio.scan_contexts().keys())


# === Classes ===


class Device:
    """Base class for all devices."""

    def __init__(self) -> None:
        """Initialize the device."""
        self.name: str = "unknown"
        self.id: str = -1
        self._device = None

    def is_connected(self) -> bool:
        """Check if the device is connected.

        Returns:
            bool: True if the device is connected, False otherwise.
        """
        return self._device is not None

    def connect(self) -> None:
        """Connect to the device.
        
        Note:
            This function needs to be implemented by the actual device class.

        Raises:
            NotImplementedError: This function needs to be implemented by the actual device class.
        """
        raise NotImplementedError("This function needs to be implemented by the actual device class.")

    def disconnect(self) -> None:
        """Disconnect from the device.

        Note:
            This function needs to be implemented by the actual device class.

        Raises:
            NotImplementedError: This function needs to be implemented by the actual device class.
        """
        raise NotImplementedError("This function needs to be implemented by the actual device class.")

    def acquire(self) -> np.ndarray:
        """Acquire data from the device.
        
        Returns:
            np.ndarray: The base always returns 0.
        """
        return np.zeros(1)


class RandomGenerator(Device):
    """This class generates random data for testing purposes."""

    def acquire(self) -> np.ndarray:
        """Acquire data from the device.

        Returns:
            np.ndarray: 1x1024 The acquired data.

        ---
        """
        return np.random.rand(1024)


class Pluto(Device):
    """This class interacts with the ADALM Pluto device."""
    def __init__(self) -> None:
        """Initialize the device."""
        super().__init__()
        self.name = "PlutoSDR"

    def connect(self) -> None:
        """Connect to the device."""
        try:
            self._device = adi.Pluto()
        # The pluto driver throws a generic exception if the device is not found
        except Exception as error: # pylint: disable=broad-except
            self._device = None
            raise IOError("Could not connect to device.") from error
        # if self._device is not None:
        #     self._device.rx_lo = 1000000000
        #     self._device.rx_rf_bandwidth = 20000000
        #     self._device.rx_buffer_size = 1024
        #     self._device.rx_enabled_channels = [0]
        #     self._device.rx_enabled = True

    def acquire(self):
        return self._device.rx().real
