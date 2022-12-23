"""
Cloe Multithreaded Workers

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

from typing import Callable

from PyQt5.QtCore import (QRunnable, pyqtSlot)

from .signals import BaseWorkerSignal

class BaseWorker(QRunnable):
    def __init__(self, fn: Callable, *args, **kwargs):
        super(BaseWorker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = BaseWorkerSignal()

    @pyqtSlot()
    def run(self):
        output = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(output)
        self.signals.finished.emit()
