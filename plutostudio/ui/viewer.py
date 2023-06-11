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
""" Viewer module for the PlutoStudio package.

## Description
This module contains different viewers which can be used within a layout
to display data in different styles.

### Details
- *File:*     `viewer.py`
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
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# === Classes ===


class Viewer:
    """Base class for all viewers."""

    def __init__(self, parent):
        """Initialize the viewer.

        Args:
            parent (object): The parent object to use for the viewer.

        ---
        """
        # Use dark style from matplotlib
        plt.style.use("dark_background")

        # Initialize the figure with the size of the parent
        _figure = plt.Figure(
            figsize=(parent.winfo_width(), parent.winfo_height()),
            dpi=100,
            layout="tight",
        )

        # Initialize the viewer frame
        self.canvas = FigureCanvasTkAgg(_figure, master=parent)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Add axes to the figure
        self.axes = self.canvas.figure.add_subplot(111)

        # Initialize data for blitting
        self._background = None
        self._artists = []

    def add_artist(self, art):
        """
        Add an artist to be managed.

        Args:
            art : Artist
            The artist to be added.  Will be set to 'animated' (just
            to be safe).  *art* must be in the figure associated with
            the canvas this class is managing.

        """
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        if event is not None:
            if event.canvas != self:
                raise RuntimeError
        # Scale axes to fit the data
        self.axes.relim()
        self.axes.autoscale_view()

        # Save the background
        self._background = self.canvas.copy_from_bbox(self.canvas.figure.bbox)
        self._draw_animated()

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for artist in self._artists:
            fig.draw_artist(artist)

    def _update(self):
        """Update the screen with animated artists."""
        fig = self.canvas.figure
        # paranoia in case we missed the draw event,
        if self._background is None:
            self.on_draw(None)
        else:
            # restore the background
            self.canvas.restore_region(self._background)
            # draw all of the animated artists
            self._draw_animated()
            # update the GUI state
            self.canvas.blit(fig.bbox)
        # let the GUI event loop process anything it has to do
        self.canvas.flush_events()


class DefaultViewer(Viewer):
    """Default viewer for the GUI."""

    def __init__(self, parent):
        """Initialize the default viewer.

        Args:
            parent (object): The parent object to use for the viewer.

        ---
        """
        super().__init__(parent)
        self.last_update = time.perf_counter()
        (self.trace,) = self.axes.plot([0, 1000], [0, 1], "o", c="y")
        self.fps_counter = self.axes.text(
            0,
            1.0,
            "FPS: 0.00",
            fontsize=20,
            fontweight="bold",
        )
        self.add_artist(self.trace)
        self.add_artist(self.fps_counter)

    def draw(self, data):
        """Update the viewer.

        Args:
            data (list): The data to display.

        ---
        """
        # Update the data
        self.trace.set_data(range(len(data)), data)

        # Update the FPS counter
        now = time.perf_counter()
        fps = 1 / (now - self.last_update)
        self.fps_counter.set_text(f"FPS: {fps:.2f}")
        self.last_update = now

        # Update the viewer
        super()._update()
