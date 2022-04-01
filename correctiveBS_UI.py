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
        self.setFixedSize(470, 740)


        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.show()


    def create_widgets(self):
        # 创建加载Base_Geo 组件
        self.baseGeo_Label = QtWidgets.QLabel('Base Geo:')
        self.baseGeo_LineEdit = QtWidgets.QLineEdit()
        self.baseGeo_LineEdit.setReadOnly(True)
        self.baseGeo_Btn = QtWidgets.QPushButton('Load')

        # 创建加载Ori_Geo 组件
        self.oriGeo_Label = QtWidgets.QLabel('Ori Geo:')
        self.oriGeo_LineEdit = QtWidgets.QLineEdit()
        self.oriGeo_LineEdit.setReadOnly(True)
        self.oriGeo_Btn = QtWidgets.QPushButton('Load')

        # 创建加载blendShape 组件
        self.blendshape_Label = QtWidgets.QLabel('blendShape:')
        self.blendshape_comboBox = QtWidgets.QComboBox()
        self.add_Btn = QtWidgets.QPushButton('Add')
        self.del_Btn = QtWidgets.QPushButton('Del')

        # 创建分割线 组件
        self.separator_01 = QtWidgets.QFrame()
        self.separator_01.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_01.setFrameShadow(QtWidgets.QFrame.Sunken)

        # 创建 控制器类型 组件
        self.controlsType_Label = QtWidgets.QLabel('Type:')
        # self.spacerItem_01 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
        #                                            QtWidgets.QSizePolicy.Minimum)
        self.adv_radioBtn = QtWidgets.QRadioButton('ADV')
        self.adv_radioBtn.setChecked(True)
        self.defined_radionBtn = QtWidgets.QRadioButton('Defined')
        self.defined_radionBtn.setEnabled(False)

        self.radionBtn_Grp = QtWidgets.QButtonGroup()
        self.radionBtn_Grp.addButton(self.adv_radioBtn,1)
        self.radionBtn_Grp.addButton(self.defined_radionBtn,2)

        # 创建tabWidget内 组件
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setStyleSheet("QTabBar::tab{width:70} QTabBar::tab{height:20}")
        self.tabWidget.setCurrentIndex(1)

        self.arm_Tab = QtWidgets.QWidget(self.tabWidget)
        self.arm_Layout = QtWidgets.QVBoxLayout(self.arm_Tab)
        self.arm_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.arm_Layout.setContentsMargins(2, 2, 2, 2)
        self.arm_Layout.setSpacing(3)
        self.arm_CreateBtn = QtWidgets.QPushButton('Create Targets')
        self.arm_Splitter = QtWidgets.QSplitter(self.arm_Tab)
        self.arm_Splitter.setMinimumSize(QtCore.QSize(400, 0))
        self.arm_Splitter.setOrientation(QtCore.Qt.Vertical)
        self.arm_ListWidget_01 = QtWidgets.QListWidget(self.arm_Splitter)
        self.arm_ListWidget_02 = QtWidgets.QListWidget(self.arm_Splitter)
        self.arm_Layout.addWidget(self.arm_CreateBtn)
        self.arm_Layout.addWidget(self.arm_Splitter)
        self.tabWidget.addTab(self.arm_Tab,'Arm')

        self.leg_Tab = QtWidgets.QWidget(self.tabWidget)
        self.leg_Layout = QtWidgets.QVBoxLayout(self.leg_Tab)
        self.leg_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.leg_Layout.setContentsMargins(2, 2, 2, 2)
        self.leg_Layout.setSpacing(3)
        self.leg_CreateBtn = QtWidgets.QPushButton('Create Targets')
        self.leg_Splitter = QtWidgets.QSplitter(self.leg_Tab)
        self.leg_Splitter.setMinimumSize(QtCore.QSize(400, 0))
        self.leg_Splitter.setOrientation(QtCore.Qt.Vertical)
        self.leg_ListWidget_01 = QtWidgets.QListWidget(self.leg_Splitter)
        self.leg_ListWidget_02 = QtWidgets.QListWidget(self.leg_Splitter)
        self.leg_Layout.addWidget(self.leg_CreateBtn)
        self.leg_Layout.addWidget(self.leg_Splitter)
        self.tabWidget.addTab(self.leg_Tab, 'leg')

        self.finger_Tab = QtWidgets.QWidget(self.tabWidget)
        self.finger_Layout = QtWidgets.QVBoxLayout(self.finger_Tab)
        self.finger_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.finger_Layout.setContentsMargins(2, 2, 2, 2)
        self.finger_Layout.setSpacing(3)
        self.finger_CreateBtn = QtWidgets.QPushButton('Create Targets')
        self.finger_Splitter = QtWidgets.QSplitter(self.finger_Tab)
        self.finger_Splitter.setMinimumSize(QtCore.QSize(400, 0))
        self.finger_Splitter.setOrientation(QtCore.Qt.Vertical)
        self.finger_ListWidget_01 = QtWidgets.QListWidget(self.finger_Splitter)
        self.finger_ListWidget_02 = QtWidgets.QListWidget(self.finger_Splitter)
        self.finger_Layout.addWidget(self.finger_CreateBtn)
        self.finger_Layout.addWidget(self.finger_Splitter)
        self.tabWidget.addTab(self.finger_Tab, 'finger')

        self.torso_Tab = QtWidgets.QWidget(self.tabWidget)
        self.torso_Layout = QtWidgets.QVBoxLayout(self.torso_Tab)
        self.torso_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.torso_Layout.setContentsMargins(2, 2, 2, 2)
        self.torso_Layout.setSpacing(3)
        self.torso_CreateBtn = QtWidgets.QPushButton('Create Targets')
        self.torso_Splitter = QtWidgets.QSplitter(self.torso_Tab)
        self.torso_Splitter.setMinimumSize(QtCore.QSize(400, 0))
        self.torso_Splitter.setOrientation(QtCore.Qt.Vertical)
        self.torso_ListWidget_01 = QtWidgets.QListWidget(self.torso_Splitter)
        self.torso_ListWidget_02 = QtWidgets.QListWidget(self.torso_Splitter)
        self.torso_Layout.addWidget(self.torso_CreateBtn)
        self.torso_Layout.addWidget(self.torso_Splitter)
        self.tabWidget.addTab(self.torso_Tab, 'torso')


        # 创建控制器旋转数值显示 组件
        self.rotate_Label = QtWidgets.QLabel('Rotate:')
        self.rotate_LineEdit_01 = QtWidgets.QLineEdit()
        self.rotate_LineEdit_01.setReadOnly(True)
        self.rotate_LineEdit_02 = QtWidgets.QLineEdit()
        self.rotate_LineEdit_02.setReadOnly(True)
        self.rotate_LineEdit_03 = QtWidgets.QLineEdit()
        self.rotate_LineEdit_03.setReadOnly(True)

        # 创建修型按钮 组件
        self.sculpt_Btn = QtWidgets.QPushButton('Sculpt')
        self.mirror_Btn = QtWidgets.QPushButton('Mirror')
        self.exit_Btn = QtWidgets.QPushButton('Exit')

        # 创建分割线 组件
        self.separator_02 = QtWidgets.QFrame()
        self.separator_02.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_02.setFrameShadow(QtWidgets.QFrame.Sunken)

        # 创建版权申明
        self.copyRight_label = QtWidgets.QLabel()
        self.copyRight_label.setText('Copyright(C) 2022 Rigging | QBJ')
        self.copyRight_label.setAlignment(QtCore.Qt.AlignCenter)


    def create_layouts(self):
        # 创建加载 布局
        self.load_GridLayout = QtWidgets.QGridLayout()
        self.load_GridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.load_GridLayout.setContentsMargins(2, 2, 2, 2)
        self.load_GridLayout.addWidget(self.baseGeo_Label,0,0,1,1)
        self.load_GridLayout.addWidget(self.baseGeo_LineEdit, 0, 1, 1, 4)
        self.load_GridLayout.addWidget(self.baseGeo_Btn, 0, 5, 1, 1)
        self.load_GridLayout.addWidget(self.oriGeo_Label, 1, 0, 1, 1)
        self.load_GridLayout.addWidget(self.oriGeo_LineEdit, 1, 1, 1, 4)
        self.load_GridLayout.addWidget(self.oriGeo_Btn, 1, 5, 1, 1)
        self.load_GridLayout.addWidget(self.blendshape_Label, 2, 0, 1, 1)
        self.load_GridLayout.addWidget(self.blendshape_comboBox, 2, 1, 1, 5)
        self.load_GridLayout.addWidget(self.add_Btn, 3, 4, 1, 1)
        self.load_GridLayout.addWidget(self.del_Btn, 3, 5, 1, 1)

        # 创建控制器类型 布局
        self.type_layout = QtWidgets.QHBoxLayout()
        self.type_layout.setContentsMargins(2,2,2,2)
        self.type_layout.addWidget(self.controlsType_Label)
        # self.type_layout.addItem(self.spacerItem_01)
        self.type_layout.addWidget(self.adv_radioBtn)
        self.type_layout.addWidget(self.defined_radionBtn)

        # 创建控制器旋转数值显示 布局
        self.rotate_layout = QtWidgets.QHBoxLayout()
        self.rotate_layout.setContentsMargins(4,2,4,2)
        self.rotate_layout.addWidget(self.rotate_Label)
        self.rotate_layout.addWidget(self.rotate_LineEdit_01)
        self.rotate_layout.addWidget(self.rotate_LineEdit_02)
        self.rotate_layout.addWidget(self.rotate_LineEdit_03)

        # 创建主布局
        main_Layout = QtWidgets.QVBoxLayout(self)
        main_Layout.addLayout(self.load_GridLayout)
        main_Layout.addWidget(self.separator_01)
        main_Layout.addLayout(self.type_layout)
        main_Layout.addWidget(self.tabWidget)
        main_Layout.addLayout(self.rotate_layout)
        main_Layout.addWidget(self.separator_02)
        main_Layout.addWidget(self.copyRight_label)

    def create_connections(self):
        pass

    def click_BaseGeoLoad_Btn(self):
        pass

    def click_OriGeoLoad_Btn(self):
        pass

    def click_addBS_Btn(self):
        pass

    def click_delBs_Btn(self):
        pass

    def click_armCreate_Btn(self):
        pass

    def click_legCreate_Btn(self):
        pass

    def click_fingerCreate_Btn(self):
        pass

    def click_torsoCreate_Btn(self):
        pass

    def click_sculpt_Btn(self):
        pass

    def click_mirror_Btn(self):
        pass

    def click_exit_Btn(self):
        pass
