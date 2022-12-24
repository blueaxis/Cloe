"""
Cloe Global Hotkeys

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

from pynput.keyboard import GlobalHotKeys
from PyQt5.QtCore import QObject

from .workers import BaseWorkerSignal

class Hotkeys(GlobalHotKeys):
    """Listener to support global hotkeys

    Args:
        hotkeys (dict[str, tuple[QObject, Callable]]): See detailed description below

    hotkeys is a [str, tuple] dictionary with the following scheme:
        h (str): Hotkey combination
        tuple[obj (QObject), fn (str)]: Object/widget with function named fn    
    """
    def __init__(self, hotkeys: dict[str, tuple[QObject, str]], *args, **kwargs):
        for h in hotkeys:
            obj, fn = hotkeys[h]
            hotkeys[h] = lambda obj=obj, fn=fn: self.onPress(obj, fn)
        super().__init__(hotkeys, *args, **kwargs)
        self.signals = BaseWorkerSignal()

    def onPress(self, obj: QObject, fn: str):
        self.signals.result.emit((obj, fn))
