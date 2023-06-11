#!/usr/bin/env python
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
""" Run the PlutoStudio application.

## Description
Main entry point for the PlutoStudio application.

### Details
- *File:*     `PlutoStudio.py`
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
import sys
from plutostudio.ui.app import PlutoApp

# === Main ===
def main() -> int:
    """Main entry point for the PlutoStudio application."""
    # Create the app
    app = PlutoApp()

    # Run the app
    app.mainloop()

    # Return success
    return 0

# Run the application
if __name__ == "__main__":
    # Run the main function
    sys.exit(main())