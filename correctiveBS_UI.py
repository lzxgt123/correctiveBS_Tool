# .-*- coding: utf-8 -*-
# .FileName:correctiveBS_UI
# .Date....:2022-03-21 : 11 :10
# .Aurhor..:Qian binjie
# .Contact.:1075064966@qq.com
'''
launch :
        import correctiveBS_UI as QBJ_correctiveBS_UI
        reload(QBJ_correctiveBS_UI)
'''

import pymel.core as pm
import maya.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets,QtCore,QtGui


def maya_main_window():
    '''
        返回maya主窗口，使之变成一个python对象
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class CorrectiveBSUI(QtWidgets.QDialog):

    BUTTON_BGC = "background-color:rgb(142,188,255);color:black;"
    WINDOW_TITLE = 'Corrective BS v1.0.0'
    limitAngleExpr = QtCore.QRegExp('^-?(180|([1-9]?\d|1[0-7][0-9])(\.\d{1,2})?)$')

    def __init__(self,parent=maya_main_window()):
        super(CorrectiveBSUI, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint)
        self.showUI()


    def showUI(self):
        if cmds.window(self.WINDOW_TITLE, exists=True):
            cmds.deleteUI(self.WINDOW_TITLE)

        # 设置窗口对象名称
        self.setObjectName(self.WINDOW_TITLE)
        # 设置窗口标题
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setFixedSize(415, 530)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.show()

    def create_widgets(self):
        pass


    def create_layouts(self):
        pass


    def create_connections(self):
        pass