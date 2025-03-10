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
import numpy as np
from PySide2.QtCore import QModelIndex

from statapp.models.editable_table_model import EditableTableModel
from statapp.models.utils import yxHeader


class InputValuesModel(EditableTableModel):
    def __init__(self, data=np.array([[]], dtype=np.float32)):
        super().__init__(data)

    def getHorizontalHeader(self):
        return yxHeader(self.columnCount(QModelIndex()))

    def getY(self):
        return self._data[:, 0]

    def removeCol(self, index: int):
        self.updateAllData(np.delete(self._data, index, axis=1))
