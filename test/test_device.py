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
""" Test the device module.

## Description
Contains the test group to test the device module.

### Details
- *File:*     `test_device.py`
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
import pytest

# Import the module to test
import plutostudio.core.device as UUT

# === Fixtures ===
@pytest.fixture
def PlutoMock(mocker):
    """Mock adi.Pluto() class."""
    yield mocker.patch("adi.Pluto")


# === Tests ===


class Test_DeviceBase:
    """Test group to test the DeviceBase class."""

    @pytest.mark.slow()
    def test_list_devices(self):
        """Test the list_devices function."""
        assert isinstance(UUT.list_devices(), tuple)

    def test_device_init(self):
        """Test the initial state of a device."""
        # Arrange
        # Act
        device = UUT.Device()

        # Assert
        assert device.name == "unknown"
        assert device.id == -1
        assert device.is_connected() is False
        assert device._device is None

    def test_device_connect(self):
        """ Test exception when trying to call connect on the base class."""
        # Arrange
        device = UUT.Device()

        # Act
        with pytest.raises(NotImplementedError):
            device.connect()

    def test_device_disconnect(self):
        """ Test exception when trying to call disconnect on the base class."""
        # Arrange
        device = UUT.Device()

        # Act
        with pytest.raises(NotImplementedError):
            device.disconnect()

    def test_acquire(self):
        """ The base device should always return 0."""
        # Arrange
        device = UUT.Device()

        # Act
        assert device.acquire() == 0

class Test_PlutoDevice():
    """Test group to test the PlutoDevice class."""

    def test_device_init(self, PlutoMock):
        """Test the initial state of a device."""
        # Arrange
        # Act
        device = UUT.Pluto()

        # Assert
        assert device.name == "PlutoSDR"
        assert device.id == -1
        assert device.is_connected() is False
        assert device._device is None

    def test_device_connect(self, PlutoMock):
        """Test the connect function."""
        # Arrange
        device = UUT.Pluto()

        # Act
        device.connect()

        # Assert
        assert PlutoMock.call_count == 1
        assert device.is_connected() is True
