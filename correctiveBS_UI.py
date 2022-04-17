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
import system.advSystem as ADV
reload(ADV)
adv = ADV.advSystem()
import system.humanikSystem as HUMANIK
reload(HUMANIK)
humanik = HUMANIK.humanIKSystem()
import system.userDefinedSystem as UESR
reload(UESR)
user = UESR.userDedinedSystem()



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
        self.humanIK_radioBtn.setEnabled(False)
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
        self.copyRight_label.setText('Copyright(C) 2022—— Rigging | QBJ')
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
                self.addBlendShapeConfirmDialog()


    def click_targetGeoLoad_Btn(self):
        baseGeo = self.baseGeo_LineEdit.text()
        targetGeo = self.targetGeo_LineEdit.text()
        if not targetGeo:
            if baseGeo:
                targetGeo = tool.return_defaultTargetGeo(baseGeo)
                if targetGeo:
                    self.targetGeo_LineEdit.setText(str(targetGeo))
        else:
            self.loadTargetConfirmDialog()


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
        baseGeo = self.baseGeo_LineEdit.text()
        targetGeo = self.targetGeo_LineEdit.text()
        blendShapeNode = self.blendshape_comboBox.currentText()
        currectSysytem = self.radionBtn_Grp.checkedButton().text()

        # 将poseGrp添加到arm_ListWidget_01中
        self.arm_ListWidget_01.clear()
        if currectSysytem == 'ADV':
            self.add_ListWidget_01_items(adv.arm_ADV_poseDict,self.arm_ListWidget_01)

            # 根据adv控制器的命名规则，创建poseBridge组并进行连接
            adv.create_armPoseBrige()

            # 生成blendShape targetGeo，并添加到blendShapeNode中
            if adv.create_armTargets(baseGeo,targetGeo,blendShapeNode):
                self.arm_CreateBtn.setStyleSheet(self.BUTTON_BGC)
                self.arm_CreateBtn.setEnabled(False)

        print 'armCreate'


    def click_legCreate_Btn(self):
        baseGeo = self.baseGeo_LineEdit.text()
        targetGeo = self.targetGeo_LineEdit.text()
        blendShapeNode = self.blendshape_comboBox.currentText()
        currectSysytem = self.radionBtn_Grp.checkedButton().text()

        # 将poseGrp添加到arm_ListWidget_01中
        self.leg_ListWidget_01.clear()
        if currectSysytem == 'ADV':
            self.add_ListWidget_01_items(adv.leg_ADV_poseDict,self.leg_ListWidget_01)

            # 根据adv控制器的命名规则，创建poseBridge组并进行连接
            adv.create_legPoseBrige()

            # 生成blendShape targetGeo，并添加到blendShapeNode中
            if adv.create_legTargets(baseGeo, targetGeo, blendShapeNode):
                self.leg_CreateBtn.setStyleSheet(self.BUTTON_BGC)
                self.leg_CreateBtn.setEnabled(False)

        print 'legCreate'


    def click_fingerCreate_Btn(self):
        baseGeo = self.baseGeo_LineEdit.text()
        targetGeo = self.targetGeo_LineEdit.text()
        blendShapeNode = self.blendshape_comboBox.currentText()
        currectSysytem = self.radionBtn_Grp.checkedButton().text()

        # 将poseGrp添加到arm_ListWidget_01中
        self.finger_ListWidget_01.clear()
        if currectSysytem == 'ADV':
            self.add_ListWidget_01_items(adv.finger_ADV_poseDict,self.finger_ListWidget_01)

            # 生成blendShape targetGeo，并添加到blendShapeNode中
            if adv.create_fingerTargets(baseGeo, targetGeo, blendShapeNode):
                self.finger_CreateBtn.setStyleSheet(self.BUTTON_BGC)
                self.finger_CreateBtn.setEnabled(False)

        print 'fingerCreate'


    def click_torsoCreate_Btn(self):

        baseGeo = self.baseGeo_LineEdit.text()
        targetGeo = self.targetGeo_LineEdit.text()
        blendShapeNode = self.blendshape_comboBox.currentText()
        currectSysytem = self.radionBtn_Grp.checkedButton().text()

        # 将poseGrp添加到arm_ListWidget_01中
        self.torso_ListWidget_01.clear()
        if currectSysytem == 'ADV':
            self.add_ListWidget_01_items(adv.torso_ADV_poseDict,self.torso_ListWidget_01)

            # 根据adv控制器的命名规则，创建poseBridge组并进行连接
            adv.create_torsoPoseBrige()

            # 生成blendShape targetGeo，并添加到blendShapeNode中
            if adv.create_torsoTargets(baseGeo, targetGeo, blendShapeNode):
                self.torso_CreateBtn.setStyleSheet(self.BUTTON_BGC)
                self.torso_CreateBtn.setEnabled(False)

        print 'torsoCreate'



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


    def changeTargetGeo(self):
        # 将targetGeo_LineEdit的名称 ，替换为此时用户选中的模型名称
        targetGeo = tool.load_targetGeo()
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


    def add_ListWidget_01_items(self,poseDict,listWidget):
        for ctrl, poseGrp in poseDict.items():
            if cmds.objExists(ctrl):
                for pose in poseGrp:
                    listWidget.addItem(pose)

