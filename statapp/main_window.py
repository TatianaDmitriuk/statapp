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
from PySide2 import QtCore
from PySide2.QtCore import Slot, Qt, QPoint
from PySide2.QtWidgets import QMainWindow, QMessageBox, QAction, QMenu

from statapp.calculations import generateXValues, generateYValues
from statapp.constants import NUMBERS_PRECISION
from statapp.distribution_window import NormalDistributionWindow, UniformDistributionWindow, \
    ExponentialDistributionWindow
from statapp.generate_factor_window import GenerateFactorWindow
from statapp.polynoms.linear_polynom_window import LinearPolynomWindow
from statapp.mathtex_header_view import MathTexHeaderView
from statapp.models.input_values_model import InputValuesModel
from statapp.generate_window import GenerateWindow
from statapp.about_window import AboutWindow
from statapp.models.fileslc_model import FileSLCModel
from statapp.polynoms.squared_polynom_window import SquaredPolynomWindow
from statapp.ui.ui_main_window import Ui_MainWindow
from statapp.usage_window import UsageWindow
from statapp.utils import buildMessageBox, addIcon, FloatDelegate, onError
from statapp.variance_analysis import VarianceAnalysisWindow
from statapp.correlation_analysis import CorrelationAnalysisWindow
from statapp.polynoms.transform_polynom_window import TransformPolynomWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        addIcon(self)

        self.mainActions = [
            self.ui.varianceAnalysisAction,
            self.ui.correlationAnalisisAction,
            self.ui.linearPolynomAction,
            self.ui.squaredPolynomAction,
            self.ui.transformPolynomAction,
        ]

        self.aboutWindow = None
        self.usageWindow = None

        self.isDataChanged = False
        self.model = InputValuesModel()
        self.fileModel = FileSLCModel()
        self.ui.tableView.setItemDelegate(FloatDelegate())
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setHorizontalHeader(
            MathTexHeaderView(self.ui.tableView, orientation=QtCore.Qt.Horizontal)
        )
        self.model.layoutChanged.connect(self.updateActionsEnabled)
        self.updateActionsEnabled()
        #
        # Для быстрой отладки
        # n = 10
        # y = generateYValues(100, 5, n)
        # x1 = generateXValues(20, 2, 0, y)
        # x2 = generateXValues(10, 1, 0, y)
        # self.model.updateAllData(np.concatenate([y, x1, x2], axis=1))
        self.ui.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView.horizontalHeader().customContextMenuRequested.connect(self.removeColumn)


    def removeColumn(self, event: QPoint):
        menu = QMenu(self)

        col = self.ui.tableView.columnAt(event.x())

        if col == 0:
            return

        def fun():
            self.model.removeCol(col)
            self.isDataChanged = True

        selectAction = QAction("Удалить", self)
        selectAction.triggered.connect(fun)
        menu.addAction(selectAction)
        menu.exec_(self.ui.tableView.mapToGlobal(event))



    def updateActionsEnabled(self):
        data = self.model.getData()

        # есть только отклик
        if data.shape[1] == 1:
            self.ui.generateXaction.setEnabled(True)
            self.ui.uniformDistributionAction.setEnabled(True)
            self.ui.normalDistributionAction.setEnabled(True)
            self.ui.exponentialDistributionAction.setEnabled(True)
            self.setEnabledMainActions(False)
        # есть отклик и фактор(ы)
        elif data.shape[1] > 1:
            self.ui.generateXaction.setEnabled(True)
            self.ui.uniformDistributionAction.setEnabled(True)
            self.ui.normalDistributionAction.setEnabled(True)
            self.ui.exponentialDistributionAction.setEnabled(True)
            self.setEnabledMainActions(True)
        else:
            self.ui.generateXaction.setEnabled(False)
            self.ui.uniformDistributionAction.setEnabled(False)
            self.ui.normalDistributionAction.setEnabled(False)
            self.ui.exponentialDistributionAction.setEnabled(False)
            self.setEnabledMainActions(False)


    def setEnabledMainActions(self, enabled):
        for action in self.mainActions:
            action.setEnabled(enabled)

    @Slot()
    def on_openfileaction_triggered(self):
        try:
            currentData = self.model.getData()
            data = np.array([])
            if currentData.size > 1:
                file = ''
                if self.fileModel.fileName:
                    file = '\nФайл сохранения: ' + self.fileModel.fileName

                msgBox = buildMessageBox \
                    ('Сохранение данных',
                     "Сохранить данные?" + file,
                     QMessageBox.Question,
                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                     QMessageBox.Cancel)

                reply = msgBox.exec_()
                if reply == QMessageBox.StandardButton.Yes:
                    self.fileModel.saveFile(self.model.getData())

                    data = self.fileModel.loadFile()
                    if data is not None and data.shape[0] > 0:
                        self.model.updateAllData(data)
                        self.isDataChanged = False
                elif reply == QMessageBox.StandardButton.Cancel:
                    return
                else:
                    data = self.fileModel.loadFile()
                    if data is not None and data.shape[0] > 0:
                        self.model.updateAllData(data)
                        self.isDataChanged = False
            else:
                data = self.fileModel.loadFile()
                if data is not None and data.shape[0] > 0:
                    self.model.updateAllData(data)
                    self.isDataChanged = False
        except Exception as error:
            onError(error)


    @Slot()
    def on_savefileaction_triggered(self):
        try:
            self.isDataChanged = not self.fileModel.saveFile(self.model.getData())
        except Exception as error:
            onError(error)

    @Slot()
    def on_closefileaction_triggered(self):
        try:
            self.fileModel.closeFile()
            self.isDataChanged = False
        except Exception as error:
            onError(error)

    @Slot()
    def on_generateYaction_triggered(self):
        try:
            gw = GenerateWindow()

            if gw.exec():
                y = generateYValues(gw.mat, gw.deviation, gw.count)
                self.model.updateAllData(y.round(NUMBERS_PRECISION))
                self.isDataChanged = True
        except Exception as error:
            onError(error)

    @Slot()
    def on_generateXaction_triggered(self):
        try:
            gfw = GenerateFactorWindow()

            if gfw.exec():
                data = self.model.getData()
                y = self.model.getY()
                xValues = generateXValues(gfw.mat, gfw.deviation, gfw.typeConnection, y)
                data = np.concatenate((data, xValues.round(NUMBERS_PRECISION)), axis=1)
                self.model.updateAllData(data)
                self.isDataChanged = True
        except Exception as error:
            onError(error)

    @Slot()
    def on_aboutmenuaction_triggered(self):
        self.aboutWindow = AboutWindow()
        self.aboutWindow.show()

    @Slot()
    def on_usageaction_triggered(self):
        self.usageWindow = UsageWindow()
        self.usageWindow.show()

    @Slot()
    def on_varianceAnalysisAction_triggered(self):
        try:
            dw = VarianceAnalysisWindow(self.model.getData())
            dw.exec()
        except Exception as error:
            onError(error)

    @Slot()
    def on_correlationAnalisisAction_triggered(self):
        try:
            dw = CorrelationAnalysisWindow(self.model.getData())
            dw.exec()
        except Exception as error:
            onError(error)

    @Slot()
    def on_linearPolynomAction_triggered(self):
        try:
            dw = LinearPolynomWindow(self.model.getData())
            dw.exec()
        except Exception as error:
            onError(error)

    @Slot()
    def on_squaredPolynomAction_triggered(self):
        try:
            dw = SquaredPolynomWindow(self.model.getData())
            dw.exec()
        except Exception as error:
            onError(error)

    @Slot()
    def on_transformPolynomAction_triggered(self):
        try:
            dw = TransformPolynomWindow(self.model.getData())
            dw.exec()
        except Exception as error:
            onError(error)

    @Slot()
    def on_uniformDistributionAction_triggered(self):
        try:
            dw = UniformDistributionWindow(self.model.getData())
            dw.exec()
        except Exception as error:
            onError(error)

    @Slot()
    def on_normalDistributionAction_triggered(self):
        try:
            dw = NormalDistributionWindow(self.model.getData())
            dw.exec()
        except Exception as error:
            onError(error)

    @Slot()
    def on_exponentialDistributionAction_triggered(self):
        try:
            dw = ExponentialDistributionWindow(self.model.getData())
            dw.exec()
        except Exception as error:
            onError(error)

    def closeEvent(self, event):
        if self.isDataChanged:
            file = ''
            if self.fileModel.fileName:
                file = '\nФайл сохранения: ' + self.fileModel.fileName

            msgBox = buildMessageBox \
                ('Завершение работы',
                 "Сохранить данные?" + file,
                 QMessageBox.Question,
                 QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                 QMessageBox.Cancel)

            reply = msgBox.exec_()
            if reply == QMessageBox.StandardButton.Yes:
                self.fileModel.saveFile(self.model.getData())
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
