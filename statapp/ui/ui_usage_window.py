# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Maxim Slipenko, Eugene Lazurenko.
#
# This file is part of Statapp
# (see https://github.com/shizand/statapp).
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


################################################################################
## Form generated from reading UI file 'usage_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_UsageWindow(object):
    def setupUi(self, UsageWindow):
        if not UsageWindow.objectName():
            UsageWindow.setObjectName(u"UsageWindow")
        UsageWindow.resize(400, 300)
        self.gridLayout = QGridLayout(UsageWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.browserContainer = QVBoxLayout()
        self.browserContainer.setObjectName(u"browserContainer")

        self.gridLayout.addLayout(self.browserContainer, 0, 0, 1, 1)


        self.retranslateUi(UsageWindow)

        QMetaObject.connectSlotsByName(UsageWindow)
    # setupUi

    def retranslateUi(self, UsageWindow):
        UsageWindow.setWindowTitle(QCoreApplication.translate("UsageWindow", u"\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0435", None))
    # retranslateUi
