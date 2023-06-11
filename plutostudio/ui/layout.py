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
"""Layouts for the GUI.

## Description
This module collects all the layouts for the GUI.

### Details
- *File:*     `layout.py`
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
import ttkbootstrap as ttk

# === Classes ===


class Layout:
    """Base class for all layouts."""

    def __init__(self, parent, **kwargs):
        # Initialize the content frame
        self.content = ttk.Frame(parent, **kwargs)
        self.content.grid(row=0, column=0, sticky="nsew")

        # Configure the grid the be resizable
        self.content.master.grid_rowconfigure(0, weight=1)
        self.content.master.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(2, weight=1)
        self.content.grid_columnconfigure(3, weight=1)

        # Add a frame for the plot
        self.view_frame = ttk.Frame(self.content, padding=10)
        self.view_frame.grid(row=0, column=0, sticky="nsew")
        self.view_frame.grid_rowconfigure(0, weight=1)
        self.view_frame.grid_columnconfigure(0, weight=1)

        # Add start and stop callback
        self._start_callback = None
        self._stop_callback = None

    def register_start_callback(self, callback):
        """Register a callback for the start button.

        Args:
            callback (function): The callback function to register.
        """
        self._start_callback = callback

    def register_stop_callback(self, callback):
        """Register a callback for the stop button.

        Args:
            callback (function): The callback function to register.
        """
        self._stop_callback = callback


class DefaultLayout(Layout):
    """Default layout for the GUI.

    Args:
        parent (object): The tkinter object to use as parent.
    """

    def __init__(self, parent, **kwargs):
        """Initialize the DefaultLayout.

        Args:
            parent (object): The parent tkinter object.

        ---
        """
        # Initialize the content
        super().__init__(parent, **kwargs)

        # Add buttons
        self.buttons = {
            "Run": ttk.Button(
                self.content,
                text="Run",
                bootstyle="success",
                command=self._on_button_run,
                takefocus=False,
            ),
            "Stop": ttk.Button(
                self.content,
                text="Stop",
                bootstyle="danger",
                command=self._on_button_stop,
                takefocus=False,
                state="disabled",
            ),
            "Quit": ttk.Button(
                self.content,
                text="Quit",
                bootstyle="outline",
                command=self.content.master.destroy,
                takefocus=False,
            ),
        }

        # Position the buttons
        self.buttons["Run"].grid(row=0, column=0, sticky="w")
        self.buttons["Stop"].grid(row=0, column=1, sticky="w")
        self.buttons["Quit"].grid(row=0, column=3, sticky="e")

        # Add the separators
        self.separators = []
        self.separators.append(ttk.Separator(self.content, orient="horizontal"))
        self.separators.append(ttk.Separator(self.content, orient="vertical"))
        self.separators[0].grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)
        self.separators[1].grid(row=0, column=2, rowspan=3, sticky="nsew", padx=10)

        # Position the viewer
        self.view_frame.grid(row=2, column=3, sticky="nsew")

    def _on_button_run(self):
        """Action when Run button is pressed."""
        # Disable the run button and enable the stop button
        self.buttons["Run"]["state"] = "disabled"
        self.buttons["Stop"]["state"] = "normal"

        # Call the start callback
        if self._start_callback is not None:
            self._start_callback()

    def _on_button_stop(self):
        """Action when Stop button is pressed."""
        # Disable the stop button and enable the run button
        self.buttons["Run"]["state"] = "normal"
        self.buttons["Stop"]["state"] = "disabled"

        # Call the stop callback
        if self._stop_callback is not None:
            self._stop_callback()
