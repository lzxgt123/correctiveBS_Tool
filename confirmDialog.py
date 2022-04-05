# .-*- coding: utf-8 -*-
# .FileName:confirmDialog
# .Date....:2022-04-04 : 17 :09
# .Author..:Qian binJie
# .Contact.:1075064966@qq.com
'''
launch :
        import confirmDialog as QBJ_confirmDialog
        reload(QBJ_confirmDialog)
'''
from PySide2 import QtWidgets,QtCore,QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


def maya_main_window():
    '''
        返回maya主窗口，使之变成一个python对象
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class confirm_Dialog(QtWidgets.QDialog):

    def __init__(self,parent=maya_main_window()):
        super(confirm_Dialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)


    def addBlendShapeConfirmDialog(self,yesCommand):
        self.addBlendShapeConfirm_Dialog = QtWidgets.QDialog()
        self.addBlendShapeConfirm_Dialog.setWindowTitle('Add blendShape')
        self.addBlendShapeConfirm_Dialog.setFixedSize(200, 80)
        main_Layout = QtWidgets.QVBoxLayout(self.addBlendShapeConfirm_Dialog)
        main_Layout.setContentsMargins(4, 4, 4, 4)
        label_Layout = QtWidgets.QVBoxLayout()
        button_Layout = QtWidgets.QHBoxLayout()
        button_Layout.setContentsMargins(2, 2, 2, 2)
        button_Layout.setSpacing(10)
        confirm_Label_01 = QtWidgets.QLabel("Can't find blendShape Node ,")
        confirm_Label_01.setAlignment(QtCore.Qt.AlignCenter)
        confirm_Label_02 = QtWidgets.QLabel("Add or not ?")
        confirm_Label_02.setAlignment(QtCore.Qt.AlignCenter)
        yes_Btn = QtWidgets.QPushButton('Yes')
        yes_Btn.setFixedSize(80, 20)
        No_Btn = QtWidgets.QPushButton('No')
        No_Btn.setFixedSize(80, 20)
        yes_Btn.clicked.connect(yesCommand)
        No_Btn.clicked.connect(self.addBlendShapeConfirm_Dialog.close)
        label_Layout.addWidget(confirm_Label_01)
        label_Layout.addWidget(confirm_Label_02)
        button_Layout.addWidget(yes_Btn)
        button_Layout.addWidget(No_Btn)
        main_Layout.addLayout(label_Layout)
        main_Layout.addLayout(button_Layout)
        self.addBlendShapeConfirm_Dialog.exec_()


    def loadTargetConfirmDialog(self,yesCommand):
        self.loadTargetConfirm_Dialog = QtWidgets.QDialog()
        self.loadTargetConfirm_Dialog.setWindowTitle('Load target')
        self.loadTargetConfirm_Dialog.setFixedSize(200, 80)
        main_Layout = QtWidgets.QVBoxLayout(self.loadTargetConfirm_Dialog)
        main_Layout.setContentsMargins(4, 4, 4, 4)
        label_Layout = QtWidgets.QVBoxLayout()
        button_Layout = QtWidgets.QHBoxLayout()
        button_Layout.setContentsMargins(2, 2, 2, 2)
        button_Layout.setSpacing(10)
        confirm_Label_01 = QtWidgets.QLabel("Already have target Geo ,")
        confirm_Label_01.setAlignment(QtCore.Qt.AlignCenter)
        confirm_Label_02 = QtWidgets.QLabel("Change or not ?")
        confirm_Label_02.setAlignment(QtCore.Qt.AlignCenter)
        yes_Btn = QtWidgets.QPushButton('Yes')
        yes_Btn.setFixedSize(80, 20)
        No_Btn = QtWidgets.QPushButton('No')
        No_Btn.setFixedSize(80, 20)
        yes_Btn.clicked.connect(yesCommand)
        No_Btn.clicked.connect(self.loadTargetConfirm_Dialog.close)
        label_Layout.addWidget(confirm_Label_01)
        label_Layout.addWidget(confirm_Label_02)
        button_Layout.addWidget(yes_Btn)
        button_Layout.addWidget(No_Btn)
        main_Layout.addLayout(label_Layout)
        main_Layout.addLayout(button_Layout)
        self.loadTargetConfirm_Dialog.exec_()

