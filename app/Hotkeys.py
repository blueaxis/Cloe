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

from Workers import WorkerSignal


class HotKeys(GlobalHotKeys):

    def __init__(self, hotkeys, *args, **kwargs):
        for h in hotkeys:
            obj, func = hotkeys[h]
            hotkeys[h] = lambda o=obj, f=func: self.onPress(o, f)
        super().__init__(hotkeys, *args, **kwargs)
        self.signals = WorkerSignal()

    def onPress(self, obj, func):
        self.signals.result.emit((obj, func))
