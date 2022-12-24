"""
Cloe

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

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from components.windows import SystemTray
from utils.constants import APP_LOGO, APP_NAME, STYLESHEET_DEFAULT

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(APP_LOGO))
    app.setQuitOnLastWindowClosed(False)

    widget = SystemTray()

    styles = STYLESHEET_DEFAULT
    with open(styles, "r") as fh:
        app.setStyleSheet(fh.read())

    widget.show()
    widget.loadModel()
    app.exec_()
    sys.exit()
