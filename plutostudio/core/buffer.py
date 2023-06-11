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
""" Different buffers for the application.

## Description
The buffer module contains different buffers to exchange data between the
device and the GUI. Different buffer modes are available to fit the
desired update behavior in the GUI.

### Details
- *File:*     `buffer.py`
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

# === Classes ===


class Buffer:
    """Base class for all buffers.

    This class provides a basic interface to exchange data between the
    different modules of the application.
    """

    @property
    def size(self) -> int:
        """Get the size of the buffer.

        Returns:
            int: The size of the buffer.
        """
        return self._size

    @property
    def capacity(self) -> int:
        """Get the capacity of the buffer.

        Returns:
            int: The capacity of the buffer.
        """
        return self._capacity

    def __init__(self, max_capacity: int = 1000) -> None:
        """Initialize the buffer.

        Args:
            max_capacity (int, optional): The maximum capacity of the buffer. Defaults to 1000.

        ---
        """
        self._size: int = 0
        self._capacity: int = max_capacity
        self._data = np.zeros(max_capacity)

    def get(self) -> np.ndarray:
        """Get data from the buffer.

        Note:
            This function should be overwritten by the inheriting class.

        Returns:
            np.array: The data from the buffer.
        """
        # Return the data
        return self._data.view()

    def clear(self) -> None:
        """Clear the buffer."""
        # Clear data
        self._data.fill(0)

        # Reset size
        self._size = 0


class FixedBuffer(Buffer):
    """This class implements a fixed buffer.

    This buffer has a fixed size and will raise an exception when it is full.

    Raises:
        IndexError: The buffer is full and cannot accept more data.
    """

    def put(self, data: float | list) -> None:
        """Put data in the buffer.

        Args:
            data (float | list): The data to put in the buffer.

        Raises:
            ValueError: _description_

        ---
        """
        # Put the data in the buffer
        try:
            self._data[self._size] = data
            self._size += 1
        # If the data is a list, put each element in the buffer
        except ValueError:
            for value in data:
                self.put(value)


class CircularBuffer(Buffer):
    """This class implements a circular buffer.

    This buffer has a fixed size and will overwrite the oldest data when it is full.
    """

    def put(self, data: float | list) -> None:
        """Put data in the buffer.

        Args:
            data (float | list): The data to put in the buffer.

        Raises:
            ValueError: _description_

        ---
        """
        # Put the data in the buffer
        try:
            self._data[self._size] = data
            self._size += 1
        # Wrap around if the buffer is full
        except IndexError:
            self._size = 0
            self.put(data)
        # If the data is a list, put each element in the buffer
        except ValueError:
            for value in data:
                self.put(value)
