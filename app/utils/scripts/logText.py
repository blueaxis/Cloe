"""
Cloe Helper Functions

Copyright (C) `2021-2022` `<Alarcon Ace Belen>`

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from os import path as osPath

from PyQt5.QtGui import QGuiApplication


def logText(text: str, *, saveLog=False, path=".") -> None:
    """Helper function to log text

    Args:
        text (str): Text to log
        saveLog (bool, optional): Save text to a file if enabled. Defaults to False.
        path (str, optional): Log file location. Defaults to current path.
    """
    clipboard = QGuiApplication.clipboard()
    clipboard.setText(text)

    if saveLog:
        filename = "log.txt"
        with open(osPath.join(path, filename), "a", encoding="utf-8") as fh:
            fh.write(text + "\n")
