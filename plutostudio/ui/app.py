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
""" Main application

## Description
This file contains the main application window for the PlutoPy application.
Run this file to start the application with the default layout.

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
from threading import Thread, Event
import ttkbootstrap as ttk
from plutostudio import __version__
from plutostudio.core.device import Pluto
from plutostudio.core.buffer import CircularBuffer as Buffer
from .layout import DefaultLayout
from .viewer import DefaultViewer


class PlutoApp(ttk.Window):
    """The main application window.

    This class runs the main application window and is intended to run
    the main application loop.

    Args:
        ttk (Window): The ttk.Window to use as parent.
    """

    def __init__(self):
        """Initialize the main application window.

        This function initializes the main application window and
        is intended to run the main application loop.
        """
        # Initialize the main window
        super().__init__(themename="darkly")
        self.title(f"Pluto Studio - v{__version__}")
        self.geometry("1920x1080")
        self.resizable(False, False)
        self._stop_event = Event()

        # Add the layout
        self.layout = DefaultLayout(self, padding=10)
        self.layout.register_start_callback(self.start_acquisition)
        self.layout.register_stop_callback(self.stop_acquisition)

        # Add the viewer
        self.viewer = DefaultViewer(self.layout.view_frame)

        # Add the device
        self.device = Pluto()

        # Add data buffer
        self.buffer = Buffer(1024)

        # Add the acquisition thread
        self.acquisition_thread = None

    def destroy(self) -> None:
        """Destroy the main application window."""
        # Disconnect the device
        if self.device.is_connected():
            self.device.disconnect()

        # Stop the acquisition thread
        self.stop_acquisition()

        # Give the thread time to stop and destroy the window
        return super().after(100, super().destroy)

    def start_acquisition(self):
        """Start the data acquisition."""
        self._stop_event.clear()
        Thread(target=self.acquisition_loop).start()

    def stop_acquisition(self):
        """Stop the data acquisition."""
        self._stop_event.set()

    def acquisition_loop(self):
        """The acquisition loop."""
        while not self._stop_event.is_set():
            # self.buffer.clear()
            self.buffer.put(self.device.acquire())
            self.viewer.draw(self.buffer.get())
