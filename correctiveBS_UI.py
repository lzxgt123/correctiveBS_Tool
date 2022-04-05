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


import pymel.core as pm
import maya.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets,QtCore,QtGui
import correctiveBS_Tool as CBT
reload(CBT)
tool = CBT.CorrectiveBsTool()
import confirmDialog as CD
reload(CD)
cd = CD.confirm_Dialog()

def maya_main_window():
    '''
        返回maya主窗口，使之变成一个python对象
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class CorrectiveBsUI(QtWidgets.QDialog):

    BUTTON_BGC = "background-color:rgb(142,188,255);color:black;"
    WINDOW_TITLE = 'Corrective Tool v1.0.0'
    limitAngleExpr = QtCore.QRegExp('^-?(180|([1-9]?\d|1[0-7][0-9])(\.\d{1,2})?)$')

    arm_Pose_dict = {
                     'FKScapula_L':[u'-----肩胛-----', 'Scapula_L_Up', 'Scapula_L_Down', 'Scapula_L_Front', 'Scapula_L_Back'],
                     'FKShoulder_L':[u'-----上臂-----', 'Shoulder_L_Up', 'Shoulder_L_Down', 'Shoulder_L_Front', 'Shoulder_L_Back',
                     'Shoulder_L_UpFront', 'Shoulder_L_UpBack', 'Shoulder_L_DownFront', 'Shoulder_L_DownBack'],
                     'FKElbow_L':[u'-----肘部-----', 'Elbow_L_Front'],
                     'FKWrist_L':[u'-----手腕-----', 'Wrist_L_Up', 'Wrist_L_Down', 'Wrist_L_Front', 'Wrist_L_Back', 'Wrist_L_UpFront',
                     'Wrist_L_UpBack', 'Wrist_L_DownFront', 'Wrist_L_DownBack']
                     }

    leg_Pose_dict = {
                     'FKHip_L':[u'-----腿部-----', 'Hip_L_Up', 'Hip_L_Down', 'Hip_L_Front', 'Hip_L_Back',
                     'Hip_L_UpFront', 'Hip_L_UpBack', 'Hip_L_DownFront', 'Hip_L_DownBack'],
                     'FKKnee_L':[u'-----膝盖-----',  'Knee_L_Back'],
                     'FKAnkle_L':[u'-----脚踝-----', 'Ankle_L_Up', 'Ankle_L_Down', 'Ankle_L_Front', 'Ankle_L_Back', 'Ankle_L_UpFront',
                     'Ankle_L_UpBack', 'Ankle_L_DownFront', 'Ankle_L_DownBack']
                     }

    finger_pose_dict = {
                        'FKIndexFinger1_L':[u'-----食指-----', 'IndexFinger1_L_Down', 'IndexFinger1_L_Up'],
                        'FKIndexFinger2_L': [ 'IndexFinger2_L_Down', 'IndexFinger2_L_Up'],
                        'FKIndexFinger3_L': [ 'IndexFinger3_L_Down', 'IndexFinger3_L_Up'],
                        'FKMiddleFinger1_L':[u'-----中指-----', 'MiddleFinger1_L_Down','MiddleFinger1_L_Up'],
                        'FKMiddleFinger2_L': [ 'MiddleFinger2_L_Down', 'MiddleFinger2_L_Up'],
                        'FKMiddleFinger3_L': [ 'MiddleFinger3_L_Down', 'MiddleFinger3_L_Up'],
                        'FKRingFinger1_L':[u'-----无名指-----', 'RingFinger1_L_Down','RingFinger1_L_Up'],
                        'FKRingFinger2_L': ['RingFinger2_L_Down', 'RingFinger2_L_Up'],
                        'FKRingFinger3_L': ['RingFinger3_L_Down', 'RingFinger3_L_Up'],
                        'FKPinkyFinger1_L':[u'-----小拇指-----', 'PinkyFinger1_L_Down','PinkyFinger1_L_Up'],
                        'FKPinkyFinger2_L': [ 'PinkyFinger2_L_Down', 'PinkyFinger2_L_Up'],
                        'FKPinkyFinger3_L': [ 'PinkyFinger3_L_Down', 'PinkyFinger3_L_Up'],
                        'FKThumbFinger1_L':[u'-----大拇指-----', 'ThumbFinger1_L_Down','ThumbFinger1_L_Up'],
                        'FKThumbFinger2_L': [ 'ThumbFinger2_L_Down', 'ThumbFinger2_L_Up'],
                        'FKThumbFinger3_L': [ 'ThumbFinger3_L_Down', 'ThumbFinger3_L_Up']
                        }

    torso_pose_dict = {
                        'FKHead_M':[u'-----头部-----','Head_Front','Head_Back','Head_Left','Head_Right'],
                        'FKNeck_M':[u'-----颈部-----', 'Neck_Front', 'Neck_Back', 'Neck_Left', 'Neck_Right'],
                        'FKChest_M':[u'-----胸腔-----','Chest_Front', 'Chest_Back', 'Chest_Left', 'Chest_Right'],
                        'FKSpine1_M':[u'-----躯干-----','Spine1_Front', 'Spine1_Back', 'Spine1_Left', 'Spine1_Right'],
                        'FKSpine2_M':['Spine2_Front', 'Spine2_Back', 'Spine2_Left', 'Spine2_Right']
                        }

    def __init__(self,parent=maya_main_window()):
        super(CorrectiveBsUI, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint)
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
        # self.add_Btn = QtWidgets.QPushButton('Add')
        self.del_Btn = QtWidgets.QPushButton('Del')

        # 创建分割线 组件
        self.separator_01 = QtWidgets.QFrame()
        self.separator_01.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_01.setFrameShadow(QtWidgets.QFrame.Sunken)

        # 创建 控制器类型 组件
        self.controlsType_Label = QtWidgets.QLabel('Rig System :')
        # self.spacerItem_01 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
        #                                            QtWidgets.QSizePolicy.Minimum)
        self.adv_radioBtn = QtWidgets.QRadioButton('ADV')
        self.adv_radioBtn.setChecked(True)
        self.humanIK_radioBtn = QtWidgets.QRadioButton('HumanIK')
        self.defined_radionBtn = QtWidgets.QRadioButton('Defined')
        self.defined_radionBtn.setEnabled(False)

        self.radionBtn_Grp = QtWidgets.QButtonGroup()
        self.radionBtn_Grp.addButton(self.adv_radioBtn,1)
        self.radionBtn_Grp.addButton(self.humanIK_radioBtn, 2)
        self.radionBtn_Grp.addButton(self.defined_radionBtn,3)

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
        self.arm_Splitter_01 = QtWidgets.QSplitter(self.arm_Tab)
        self.arm_Splitter_01.setMinimumSize(QtCore.QSize(400, 0))
        self.arm_Splitter_01.setOrientation(QtCore.Qt.Vertical)
        self.arm_Splitter_02 = QtWidgets.QSplitter(self.arm_Splitter_01)
        self.arm_Splitter_02.setOrientation(QtCore.Qt.Horizontal)
        self.arm_ListWidget_01 = QtWidgets.QListWidget(self.arm_Splitter_02)
        self.arm_ListWidget_02 = QtWidgets.QListWidget(self.arm_Splitter_02)
        self.arm_ListWidget_03 = QtWidgets.QListWidget(self.arm_Splitter_01)
        self.arm_Splitter_01.setStretchFactor(0, 8)
        self.arm_Splitter_01.setStretchFactor(1, 2)
        self.arm_Layout.addWidget(self.arm_CreateBtn)
        self.arm_Layout.addWidget(self.arm_Splitter_01)
        self.tabWidget.addTab(self.arm_Tab,'Arm')

        self.leg_Tab = QtWidgets.QWidget(self.tabWidget)
        self.leg_Layout = QtWidgets.QVBoxLayout(self.leg_Tab)
        self.leg_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.leg_Layout.setContentsMargins(2, 2, 2, 2)
        self.leg_Layout.setSpacing(3)
        self.leg_CreateBtn = QtWidgets.QPushButton('Create Targets')
        self.leg_Splitter_01 = QtWidgets.QSplitter(self.leg_Tab)
        self.leg_Splitter_01.setMinimumSize(QtCore.QSize(400, 0))
        self.leg_Splitter_01.setOrientation(QtCore.Qt.Vertical)
        self.leg_Splitter_02 = QtWidgets.QSplitter(self.leg_Splitter_01)
        self.leg_Splitter_02.setOrientation(QtCore.Qt.Horizontal)
        self.leg_ListWidget_01 = QtWidgets.QListWidget(self.leg_Splitter_02)
        self.leg_ListWidget_02 = QtWidgets.QListWidget(self.leg_Splitter_02)
        self.leg_ListWidget_03 = QtWidgets.QListWidget(self.leg_Splitter_01)
        self.leg_Splitter_01.setStretchFactor(0, 8)
        self.leg_Splitter_01.setStretchFactor(1, 2)
        self.leg_Layout.addWidget(self.leg_CreateBtn)
        self.leg_Layout.addWidget(self.leg_Splitter_01)
        self.tabWidget.addTab(self.leg_Tab, 'leg')

        self.finger_Tab = QtWidgets.QWidget(self.tabWidget)
        self.finger_Layout = QtWidgets.QVBoxLayout(self.finger_Tab)
        self.finger_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.finger_Layout.setContentsMargins(2, 2, 2, 2)
        self.finger_Layout.setSpacing(3)
        self.finger_CreateBtn = QtWidgets.QPushButton('Create Targets')
        self.finger_Splitter_01 = QtWidgets.QSplitter(self.finger_Tab)
        self.finger_Splitter_01.setMinimumSize(QtCore.QSize(400, 0))
        self.finger_Splitter_01.setOrientation(QtCore.Qt.Vertical)
        self.finger_Splitter_02 = QtWidgets.QSplitter(self.finger_Splitter_01)
        self.finger_Splitter_02.setOrientation(QtCore.Qt.Horizontal)
        self.finger_ListWidget_01 = QtWidgets.QListWidget(self.finger_Splitter_02)
        self.finger_ListWidget_02 = QtWidgets.QListWidget(self.finger_Splitter_02)
        self.finger_ListWidget_03 = QtWidgets.QListWidget(self.finger_Splitter_01)
        self.finger_Splitter_01.setStretchFactor(0, 8)
        self.finger_Splitter_01.setStretchFactor(1, 2)
        self.finger_Layout.addWidget(self.finger_CreateBtn)
        self.finger_Layout.addWidget(self.finger_Splitter_01)
        self.tabWidget.addTab(self.finger_Tab, 'finger')

        self.torso_Tab = QtWidgets.QWidget(self.tabWidget)
        self.torso_Layout = QtWidgets.QVBoxLayout(self.torso_Tab)
        self.torso_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.torso_Layout.setContentsMargins(2, 2, 2, 2)
        self.torso_Layout.setSpacing(3)
        self.torso_CreateBtn = QtWidgets.QPushButton('Create Targets')
        self.torso_Splitter_01 = QtWidgets.QSplitter(self.torso_Tab)
        self.torso_Splitter_01.setMinimumSize(QtCore.QSize(400, 0))
        self.torso_Splitter_01.setOrientation(QtCore.Qt.Vertical)
        self.torso_Splitter_02 = QtWidgets.QSplitter(self.torso_Splitter_01)
        self.torso_Splitter_02.setOrientation(QtCore.Qt.Horizontal)
        self.torso_ListWidget_01 = QtWidgets.QListWidget(self.torso_Splitter_02)
        self.torso_ListWidget_02 = QtWidgets.QListWidget(self.torso_Splitter_02)
        self.torso_ListWidget_03 = QtWidgets.QListWidget(self.torso_Splitter_01)
        self.torso_Splitter_01.setStretchFactor(0, 8)
        self.torso_Splitter_01.setStretchFactor(1, 2)
        self.torso_Layout.addWidget(self.torso_CreateBtn)
        self.torso_Layout.addWidget(self.torso_Splitter_01)
        self.tabWidget.addTab(self.torso_Tab, 'torso')

        self.other_Tab = QtWidgets.QWidget(self.tabWidget)
        self.other_Layout = QtWidgets.QVBoxLayout(self.other_Tab)
        self.other_Layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.other_Layout.setContentsMargins(2, 2, 2, 2)
        self.other_Layout.setSpacing(3)
        self.other_CreateBtn = QtWidgets.QPushButton('Create Targets')
        self.other_Splitter_01 = QtWidgets.QSplitter(self.other_Tab)
        self.other_Splitter_01.setMinimumSize(QtCore.QSize(400, 0))
        self.other_Splitter_01.setOrientation(QtCore.Qt.Vertical)
        self.other_Splitter_02 = QtWidgets.QSplitter(self.other_Splitter_01)
        self.other_Splitter_02.setOrientation(QtCore.Qt.Horizontal)
        self.other_ListWidget_01 = QtWidgets.QListWidget(self.other_Splitter_02)
        self.other_ListWidget_02 = QtWidgets.QListWidget(self.other_Splitter_02)
        self.other_ListWidget_03 = QtWidgets.QListWidget(self.other_Splitter_01)
        self.other_Splitter_01.setStretchFactor(0, 8)
        self.other_Splitter_01.setStretchFactor(1, 2)
        self.other_Layout.addWidget(self.other_CreateBtn)
        self.other_Layout.addWidget(self.other_Splitter_01)
        self.tabWidget.addTab(self.other_Tab, 'other')


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
        self.load_GridLayout.setVerticalSpacing(4)
        self.load_GridLayout.addWidget(self.baseGeo_Label,0,0,1,1)
        self.load_GridLayout.addWidget(self.baseGeo_LineEdit, 0, 1, 1, 4)
        self.load_GridLayout.addWidget(self.baseGeo_Btn, 0, 5, 1, 1)
        self.load_GridLayout.addWidget(self.targetGeo_Label, 1, 0, 1, 1)
        self.load_GridLayout.addWidget(self.targetGeo_LineEdit, 1, 1, 1, 4)
        self.load_GridLayout.addWidget(self.targetGeo_Btn, 1, 5, 1, 1)
        self.load_GridLayout.addWidget(self.blendshape_Label, 2, 0, 1, 1)
        self.load_GridLayout.addWidget(self.blendshape_comboBox, 2, 1, 1, 4)
        # self.load_GridLayout.addWidget(self.add_Btn, 3, 4, 1, 1)
        self.load_GridLayout.addWidget(self.del_Btn, 2, 5, 1, 1)

        # 创建控制器类型 布局
        self.type_layout = QtWidgets.QHBoxLayout()
        self.type_layout.setContentsMargins(2,2,2,2)
        self.type_layout.addWidget(self.controlsType_Label)
        self.type_layout.addWidget(self.adv_radioBtn)
        self.type_layout.addWidget(self.humanIK_radioBtn)
        self.type_layout.addWidget(self.defined_radionBtn)

        # 创建sculpt布局
        self.sculpt_Layout = QtWidgets.QHBoxLayout()
        self.sculpt_Layout.setContentsMargins(2,2,2,2)
        self.sculpt_Layout.addWidget(self.sculpt_Btn)
        self.sculpt_Layout.addWidget(self.mirror_Btn)
        self.sculpt_Layout.addWidget(self.exit_Btn)

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
        main_Layout.addLayout(self.sculpt_Layout)
        main_Layout.addWidget(self.separator_02)
        main_Layout.addWidget(self.copyRight_label)

    def create_connections(self):
        self.baseGeo_Btn.clicked.connect(self.click_BaseGeoLoad_Btn)
        self.targetGeo_Btn.clicked.connect(self.click_targetGeoLoad_Btn)
        # self.add_Btn.clicked.connect(self.click_addBS_Btn)
        self.del_Btn.clicked.connect(self.click_delBs_Btn)
        self.sculpt_Btn.clicked.connect(self.click_sculpt_Btn)
        self.mirror_Btn.clicked.connect(self.click_mirror_Btn)
        self.exit_Btn.clicked.connect(self.click_exit_Btn)

        self.arm_CreateBtn.clicked.connect(self.click_armCreate_Btn)
        self.leg_CreateBtn.clicked.connect(self.click_legCreate_Btn)
        self.finger_CreateBtn.clicked.connect(self.click_fingerCreate_Btn)
        self.torso_CreateBtn.clicked.connect(self.click_torsoCreate_Btn)
        self.other_CreateBtn.clicked.connect(self.click_otherCreate_Btn)


    def click_BaseGeoLoad_Btn(self):
        # 获取 baseGeo
        baseGeo = tool.load_BaseGeo()
        # 将获取到的baseGeo名称，加载到baseGeo_LineEdit中
        if baseGeo:
            self.baseGeo_LineEdit.setText(str(baseGeo))
            # 检查场景中是否存在targetGeo
            if tool.return_defaultTargetGeo(baseGeo):
                targetGeo = tool.return_defaultTargetGeo(baseGeo)
                self.targetGeo_LineEdit.setText(str(targetGeo))

            bsNode = tool.get_blendshape(baseGeo)

            if bsNode:
                if len(bsNode) == 1:
                    self.blendshape_comboBox.addItem(bsNode[0])
                else :
                    om.MGlobal_displayError('QBJ_Tip : More than one blendShape node on the object !!!')
                    return
            else:
                cd.addBlendShapeConfirmDialog(self.create_blendShape)


    def click_targetGeoLoad_Btn(self):
        baseGeo = self.baseGeo_LineEdit.text()
        targetGeo = self.targetGeo_LineEdit.text()
        if not targetGeo:
            if baseGeo:
                targetGeo = tool.return_defaultTargetGeo(baseGeo)
                if targetGeo:
                    self.targetGeo_LineEdit.setText(str(targetGeo))
        else:
            cd.loadTargetConfirmDialog(self.changeTargetGeo)


    def click_delBs_Btn(self):
        bsNode = self.blendshape_comboBox.currentText()
        targetGeo = self.targetGeo_LineEdit.text()
        if bsNode:
            tool.del_blendShape(bsNode)
            self.blendshape_comboBox.clear()
        if targetGeo:
            tool.del_targetGeo(targetGeo)
            self.targetGeo_LineEdit.clear()
            om.MGlobal_displayInfo('QBJ_Tip : Delete blendShape Node successfully !')


    def click_armCreate_Btn(self):
        print 'armCreate'



    def click_legCreate_Btn(self):
        print 'legCreate'
        pass

    def click_fingerCreate_Btn(self):
        print 'fingerCreate'
        pass

    def click_torsoCreate_Btn(self):
        print 'torsoCreate'
        pass

    def click_otherCreate_Btn(self):
        print 'otherCreate'
        pass


    def click_sculpt_Btn(self):
        print 'sculpt'
        pass


    def click_mirror_Btn(self):
        print 'mirror'
        pass


    def click_exit_Btn(self):
        print 'exit'
        pass


    def create_blendShape(self):
        # 为 baseGeo 创建blendShape，并将生成的target和bsNode加载到Gui中
        baseGeo = self.baseGeo_LineEdit.text()
        if baseGeo:
            targetGeo_bsNode_list = tool.add_blendShape(baseGeo)
            self.targetGeo_LineEdit.setText(str(targetGeo_bsNode_list[0]))
            self.blendshape_comboBox.addItem(str(targetGeo_bsNode_list[1][0]))
            om.MGlobal_displayInfo('QBJ_Tip : Add blendShape successfully !')

        cd.addBlendShapeConfirm_Dialog.close()


    def changeTargetGeo(self):
        # 将targetGeo_LineEdit的名称 ，替换为此时用户选中的模型名称
        targetGeo = tool.load_targetGeo()
        if targetGeo:
            self.targetGeo_LineEdit.setText(str(targetGeo))

        cd.loadTargetConfirm_Dialog.close()

