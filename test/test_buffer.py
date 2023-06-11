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
""" Test the buffer module.

## Description
Contains the test group to test the buffer module.

### Details
- *File:*     `test_buffer.py`
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
import numpy as np

# Import the Unit Under Test
import plutostudio.core.buffer as UUT

# === Fixtures ===

# === Tests ===


class Test_Buffer():
    """Test group to test the buffer base class."""
    def test_default_init(self):
        """Test the default initialization of the buffer."""
        # Arrange
        # Act
        buffer = UUT.Buffer()

        # Assert
        assert buffer.size == 0
        assert buffer.capacity == 1000
        assert buffer.get().size == 1000
        assert (buffer.get() == 0).all()

    def test_custom_init(self):
        """Test the custom initialization of the buffer."""
        # Arrange
        # Act
        buffer = UUT.Buffer(100)

        # Assert
        assert buffer.size == 0
        assert buffer.capacity == 100
        assert buffer.get().size == 100
        assert (buffer.get() == 0).all()

    def test_clear(self):
        """Test the clear function of the buffer."""
        # Arrange
        buffer = UUT.Buffer()
        buffer._data.fill(1)

        # Act
        buffer.clear()

        # Assert
        assert buffer.size == 0
        assert buffer.capacity == 1000
        assert buffer.get().size == 1000
        assert (buffer.get() == 0).all()

class Test_FixedBuffer():
    """Test group to test the fixed buffer class."""
    def test_default_init(self):
        """Test the default initialization of the fixed buffer."""
        # Arrange
        # Act
        buffer = UUT.FixedBuffer()

        # Assert
        assert buffer.size == 0
        assert buffer.capacity == 1000
        assert buffer.get().size == 1000
        assert (buffer.get() == 0).all()

    def test_custom_init(self):
        """Test the custom initialization of the fixed buffer."""
        # Arrange
        # Act
        buffer = UUT.FixedBuffer(100)

        # Assert
        assert buffer.size == 0
        assert buffer.capacity == 100
        assert buffer.get().size == 100
        assert (buffer.get() == 0).all()

    def test_clear(self):
        """Test the clear function of the fixed buffer."""
        # Arrange
        buffer = UUT.FixedBuffer()
        buffer._data.fill(1)
        buffer._size = 1000

        # Act
        buffer.clear()

        # Assert
        assert buffer.size == 0
        assert buffer.capacity == 1000
        assert buffer.get().size == 1000
        assert (buffer.get() == 0).all()

    def test_put_single(self):
        """Test putting data in the fixed buffer."""
        # Arrange
        buffer = UUT.FixedBuffer(100)

        # Act
        buffer.put(42)

        # Assert
        assert buffer.size == 1
        assert buffer.get()[0] == 42
    
    def test_put_list(self):
        """Test putting data in the fixed buffer."""
        # Arrange
        buffer = UUT.FixedBuffer(100)

        # Act
        buffer.put([42, 43])

        # Assert
        assert buffer.size == 2
        assert buffer.get()[0] == 42
        assert buffer.get()[1] == 43

    def test_put_overflow(self):
        """Test the put function of the fixed buffer with overflow."""
        # Arrange
        buffer = UUT.FixedBuffer(10)
        data = np.arange(20)

        # Assert
        with pytest.raises(IndexError):
            # Act
            buffer.put(data)
            assert buffer.size == 10
            assert buffer.get()[9] == 9

    def test_put_list_and_clear(self):
        """Test putting data in the fixed buffer."""
        # Arrange
        buffer = UUT.FixedBuffer(10)

        # Act
        data = np.arange(10)
        buffer.put(data)
        buffer.clear()
        buffer.put(data+5)

        # Assert
        assert buffer.size == 10
        assert buffer.get()[0] == 5
        assert buffer.get()[9] == 14


class Test_CircularBuffer():
    """Test group to test the circular buffer class."""
    def test_default_init(self):
        """Test the default initialization of the circular buffer."""
        # Arrange
        # Act
        buffer = UUT.CircularBuffer()

        # Assert
        assert buffer.size == 0
        assert buffer.capacity == 1000
        assert buffer.get().size == 1000
        assert (buffer.get() == 0).all()

    def test_custom_init(self):
        """Test the custom initialization of the circular buffer."""
        # Arrange
        # Act
        buffer = UUT.CircularBuffer(100)

        # Assert
        assert buffer.size == 0
        assert buffer.capacity == 100
        assert buffer.get().size == 100
        assert (buffer.get() == 0).all()

    def test_clear(self):
        """Test the clear function of the circular buffer."""
        # Arrange
        buffer = UUT.CircularBuffer()
        buffer._data.fill(1)
        buffer._size = 1000

        # Act
        buffer.clear()

        # Assert
        assert buffer.size == 0
        assert buffer.capacity == 1000
        assert buffer.get().size == 1000
        assert (buffer.get() == 0).all()

    def test_put_single(self):
        """Test putting data in the circular buffer."""
        # Arrange
        buffer = UUT.CircularBuffer(100)

        # Act
        buffer.put(42)

        # Assert
        assert buffer.size == 1
        assert buffer.get()[0] == 42
    
    def test_put_list(self):
        """Test putting data in the circular buffer."""
        # Arrange
        buffer = UUT.CircularBuffer(100)

        # Act
        buffer.put([42, 43])

        # Assert
        assert buffer.size == 2
        assert buffer.get()[0] == 42
        assert buffer.get()[1] == 43

    def test_put_overflow(self):
        """Test the put function of the circular buffer with overflow."""
        # Arrange
        buffer = UUT.CircularBuffer(10)
        data = np.arange(20)

        # Act
        buffer.put(data)

        # Assert
        assert buffer.size == 10
        assert buffer.get()[0] == 10
        assert buffer.get()[9] == 19