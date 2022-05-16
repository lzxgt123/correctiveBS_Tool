# .-*- coding: utf-8 -*-
# .FileName:correctiveBS_UI
# .Date....:2022-03-21 : 11 :10
# .Author..:Qian binJie
# .Contact.:1075064966@qq.com
'''
launch :
        import correctiveBS_UI as QBJ_correctiveBS_UI
        reload(QBJ_correctiveBS_UI)
'''

from itertools import chain
import pymel.core as pm
import maya.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets,QtCore,QtGui
import correctiveBS_Tool as CBT
reload(CBT)
tool = CBT.CorrectiveBsTool()
import system.advSystem as ADV
reload(ADV)
adv = ADV.advSystem()


def maya_main_window():
    '''
        返回maya主窗口，使之变成一个python对象
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class CorrectiveBsUI(QtWidgets.QDialog):

    BUTTON_BGC = "background-color:rgb(142,188,255);color:black;"
    WINDOW_TITLE = 'Corrective Tool v1.0.0 Beta'
    limitAngleExpr = QtCore.QRegExp('^-?(180|([1-9]?\d|1[0-7][0-9])(\.\d{1,2})?)$')


    armPoseList = [u'-----肩胛-----', 'Scapula_L_Up', 'Scapula_L_Down', 'Scapula_L_Front', 'Scapula_L_Back',
                   u'-----上臂-----', 'Shoulder_L_Up', 'Shoulder_L_Down', 'Shoulder_L_Front', 'Shoulder_L_Back',
                   'Shoulder_L_UpFront', 'Shoulder_L_UpBack', 'Shoulder_L_DownFront', 'Shoulder_L_DownBack',
                   u'-----肘部-----', 'Elbow_L_Front',
                   u'-----手腕-----','Wrist_L_Up', 'Wrist_L_Down', 'Wrist_L_Front',
                   'Wrist_L_Back', 'Wrist_L_UpFront','Wrist_L_UpBack', 'Wrist_L_DownFront', 'Wrist_L_DownBack'
                   ]


    legPoseList = [u'-----腿部-----', 'Hip_L_Up', 'Hip_L_Down', 'Hip_L_Front', 'Hip_L_Back',
                   'Hip_L_UpFront', 'Hip_L_UpBack', 'Hip_L_DownFront', 'Hip_L_DownBack',
                   u'-----膝盖-----', 'Knee_L_Back',
                   u'-----脚踝-----', 'Ankle_L_Up', 'Ankle_L_Down', 'Ankle_L_Front', 'Ankle_L_Back', 'Ankle_L_UpFront',
                   'Ankle_L_UpBack', 'Ankle_L_DownFront', 'Ankle_L_DownBack'
                   ]


    fingerPoseList = [u'-----食指-----',  'IndexFinger1_L_Up','IndexFinger1_L_Down',
                      'IndexFinger2_L_Down', 'IndexFinger3_L_Down',

                      u'-----中指-----',  'MiddleFinger1_L_Up','MiddleFinger1_L_Down',
                      'MiddleFinger2_L_Down', 'MiddleFinger3_L_Down',

                      u'-----无名指-----',  'RingFinger1_L_Up','RingFinger1_L_Down',
                      'RingFinger2_L_Down', 'RingFinger3_L_Down',

                      u'-----小拇指-----',  'PinkyFinger1_L_Up','PinkyFinger1_L_Down',
                      'PinkyFinger2_L_Down','PinkyFinger3_L_Down',

                      u'-----大拇指-----',  'ThumbFinger1_L_Up','ThumbFinger1_L_Down',
                      'ThumbFinger2_L_Down', 'ThumbFinger3_L_Down'
                     ]


    torsoPoseList = [u'-----头部-----', 'Head_M_Front', 'Head_M_Back', 'Head_M_Left', 'Head_M_Right',
                     u'-----颈部-----', 'Neck_M_Front', 'Neck_M_Back', 'Neck_M_Left', 'Neck_M_Right',
                     u'-----胸腔-----', 'Chest_M_Front', 'Chest_M_Back', 'Chest_M_Left', 'Chest_M_Right',
                     u'-----躯干-----', 'Spine1_M_Front', 'Spine1_M_Back', 'Spine1_M_Left', 'Spine1_M_Right',
                     'Spine2_M_Front', 'Spine2_M_Back', 'Spine2_M_Left', 'Spine2_M_Right'
                    ]

    allPoseList = list(chain(armPoseList, legPoseList, fingerPoseList, torsoPoseList))

    def __init__(self,parent=maya_main_window()):
        super(CorrectiveBsUI, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint)
        self.showUI()


    def setFkModel(self):
        # 将所有控制器设置为fk模式
        model = self.radionBtn_Grp.checkedButton().text()
        if model == 'ADV':
            try:
                for ctrl in ['FKIKArm_L', 'FKIKArm_R', 'FKIKSpine_M', 'FKIKLeg_L', 'FKIKLeg_R']:
                    cmds.setAttr('{}.FKIKBlend'.format(ctrl), 0)
                om.MGlobal_displayInfo('QBJ_Tip : Switch to FK mode successfully !')
            except:
                om.MGlobal_displayWarning('QBJ_Tip : The ADV IKFK switch controller are not found ,failed to switch FK model !!')

        elif model == 'HumanIk':
            pass


    def check_ifnot_PoseGrp(self,ListWidget_01):
        poseGrpList = cmds.ls('*poseGrp')
        for i in range(ListWidget_01.count()):
            pose = ListWidget_01.item(i)
            if not pose.text().startswith('-'):
                poseGrp = pose.text().split('_')[0] + '_' + pose.text().split('_')[1] + '_' + 'poseGrp'
                if poseGrp not in poseGrpList:
                    pose.setFlags(pose.flags() & ~QtCore.Qt.ItemIsEnabled)


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
        self.setFkModel()
        self.show()


    def create_widgets(self):
        # 创建加载Base_Geo 组件
        self.baseGeo_Label = QtWidgets.QLabel('Base Geo :')
        self.baseGeo_LineEdit = QtWidgets.QLineEdit()
        self.baseGeo_LineEdit.setReadOnly(True)
        self.baseGeo_Btn = QtWidgets.QPushButton('Load')

        # 创建加载target _Geo 组件
        self.targetGeo_Label = QtWidgets.QLabel('Target  Geo :')
        self.targetGeo_LineEdit = QtWidgets.QLineEdit()
        self.targetGeo_LineEdit.setReadOnly(True)
        self.targetGeo_Btn = QtWidgets.QPushButton('Load')

        # 创建加载blendShape 组件
        self.blendshape_Label = QtWidgets.QLabel('blendShape :')
        self.blendshape_comboBox = QtWidgets.QComboBox()
        self.add_Btn = QtWidgets.QPushButton('Add')
        self.del_Btn = QtWidgets.QPushButton('Del')

        # 创建分割线 组件
        self.separator_01 = QtWidgets.QFrame()
        self.separator_01.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_01.setFrameShadow(QtWidgets.QFrame.Sunken)

        # 创建 控制器类型 组件
        self.controlsType_Label = QtWidgets.QLabel('Rig System :')
        self.adv_radioBtn = QtWidgets.QRadioButton('ADV')
        self.adv_radioBtn.setChecked(True)
        self.humanIK_radioBtn = QtWidgets.QRadioButton('HumanIK')
        self.humanIK_radioBtn.setEnabled(False)

        self.radionBtn_Grp = QtWidgets.QButtonGroup()
        self.radionBtn_Grp.addButton(self.adv_radioBtn,1)
        self.radionBtn_Grp.addButton(self.humanIK_radioBtn, 2)


        # 创建驱动控制 组件
        self.driver_Label = QtWidgets.QLabel('Driver :')
        self.driver_LineEdit = QtWidgets.QLineEdit()
        self.driver_LineEdit.setReadOnly(True)
        self.driver_value_LineEdit = QtWidgets.QLineEdit()
        self.driver_value_LineEdit.setMaximumWidth(80)
        self.driver_value_LineEdit.setReadOnly(True)

        # 创建tabWidget内 组件
        # 添加 arm_ListWidget_01右击menu显示
        self.arm_ListWidget_01 = QtWidgets.QListWidget()
        self.arm_ListWidget_01.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.arm_contextMenu = QtWidgets.QMenu(self.arm_ListWidget_01)
        self.arm_updateDriver = self.arm_contextMenu.addAction('Update Driver')
        self.arm_contextMenu.addSeparator()
        self.arm_addPose = self.arm_contextMenu.addAction('Add Pose')
        self.arm_removePose = self.arm_contextMenu.addAction('Remove Pose')
        self.arm_resetPose = self.arm_contextMenu.addAction('Reset Pose')
        self.arm_contextMenu.addSeparator()
        self.arm_setAni = self.arm_contextMenu.addAction('Set Animation')
        self.arm_delAni = self.arm_contextMenu.addAction('Del Animation')
        # 将 pose添加进listWidget中
        for item in self.armPoseList:
            self.arm_ListWidget_01.addItem(item)
        # 将没有对应poseGrp的item设置为不可选状态
        self.check_ifnot_PoseGrp(self.arm_ListWidget_01)
        # 创建 arm_sculpt布局
        self.arm_mirror_CB = QtWidgets.QCheckBox('Mirror')
        self.arm_mirror_CB.setChecked(True)
        self.arm_sculpt_Btn = QtWidgets.QPushButton('Sculpt')
        self.arm_exit_Btn = QtWidgets.QPushButton('Exit')


        # 添加leg_ListWidget_01右击menu显示
        self.leg_ListWidget_01 = QtWidgets.QListWidget()
        self.leg_ListWidget_01.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.leg_contextMenu = QtWidgets.QMenu(self.leg_ListWidget_01)
        self.leg_updateDriver = self.leg_contextMenu.addAction('Update Driver')
        self.leg_contextMenu.addSeparator()
        self.leg_addPose = self.leg_contextMenu.addAction('Add Pose')
        self.leg_removePose = self.leg_contextMenu.addAction('Remove Pose')
        self.leg_resetPose = self.leg_contextMenu.addAction('Reset Pose')
        self.leg_contextMenu.addSeparator()
        self.leg_setAni = self.leg_contextMenu.addAction('Set Animation')
        self.leg_delAni = self.leg_contextMenu.addAction('Del Animation')



        # 将 pose添加进listWidget中
        for item in self.legPoseList:
            self.leg_ListWidget_01.addItem(item)
        # 将没有对应poseGrp的item设置为不可选状态
        self.check_ifnot_PoseGrp(self.leg_ListWidget_01)
        # 创建leg_sculpt布局
        self.leg_mirror_CB = QtWidgets.QCheckBox('Mirror')
        self.leg_mirror_CB.setChecked(True)
        self.leg_sculpt_Btn = QtWidgets.QPushButton('Sculpt')
        self.leg_exit_Btn = QtWidgets.QPushButton('Exit')


        # 添加finger_ListWidget_01右击menu显示
        self.finger_ListWidget_01 = QtWidgets.QListWidget()
        self.finger_ListWidget_01.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.finger_contextMenu = QtWidgets.QMenu(self.finger_ListWidget_01)
        self.finger_updateDriver = self.finger_contextMenu.addAction('Update Driver')
        self.finger_contextMenu.addSeparator()
        self.finger_addPose = self.finger_contextMenu.addAction('Add Pose')
        self.finger_removePose = self.finger_contextMenu.addAction('Remove Pose')
        self.finger_resetPose = self.finger_contextMenu.addAction('Reset Pose')
        self.finger_contextMenu.addSeparator()
        self.finger_setAni = self.finger_contextMenu.addAction('Set Animation')
        self.finger_delAni = self.finger_contextMenu.addAction('Del Animation')


        # 将 pose添加进listWidget中
        for item in self.fingerPoseList:
            self.finger_ListWidget_01.addItem(item)
        # 创建finger_sculpt布局
        self.finger_mirror_CB = QtWidgets.QCheckBox('Mirror')
        self.finger_mirror_CB.setChecked(True)
        self.finger_sculpt_Btn = QtWidgets.QPushButton('Sculpt')
        self.finger_exit_Btn = QtWidgets.QPushButton('Exit')


        # 添加torso_ListWidget_01右击menu显示
        self.torso_ListWidget_01 = QtWidgets.QListWidget()
        self.torso_ListWidget_01.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.torso_contextMenu = QtWidgets.QMenu(self.torso_ListWidget_01)
        self.torso_updateDriver = self.torso_contextMenu.addAction('Update Driver')
        self.torso_contextMenu.addSeparator()
        self.torso_addPose = self.torso_contextMenu.addAction('Add Pose')
        self.torso_removePose = self.torso_contextMenu.addAction('Remove Pose')
        self.torso_resetPose = self.torso_contextMenu.addAction('Reset Pose')
        self.torso_contextMenu.addSeparator()
        self.torso_setAni = self.torso_contextMenu.addAction('Set Animation')
        self.torso_delAni = self.torso_contextMenu.addAction('Del Animation')
        # 将 pose添加进listWidget中
        for item in self.torsoPoseList:
            self.torso_ListWidget_01.addItem(item)
        # 将没有对应poseGrp的item设置为不可选状态
        self.check_ifnot_PoseGrp(self.torso_ListWidget_01)
        # 创建torso_sculpt布局
        self.torso_mirror_CB = QtWidgets.QCheckBox('Mirror')
        self.torso_mirror_CB.setChecked(False)
        self.torso_sculpt_Btn = QtWidgets.QPushButton('Sculpt')
        self.torso_exit_Btn = QtWidgets.QPushButton('Exit')


        self.custom_Tab = QtWidgets.QWidget()
        self.custom_Layout = QtWidgets.QVBoxLayout(self.custom_Tab)
        self.custom_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.custom_Layout.setContentsMargins(2, 2, 2, 2)
        self.custom_Layout.setSpacing(3)
        self.custom_Splitter_01 = QtWidgets.QSplitter(self.custom_Tab)
        self.custom_Splitter_01.setMinimumSize(QtCore.QSize(400, 0))
        self.custom_Splitter_01.setOrientation(QtCore.Qt.Vertical)
        self.custom_ListWidget_01 = QtWidgets.QListWidget(self.custom_Splitter_01)
        self.custom_Splitter_01.setStretchFactor(0, 7)
        self.custom_Splitter_01.setStretchFactor(1, 3)
        self.custom_Layout.addWidget(self.custom_Splitter_01)


        # 创建控制器旋转数值显示 组件
        self.rotate_Label = QtWidgets.QLabel('Rotate:')
        self.rotate_LineEdit_01 = QtWidgets.QLineEdit()
        self.rotate_LineEdit_01.setText('0.0')
        self.rotate_LineEdit_01.setReadOnly(True)
        self.rotate_LineEdit_02 = QtWidgets.QLineEdit()
        self.rotate_LineEdit_02.setText('0.0')
        self.rotate_LineEdit_02.setReadOnly(True)
        self.rotate_LineEdit_03 = QtWidgets.QLineEdit()
        self.rotate_LineEdit_03.setText('0.0')
        self.rotate_LineEdit_03.setReadOnly(True)

        # 创建分割线 组件
        self.separator_02 = QtWidgets.QFrame()
        self.separator_02.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_02.setFrameShadow(QtWidgets.QFrame.Sunken)

        # 创建版权申明
        self.copyRight_label = QtWidgets.QLabel()
        self.copyRight_label.setText('Copyright(C) 2022—— Rigging | QBJ')
        self.copyRight_label.setAlignment(QtCore.Qt.AlignCenter)


    def create_layouts(self):
        # 创建加载 布局
        self.load_GridLayout = QtWidgets.QGridLayout()
        self.load_GridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.load_GridLayout.setContentsMargins(2, 2, 2, 2)
        self.load_GridLayout.setVerticalSpacing(4)
        self.load_GridLayout.addWidget(self.baseGeo_Label,0,0,1,1)
        self.load_GridLayout.addWidget(self.baseGeo_LineEdit, 0, 1, 1, 6)
        self.load_GridLayout.addWidget(self.baseGeo_Btn, 0, 7, 1, 1)
        self.load_GridLayout.addWidget(self.targetGeo_Label, 1, 0, 1, 1)
        self.load_GridLayout.addWidget(self.targetGeo_LineEdit, 1, 1, 1, 6)
        self.load_GridLayout.addWidget(self.targetGeo_Btn, 1, 7, 1, 1)
        self.load_GridLayout.addWidget(self.blendshape_Label, 2, 0, 1, 1)
        self.load_GridLayout.addWidget(self.blendshape_comboBox, 2, 1, 1,5)
        self.load_GridLayout.addWidget(self.add_Btn, 2, 6, 1, 1)
        self.load_GridLayout.addWidget(self.del_Btn, 2, 7, 1, 1)

        # 创建控制器类型 布局
        self.type_layout = QtWidgets.QHBoxLayout()
        self.type_layout.setContentsMargins(2,2,2,2)
        self.type_layout.addWidget(self.controlsType_Label)
        self.type_layout.addWidget(self.adv_radioBtn)
        self.type_layout.addWidget(self.humanIK_radioBtn)

        # 创建驱动控制 布局
        self.driver_layout = QtWidgets.QHBoxLayout()
        self.driver_layout.setContentsMargins(4,0,4,0)
        self.driver_layout.addWidget(self.driver_Label)
        self.driver_layout.addWidget(self.driver_LineEdit)
        self.driver_layout.addWidget(self.driver_value_LineEdit)

        # 创建 tabWidget 布局
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setStyleSheet("QTabBar::tab{width:70} QTabBar::tab{height:20}")
        self.tabWidget.setCurrentIndex(1)
        # 创建 arm_Tab 布局
        self.arm_Tab = QtWidgets.QWidget()
        self.arm_Splitter_01 = QtWidgets.QSplitter()
        self.arm_Splitter_01.setMinimumSize(QtCore.QSize(400, 0))
        self.arm_Splitter_01.setOrientation(QtCore.Qt.Vertical)
        self.arm_Splitter_01.addWidget(self.arm_ListWidget_01)
        self.arm_Splitter_01.setStretchFactor(0, 8)
        self.arm_Splitter_01.setStretchFactor(1, 2)
        self.arm_sculpt_Layout = QtWidgets.QHBoxLayout()
        self.arm_sculpt_Layout.setContentsMargins(4, 2, 4, 2)
        self.arm_sculpt_Layout.addWidget(self.arm_mirror_CB)
        self.arm_sculpt_Layout.addWidget(self.arm_sculpt_Btn)
        self.arm_sculpt_Layout.addWidget(self.arm_exit_Btn)
        self.arm_Layout = QtWidgets.QVBoxLayout(self.arm_Tab)
        self.arm_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.arm_Layout.setContentsMargins(2, 2, 2, 2)
        self.arm_Layout.setSpacing(3)
        self.arm_Layout.addWidget(self.arm_Splitter_01)
        self.arm_Layout.addLayout(self.arm_sculpt_Layout)
        # 创建 leg_Tab 布局
        self.leg_Tab = QtWidgets.QWidget()
        self.leg_Splitter_01 = QtWidgets.QSplitter(self.leg_Tab)
        self.leg_Splitter_01.setMinimumSize(QtCore.QSize(400, 0))
        self.leg_Splitter_01.setOrientation(QtCore.Qt.Vertical)
        self.leg_Splitter_01.addWidget(self.leg_ListWidget_01)
        self.leg_Splitter_01.setStretchFactor(0, 8)
        self.leg_Splitter_01.setStretchFactor(1, 2)
        self.leg_sculpt_Layout = QtWidgets.QHBoxLayout()
        self.leg_sculpt_Layout.setContentsMargins(4, 2, 4, 2)
        self.leg_sculpt_Layout.addWidget(self.leg_mirror_CB)
        self.leg_sculpt_Layout.addWidget(self.leg_sculpt_Btn)
        self.leg_sculpt_Layout.addWidget(self.leg_exit_Btn)
        self.leg_Layout = QtWidgets.QVBoxLayout(self.leg_Tab)
        self.leg_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.leg_Layout.setContentsMargins(2, 2, 2, 2)
        self.leg_Layout.setSpacing(3)
        self.leg_Layout.addWidget(self.leg_Splitter_01)
        self.leg_Layout.addLayout(self.leg_sculpt_Layout)
        # 创建 finger_Tab 布局
        self.finger_Tab = QtWidgets.QWidget()
        self.finger_Splitter_01 = QtWidgets.QSplitter()
        self.finger_Splitter_01.setMinimumSize(QtCore.QSize(400, 0))
        self.finger_Splitter_01.setOrientation(QtCore.Qt.Vertical)
        self.finger_Splitter_01.addWidget(self.finger_ListWidget_01)
        self.finger_Splitter_01.setStretchFactor(0, 8)
        self.finger_Splitter_01.setStretchFactor(1, 2)
        self.finger_sculpt_Layout = QtWidgets.QHBoxLayout()
        self.finger_sculpt_Layout.setContentsMargins(4, 2, 4, 2)
        self.finger_sculpt_Layout.addWidget(self.finger_mirror_CB)
        self.finger_sculpt_Layout.addWidget(self.finger_sculpt_Btn)
        self.finger_sculpt_Layout.addWidget(self.finger_exit_Btn)
        self.finger_Layout = QtWidgets.QVBoxLayout(self.finger_Tab)
        self.finger_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.finger_Layout.setContentsMargins(2, 2, 2, 2)
        self.finger_Layout.setSpacing(3)
        self.finger_Layout.addWidget(self.finger_Splitter_01)
        self.finger_Layout.addLayout(self.finger_sculpt_Layout)
        # 创建 torso_Tab 布局
        self.torso_Tab = QtWidgets.QWidget()
        self.torso_Splitter_01 = QtWidgets.QSplitter()
        self.torso_Splitter_01.setMinimumSize(QtCore.QSize(400, 0))
        self.torso_Splitter_01.setOrientation(QtCore.Qt.Vertical)
        self.torso_Splitter_01.addWidget(self.torso_ListWidget_01)

        self.torso_Splitter_01.setStretchFactor(0, 8)
        self.torso_Splitter_01.setStretchFactor(1, 2)
        self.torso_sculpt_Layout = QtWidgets.QHBoxLayout()
        self.torso_sculpt_Layout.setContentsMargins(4, 2, 4, 2)
        self.torso_sculpt_Layout.addWidget(self.torso_mirror_CB)
        self.torso_sculpt_Layout.addWidget(self.torso_sculpt_Btn)
        self.torso_sculpt_Layout.addWidget(self.torso_exit_Btn)
        self.torso_Layout = QtWidgets.QVBoxLayout(self.torso_Tab)
        self.torso_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.torso_Layout.setContentsMargins(2, 2, 2, 2)
        self.torso_Layout.setSpacing(3)
        self.torso_Layout.addWidget(self.torso_Splitter_01)
        self.torso_Layout.addLayout(self.torso_sculpt_Layout)


        self.tabWidget.addTab(self.arm_Tab, 'Arm')
        self.tabWidget.addTab(self.leg_Tab, 'leg')
        self.tabWidget.addTab(self.finger_Tab, 'finger')
        self.tabWidget.addTab(self.torso_Tab, 'torso')
        self.tabWidget.addTab(self.custom_Tab, 'custom')


        # 创建控制器旋转数值显示 布局
        self.rotate_layout = QtWidgets.QHBoxLayout()
        self.rotate_layout.setContentsMargins(4,0,4,0)
        self.rotate_layout.addWidget(self.rotate_Label)
        self.rotate_layout.addWidget(self.rotate_LineEdit_01)
        self.rotate_layout.addWidget(self.rotate_LineEdit_02)
        self.rotate_layout.addWidget(self.rotate_LineEdit_03)

        # 创建主布局
        main_Layout = QtWidgets.QVBoxLayout(self)
        main_Layout.addLayout(self.load_GridLayout)
        main_Layout.addWidget(self.separator_01)
        main_Layout.addLayout(self.type_layout)
        main_Layout.addLayout(self.driver_layout)
        main_Layout.addWidget(self.tabWidget)
        main_Layout.addLayout(self.rotate_layout)
        main_Layout.addWidget(self.separator_02)
        main_Layout.addWidget(self.copyRight_label)


    def create_connections(self):

        self.baseGeo_Btn.clicked.connect(self.click_BaseGeoLoad_Btn)
        self.targetGeo_Btn.clicked.connect(self.click_targetGeoLoad_Btn)
        self.add_Btn.clicked.connect(self.click_addBs_Btn)
        self.del_Btn.clicked.connect(self.click_delBs_Btn)
        self.arm_sculpt_Btn.clicked.connect(lambda :self.click_sculpt_Btn(self.arm_ListWidget_01,
                                                                          self.arm_sculpt_Btn,
                                                                          self.arm_mirror_CB))
        self.arm_exit_Btn.clicked.connect(lambda :self.click_exit_Btn(self.arm_ListWidget_01,
                                                                      self.arm_sculpt_Btn,
                                                                      self.arm_mirror_CB))
        self.leg_sculpt_Btn.clicked.connect(lambda :self.click_sculpt_Btn(self.leg_ListWidget_01,
                                                                          self.leg_sculpt_Btn,
                                                                          self.leg_mirror_CB))
        self.leg_exit_Btn.clicked.connect(lambda :self.click_exit_Btn(self.leg_ListWidget_01,
                                                                      self.leg_sculpt_Btn,
                                                                      self.leg_mirror_CB))
        self.finger_sculpt_Btn.clicked.connect(lambda :self.click_sculpt_Btn(self.finger_ListWidget_01,
                                                                             self.finger_sculpt_Btn,
                                                                             self.finger_mirror_CB))
        self.finger_exit_Btn.clicked.connect(lambda :self.click_exit_Btn(self.finger_ListWidget_01,
                                                                         self.finger_sculpt_Btn,
                                                                         self.finger_mirror_CB))
        self.torso_sculpt_Btn.clicked.connect(lambda :self.click_sculpt_Btn(self.torso_ListWidget_01,
                                                                            self.torso_sculpt_Btn,
                                                                            self.torso_mirror_CB))
        self.torso_exit_Btn.clicked.connect(lambda :self.click_exit_Btn(self.torso_ListWidget_01,
                                                                        self.torso_sculpt_Btn,
                                                                        self.torso_mirror_CB))


        # self.arm_CreateBtn.clicked.connect(self.click_armCreate_Btn)
        self.arm_ListWidget_01.itemClicked.connect(self.click_armListWidget01_item)
        self.arm_ListWidget_01.customContextMenuRequested[QtCore.QPoint].connect(lambda :self.rightMenuShow(self.arm_contextMenu))
        self.arm_setAni.triggered.connect(lambda : self.click_setAnimation(self.arm_ListWidget_01))
        self.arm_delAni.triggered.connect(lambda : self.click_delAnimation(self.arm_ListWidget_01))
        self.arm_updateDriver.triggered.connect(lambda : self.click_updateDriver(self.arm_ListWidget_01,
                                                                                 self.arm_mirror_CB))
        self.arm_addPose.triggered.connect(lambda : self.click_addPose(self.arm_ListWidget_01))
        self.arm_removePose.triggered.connect(lambda : self.click_removePose(self.arm_ListWidget_01))
        self.arm_resetPose.triggered.connect(lambda : self.click_resetPose(self.arm_ListWidget_01))

        # self.leg_CreateBtn.clicked.connect(self.click_legCreate_Btn)
        self.leg_ListWidget_01.itemClicked.connect(self.click_legListWidget01_item)
        self.leg_ListWidget_01.customContextMenuRequested[QtCore.QPoint].connect(lambda :self.rightMenuShow(self.leg_contextMenu))
        self.leg_setAni.triggered.connect(lambda: self.click_setAnimation(self.leg_ListWidget_01))
        self.leg_delAni.triggered.connect(lambda: self.click_delAnimation(self.leg_ListWidget_01))
        self.leg_updateDriver.triggered.connect(lambda:self.click_updateDriver(self.leg_ListWidget_01,
                                                                               self.leg_mirror_CB))
        self.leg_addPose.triggered.connect(lambda : self.click_addPose(self.leg_ListWidget_01))
        self.leg_removePose.triggered.connect(lambda: self.click_removePose(self.leg_ListWidget_01))
        self.leg_resetPose.triggered.connect(lambda: self.click_resetPose(self.leg_ListWidget_01))

        # self.finger_CreateBtn.clicked.connect(self.click_fingerCreate_Btn)
        self.finger_ListWidget_01.clicked.connect(self.click_fingerListWidget01_item)
        self.finger_ListWidget_01.customContextMenuRequested[QtCore.QPoint].connect(lambda :self.rightMenuShow(self.finger_contextMenu))
        self.finger_setAni.triggered.connect(lambda: self.click_setAnimation(self.finger_ListWidget_01))
        self.finger_delAni.triggered.connect(lambda: self.click_delAnimation(self.finger_ListWidget_01))
        self.finger_updateDriver.triggered.connect(self.click_updateFingerDriver)
        self.finger_addPose.triggered.connect(self.click_fingerAddPose)
        self.finger_removePose.triggered.connect(lambda: self.click_removePose(self.finger_ListWidget_01))
        self.finger_resetPose.triggered.connect(lambda: self.click_resetPose(self.finger_ListWidget_01))

        # self.torso_CreateBtn.clicked.connect(self.click_torsoCreate_Btn)
        self.torso_ListWidget_01.clicked.connect(self.click_torsoListWidget01_item)
        self.torso_ListWidget_01.customContextMenuRequested[QtCore.QPoint].connect(lambda :self.rightMenuShow(self.torso_contextMenu))
        self.torso_setAni.triggered.connect(lambda: self.click_setAnimation(self.torso_ListWidget_01))
        self.torso_delAni.triggered.connect(lambda: self.click_delAnimation(self.torso_ListWidget_01))
        self.torso_updateDriver.triggered.connect(lambda : self.click_updateDriver(self.torso_ListWidget_01,
                                                                                   self.torso_mirror_CB))
        self.torso_addPose.triggered.connect(lambda : self.click_addPose(self.torso_ListWidget_01))
        self.torso_removePose.triggered.connect(lambda: self.click_removePose(self.torso_ListWidget_01))
        self.torso_resetPose.triggered.connect(lambda: self.click_resetPose(self.torso_ListWidget_01))

        self.tabWidget.currentChanged.connect(self.tabWidget_changeEvent)


    def tabWidget_changeEvent(self,index):
        if index == 2:
            # 生成左右Finger_poseGrp
            tool.create_finger_PoseGrp('Finger_L',tool.L_fingerPoseDict)
            tool.create_finger_PoseGrp('Finger_R',tool.R_fingerPoseDict)


    def rightMenuShow(self,contextMenu):
        contextMenu.exec_(QtGui.QCursor.pos())


    def click_BaseGeoLoad_Btn(self):
        # 获取 baseGeo
        baseGeo = tool.load_BaseGeo()
        # 将获取到的baseGeo名称，加载到baseGeo_LineEdit中
        if baseGeo:
            self.baseGeo_LineEdit.setText(str(baseGeo))
            # 检查场景中是否存在targetGeo
            if tool.return_targetOriGeo(baseGeo):
                targetGeo = tool.return_targetOriGeo(baseGeo)
                self.targetGeo_LineEdit.setText(str(targetGeo))

            bsNode = tool.get_blendshape(baseGeo)

            if bsNode:
                if len(bsNode) == 1:
                    self.blendshape_comboBox.clear()
                    self.blendshape_comboBox.addItem(bsNode[0])
                else :
                    om.MGlobal_displayError('QBJ_Tip : More than one blendShape node on the object !!!')
                    return
            else:
                self.addBlendShapeConfirmDialog()


    def click_targetGeoLoad_Btn(self):
        baseGeo = self.baseGeo_LineEdit.text()
        targetGeo = self.targetGeo_LineEdit.text()
        if not targetGeo:
            if baseGeo:
                targetGeo = tool.return_targetOriGeo(baseGeo)
                if targetGeo:
                    self.targetGeo_LineEdit.setText(str(targetGeo))
        else:
            self.loadTargetConfirmDialog()


    def click_addBs_Btn(self):
        # 获取 baseGeo
        baseGeo = self.baseGeo_LineEdit.text()
        if  not tool.get_blendshape(baseGeo):
            self.addBlendShapeConfirmDialog()


    def click_delBs_Btn(self):

        bsNode = self.blendshape_comboBox.currentText()
        targetGeo = self.targetGeo_LineEdit.text()
        baseGeo = self.baseGeo_LineEdit.text()
        bsTargetGrp = '{}_bsTarget_Grp'.format(baseGeo)
        if bsNode:
            tool.del_blendShape(bsNode)
            self.blendshape_comboBox.clear()
        if targetGeo:
            tool.del_targetGeo(targetGeo)
            self.targetGeo_LineEdit.clear()
        if bsTargetGrp:
            cmds.delete(bsTargetGrp)

        om.MGlobal_displayInfo('QBJ_Tip : Delete blendShape Node successfully !')


    def click_sculpt_Btn(self,ListWidget_01,sculpt_Btn,mirror_CB):
        baseGeo = self.baseGeo_LineEdit.text()
        targetOri_Geo = self.targetGeo_LineEdit.text()
        bsNode = self.blendshape_comboBox.currentText()
        mirror = mirror_CB.isChecked()
        # 检查场景中是否存在以下对象，如缺少一个，则报错并返回
        for geo in [baseGeo, targetOri_Geo]:
            if not cmds.objExists(geo):
                om.MGlobal_displayError('QBJ_Tip : Can not find {} !!!'.format(geo))
                return

        # 在有选中的pose后，才会运行
        if ListWidget_01.currentItem():
            pose = ListWidget_01.currentItem().text()

            if  not pose.startswith('-'):
                # 将sculpt_Btn及其余的item设置为不可选状态
                self.lock_allItem(ListWidget_01,sculpt_Btn)
                # 创建 tempSculptGrp，进入雕刻模式
                poseGrp = pose.split('_')[0] + '_' + pose.split('_')[1] + '_poseGrp'
                tool.enterSculptMode(baseGeo,bsNode,pose,targetOri_Geo,mirror,poseGrp)
                # 设置控制器驱动动画
                self.click_setAnimation(ListWidget_01)


    def click_exit_Btn(self,ListWidget_01,sculpt_Btn,mirror_CB):
        targetOri_Geo = self.targetGeo_LineEdit.text()
        mirror = mirror_CB.isChecked()

        if ListWidget_01.currentItem():
            baseGeo = self.baseGeo_LineEdit.text()
            pose = ListWidget_01.currentItem().text()

            if not pose.startswith('-'):
                sculptGeo = '{}_{}_sculpt'.format(baseGeo, pose)

                # 删除控制器驱动动画
                self.click_delAnimation(ListWidget_01)
                # 将 sculpt_Btn及其余的item设置为可选状态
                self.unlock_allItem(ListWidget_01, sculpt_Btn)
                # 退出 雕刻模式
                tool.exitSculptMode(baseGeo,targetOri_Geo,sculptGeo,pose,mirror)


    def create_blendShape(self):
        allPoseList = self.allPoseList
        # 为 baseGeo 创建blendShape，并将生成的target和bsNode加载到Gui中
        baseGeo = self.baseGeo_LineEdit.text()
        targetGeo = self.targetGeo_LineEdit.text()
        if baseGeo:

            targetGeo_bsNode_list = tool.add_blendShape(baseGeo,targetGeo,allPoseList)
            # 在targetGeoGrp组上添加bsTargetInfo
            self.targetGeo_LineEdit.setText(str(targetGeo_bsNode_list[0]))
            self.blendshape_comboBox.clear()
            self.blendshape_comboBox.addItem(str(targetGeo_bsNode_list[1][0]))
            om.MGlobal_displayInfo('QBJ_Tip : Add blendShape successfully !')


    def changeTargetGeo(self):
        # 将targetGeo_LineEdit的名称 ，替换为此时用户选中的模型名称
        targetGeo = tool.load_targetGeo()
        attrs_list = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']
        # 尝试将 targetGeo上的属性解锁
        try:
            for attr in attrs_list:
                cmds.setAttr('{}{}'.format(targetGeo, attr), lock=False)
        except:
            pass

        if targetGeo:
            self.targetGeo_LineEdit.setText(str(targetGeo))


    def addBlendShapeConfirmDialog(self):
        result = pm.confirmDialog(title="Add blendShape", message="Can't find blendShape Node , Add or not ?", button=[
            'Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if result == 'Yes':
            self.create_blendShape()


    def loadTargetConfirmDialog(self):
        result = pm.confirmDialog(title="Load target", message="Already have target Geo , Change or not ?", button=[
            'Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if result == 'Yes':
            self.changeTargetGeo()


    def click_ListWidget01_item(self,baseGeo,blendShapeNode,ListWidget_01):

        pose = ListWidget_01.currentItem().text()

        # # 获取对应命名的target
        # self.load_targetName( blendShapeNode, ListWidget_01)
        # 获取所选择的item对应的控制器的旋转数值
        self.set_RotateLineEdit_Value(ListWidget_01)
        # 清除所有控制器上的数值
        self.clearCtrlRotation()
        # 根据RotateLineEdit上的数值，设置控制器的旋转
        self.setCtrlRotation(ListWidget_01)
        # 获取Driver信息
        self.loadDriverInfo(ListWidget_01)
        # 选中对应的fkCtrl
        if not pose.startswith('-'):
            fkCtrl = 'FK' + pose.split('_')[0] + '_' + pose.split('_')[1]
            cmds.select(fkCtrl, r=True)


    def click_armListWidget01_item(self):
        baseGeo = self.baseGeo_LineEdit.text()
        blendShapeNode = self.blendshape_comboBox.currentText()
        self.click_ListWidget01_item(baseGeo,blendShapeNode,self.arm_ListWidget_01)


    def click_legListWidget01_item(self):
        baseGeo = self.baseGeo_LineEdit.text()
        blendShapeNode = self.blendshape_comboBox.currentText()
        self.click_ListWidget01_item(baseGeo, blendShapeNode, self.leg_ListWidget_01)


    def click_fingerListWidget01_item(self):
        baseGeo = self.baseGeo_LineEdit.text()
        blendShapeNode = self.blendshape_comboBox.currentText()
        fingerPose = self.finger_ListWidget_01.currentItem().text()
        # # 获取对应命名的target
        # self.load_targetName(blendShapeNode,self.finger_ListWidget_01)
        # 获取所选择的item对应的控制器的旋转数值
        self.set_fingerRotateLineEdit_Value()
        # 清除所有控制器上的数值
        self.clearCtrlRotation()
        # 根据RotateLineEdit上的数值，设置控制器的旋转
        self.setCtrlRotation(self.finger_ListWidget_01)
        # 获取Driver信息
        self.loadFingerDriverInfo()
        # 选中对应的fkCtrl
        if not fingerPose.startswith('-'):
            fkCtrl = 'FK' + fingerPose.split('_')[0] + '_' + fingerPose.split('_')[1]
            cmds.select(fkCtrl, r=True)


    def click_torsoListWidget01_item(self):
        baseGeo = self.baseGeo_LineEdit.text()
        blendShapeNode = self.blendshape_comboBox.currentText()
        self.click_ListWidget01_item(baseGeo, blendShapeNode, self.torso_ListWidget_01)


    def loadDriverInfo(self,ListWidget_01):
        pose = ListWidget_01.currentItem().text()
        # 过滤以'-'开头的item
        if not pose.startswith('-'):
            poseGrp = pose.split('_')[0] + '_' + pose.split('_')[1] + '_poseGrp'
            # 将poseGrp上的数据显示在driver_LineEdit中
            if cmds.objExists(poseGrp):
                value = cmds.getAttr('{}.{}'.format(poseGrp, pose))
                self.driver_LineEdit.setText('{}.{}'.format(poseGrp, pose))
                self.driver_value_LineEdit.setText('{}'.format(round(value, 4)))
        else:
            self.driver_value_LineEdit.setText('')
            self.driver_LineEdit.setText('')


    # def loadBsTargetInfo(self,baseGeo,ListWidget_01):
    #     pose = ListWidget_01.currentItem().text()
    #     # 获取当前所选pose，对应的bsTargetInfo
    #     bsTargetList = tool.check_exists_bsTargetInfo(baseGeo,pose)
    #     if bsTargetList:
    #         for t in bsTargetList:
    #             if t != '':
    #                 ListWidget_02.addItem(t)


    # def load_targetName(self,blendShapeNode,ListWidget_01):
    #     pose = ListWidget_01.currentItem().text()
    #     if blendShapeNode:
    #         # 过滤以'-'开头的item
    #         if not pose.startswith('-'):
    #             # 获取指点命名的target，并添加到ListWidget_02中
    #             allTargets = cmds.aliasAttr(blendShapeNode, q=True)
    #             targetName = []
    #             if allTargets:
    #                 for i in range(0, len(allTargets), 2):
    #                     targetName.append(allTargets[i])


    def clearCtrlRotation(self):
        # 将pose，命名转化为fkCtrl后，将rotate数值清零
        for i in self.allPoseList:
            if not i.startswith('-'):
                fkCtrl = 'FK' + i.split('_')[0] + '_' + i.split('_')[1]
                try:
                    for axis in ['rx','ry','rz']:
                        cmds.setAttr('{}.{}'.format(fkCtrl, axis), 0)
                except:
                    pass


    def setCtrlRotation (self,ListWidget_01):
        rotateValue = self.returnRotateValue()
        pose = ListWidget_01.currentItem().text()
        if not pose.startswith('-'):
            fkCtrl = 'FK' + pose.split('_')[0]+'_'+pose.split('_')[1]
            if cmds.objExists(fkCtrl):
                for rotate,value in rotateValue.items():
                    cmds.setAttr('{}.{}'.format(fkCtrl,rotate),float(value))


    def returnRotateValue(self):
        rotatetList = ['rx', 'ry', 'rz']

        rxValue = self.rotate_LineEdit_01.text()
        ryValue = self.rotate_LineEdit_02.text()
        rzValue = self.rotate_LineEdit_03.text()
        valueList = [rxValue,ryValue,rzValue]

        rotateValueData = zip(rotatetList,valueList)
        rotateValue = dict(rotateValueData)
        return rotateValue


    def clear_RotateLineEdit_Value(self):
        # 清除rotate_LineEdit上的数据
        self.rotate_LineEdit_01.setText('0.0')
        self.rotate_LineEdit_02.setText('0.0')
        self.rotate_LineEdit_03.setText('0.0')


    def set_RotateLineEdit_Value(self,ListWidget_01):
        self.driver_LineEdit.clear()
        self.clear_RotateLineEdit_Value()
        pose = ListWidget_01.currentItem().text()
        hideGrp = pose.replace(pose.split('_')[-1],'poseGrp_Hide')
        if cmds.objExists(hideGrp):
            valueList = cmds.getAttr('{}.{}'.format(hideGrp,pose.split('_')[-1]))
            self.rotate_LineEdit_01.setText(str(valueList[0][0]))
            self.rotate_LineEdit_02.setText(str(valueList[0][1]))
            self.rotate_LineEdit_03.setText(str(valueList[0][2]))


    def click_setAnimation(self,ListWidget_01):
        pose = ListWidget_01.currentItem().text()
        # self.set_RotateLineEdit_Value(ListWidget_01)
        rotateValueDict = self.returnRotateValue()
        if not pose.startswith('-'):
            # 将时间滑块的范围调整成1-25帧
            try:
                cmds.playbackOptions(edit=True,min=1,max=25,ast=1,aet=25)
            except:
                pass
            # 设置对应的fkCtrl的动画
            fkCtrl = 'FK' + pose.split('_')[0]+'_'+pose.split('_')[1]
            if cmds.objExists(fkCtrl):
                for axis ,value in rotateValueDict.items():
                    self.del_animNode(fkCtrl,axis)
                    animNode =cmds.createNode('animCurveTA',name = '{}_{}_animTA'.format(fkCtrl,axis))
                    cmds.connectAttr('{}.output'.format(animNode),'{}.{}'.format(fkCtrl,axis))
                    cmds.setKeyframe(animNode,time=1,value = 0)
                    cmds.setKeyframe(animNode, time=20, value=float(value))


    def click_delAnimation(self,ListWidget_01):
        pose = ListWidget_01.currentItem().text()
        if not pose.startswith('-'):
            fkCtrl = 'FK' + pose.split('_')[0]+'_'+pose.split('_')[1]
            if cmds.objExists(fkCtrl):
                animNodeList = cmds.listConnections(fkCtrl,type='animCurveTA')
                if animNodeList:
                    cmds.delete(animNodeList)

                # 删除控制器动画之后，将控制器上的数值恢复默认
                for axis in ['rx','ry','rz']:
                    cmds.setAttr('{}.{}'.format(fkCtrl,axis),0)
        # 将时间轴设置为第一帧
        cmds.currentTime(1)


    def del_animNode(self,fkCtrl,axis):
        animNode = cmds.listConnections('{}.{}'.format(fkCtrl,axis),type='animCurveTA')
        if animNode:
            cmds.delete(animNode)


    def click_updateDriver(self, ListWidget_01,mirror_cb):
        mirror = mirror_cb.isChecked()
        pose = ListWidget_01.currentItem().text()
        fkCtrl = 'FK' + pose.split('_')[0] + '_' + pose.split('_')[1]
        pose_R = pose.replace('_L_', '_R_')
        fkCtrl_R = fkCtrl.replace('_L', '_R')
        axisList = ['rx', 'ry', 'rz']
        valueList = [cmds.getAttr('{}.{}'.format(fkCtrl, axis)) for axis in ['rx', 'ry', 'rz']]

        if not pose.startswith('-'):
            tool.update_poseHide_Info(pose)
            tool.update_PoseLocPosition(pose)
            tool.update_animNode(pose)
            om.MGlobal_displayInfo('QBJ_Tip : Update Driver successfully !')

            if mirror:
                # 是否采用存储数值的方式进行设置？？？？
                for i in range(len(axisList)):
                    cmds.setAttr('{},{}'.format(fkCtrl_R,axisList[i]),valueList[i])

                tool.update_poseHide_Info(pose_R)
                tool.update_PoseLocPosition(pose_R)
                tool.update_animNode(pose_R)

                for i in range(len(axisList)):
                    cmds.setAttr('{},{}'.format(fkCtrl_R,axisList[i]),0)
                om.MGlobal_displayInfo('QBJ_Tip : Update Driver successfully !')



    def click_updateFingerDriver(self):
        mirror = self.finger_mirror_CB.isChecked()


        if self.finger_ListWidget_01.currentItem():
            pose = self.finger_ListWidget_01.currentItem().text()
            tool.update_fingerPoseHide_Info(pose)
            tool.update_fingerAnimNode(pose)
            om.MGlobal_displayInfo('QBJ_Tip : Update Driver successfully !')
            if mirror:
                pose_R = pose.replace('_L_', '_R_')
                tool.update_fingerPoseHide_Info(pose_R)
                tool.update_fingerAnimNode(pose_R)
                om.MGlobal_displayInfo('QBJ_Tip : Update Driver successfully !')



    def click_addPose(self,ListWidget_01):
        index =  ListWidget_01.currentIndex().row()
        print 'click_addPose'


    def click_fingerAddPose(self):
        print 'click_fingerAddPose'


    def click_removePose(self,ListWidget_01):
        index = ListWidget_01.currentIndex().row()
        print 'click_removePose'


    def click_resetPose(self,ListWidget_01):
        print 'click_resetPose'


    def loadFingerDriverInfo(self):
        fingerPoseGrp = 'Finger_L_poseGrp'
        fingerPose = self.finger_ListWidget_01.currentItem().text()
        # 将poseGrp上的数据显示在driver_LineEdit中
        if not fingerPose.startswith('-'):
            if cmds.objExists(fingerPoseGrp):
                value = cmds.getAttr('{}.{}'.format(fingerPoseGrp, fingerPose))
                self.driver_LineEdit.setText('{}.{}'.format(fingerPoseGrp, fingerPose))
                self.driver_value_LineEdit.setText('{}'.format(round(value, 4)))
        else:
            self.driver_LineEdit.setText('')
            self.driver_value_LineEdit.setText('')


    def set_fingerRotateLineEdit_Value(self):
        self.driver_LineEdit.clear()
        self.clear_RotateLineEdit_Value()
        fingerPose = self.finger_ListWidget_01.currentItem().text()
        hideGrp = 'Finger_L_poseGrp_Hide'
        if cmds.objExists(hideGrp):
            if not fingerPose.startswith('-'):
                valueList = cmds.getAttr('{}.{}'.format(hideGrp,fingerPose))
                self.rotate_LineEdit_01.setText(str(valueList[0][0]))
                self.rotate_LineEdit_02.setText(str(valueList[0][1]))
                self.rotate_LineEdit_03.setText(str(valueList[0][2]))


    def lock_allItem(self,ListWidget_01,sculpt_Btn):
        # 将sculpt_Btn设置为不可选
        sculpt_Btn.setEnabled(False)
        pose = ListWidget_01.currentItem().text()
        # 将除了选择的当前item以外的,都设置为不可选状态
        for i in range(ListWidget_01.count()):
            pose = ListWidget_01.item(i)
            currentPose= ListWidget_01.currentItem()
            pose.setFlags(pose.flags() & ~QtCore.Qt.ItemIsEnabled)
            currentPose.setFlags(pose.flags() | QtCore.Qt.ItemIsEnabled)


    def unlock_allItem(self,ListWidget_01,sculpt_Btn):
        # 将sculpt_Btn设置为可选
        sculpt_Btn.setEnabled(True)
        # 将除了选择的当前item以外的,都设置为可选状态
        for i in range(ListWidget_01.count()):
            pose = ListWidget_01.item(i)
            pose.setFlags(pose.flags() | QtCore.Qt.ItemIsEnabled)


