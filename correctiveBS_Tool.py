# .-*- coding: utf-8 -*-
# .FileName:correctiveBS_Tool
# .Date....:2022-03-21 : 11 :10
# .Author..:Qian binJie
# .Contact.:1075064966@qq.com
'''
launch :
        import correctiveBS_Tool as QBJ_correctiveBS_Tool
        reload(QBJ_correctiveBS_Tool)
'''
import collections
import maya.cmds as cmds
import maya.OpenMaya as om
import system.advSystem as adv
reload(adv)
import system.humanikSystem as humanik
reload(humanik)
import system.userDefinedSystem as user
reload(user)


class CorrectiveBsTool(object):

    default_attribute_list = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz','.v']

    angleReadableDict = {'Up':1,
                         'Down':1,
                         'Front':2,
                         'Back':2,
                         'UpFront':0,
                        'UpBack':0,
                        'DownFront':2,
                        'DownBack':2}

    L_fingerPoseList = []
    L_fingerPoseDict = collections.OrderedDict(L_fingerPoseList)
    L_fingerPoseDict['IndexFinger1_L_Up']=[0,-45,0]
    L_fingerPoseDict['IndexFinger1_L_Down']=[0,90,0]
    L_fingerPoseDict['IndexFinger2_L_Down']=[0,90,0]
    L_fingerPoseDict['IndexFinger3_L_Down']=[0,90,0]
    L_fingerPoseDict['MiddleFinger1_L_Up']=[0,-45,0]
    L_fingerPoseDict['MiddleFinger1_L_Down']=[0,90,0]
    L_fingerPoseDict['MiddleFinger2_L_Down']=[0,90,0]
    L_fingerPoseDict['MiddleFinger3_L_Down']=[0,90,0]
    L_fingerPoseDict['RingFinger1_L_Up']=[0,-45,0]
    L_fingerPoseDict['RingFinger1_L_Down']=[0,90,0]
    L_fingerPoseDict['RingFinger2_L_Down']=[0,90,0]
    L_fingerPoseDict['RingFinger3_L_Down']=[0,90,0]
    L_fingerPoseDict['PinkyFinger1_L_Up']=[0,-45,0]
    L_fingerPoseDict['PinkyFinger1_L_Down']=[0,90,0]
    L_fingerPoseDict['PinkyFinger2_L_Down']=[0,90,0]
    L_fingerPoseDict['PinkyFinger3_L_Down']=[0,90,0]
    L_fingerPoseDict['ThumbFinger1_L_Up']=[0,-45,0]
    L_fingerPoseDict['ThumbFinger1_L_Down']=[0,20,0]
    L_fingerPoseDict['ThumbFinger2_L_Down']=[0,45,0]
    L_fingerPoseDict['ThumbFinger3_L_Down']=[0,90,0]

    R_fingerPoseList = []
    R_fingerPoseDict = collections.OrderedDict(R_fingerPoseList)
    R_fingerPoseDict['IndexFinger1_R_Up'] = [0, -45, 0]
    R_fingerPoseDict['IndexFinger1_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['IndexFinger2_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['IndexFinger3_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['MiddleFinger1_R_Up'] = [0, -45, 0]
    R_fingerPoseDict['MiddleFinger1_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['MiddleFinger2_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['MiddleFinger3_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['RingFinger1_R_Up'] = [0, -45, 0]
    R_fingerPoseDict['RingFinger1_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['RingFinger2_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['RingFinger3_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['PinkyFinger1_R_Up'] = [0, -45, 0]
    R_fingerPoseDict['PinkyFinger1_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['PinkyFinger2_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['PinkyFinger3_R_Down'] = [0, 90, 0]
    R_fingerPoseDict['ThumbFinger1_R_Up'] = [0, -45, 0]
    R_fingerPoseDict['ThumbFinger1_R_Down'] = [0, 20, 0]
    R_fingerPoseDict['ThumbFinger2_R_Down'] = [0, 45, 0]
    R_fingerPoseDict['ThumbFinger3_R_Down'] = [0, 90, 0]


    def __init__(self):
        pass

    def mesh_judge(self,object):
        '''
        :param object: 需要被判断的对象
        :return: 是否为mesh对象
        '''
        cmds.select(object,r=True)
        cmds.pickWalk(direction='down')
        child = cmds.ls(sl=1)
        cmds.select(cl=True)
        if cmds.nodeType(child) == 'mesh':
            return True
        else:
            return None


    def load_BaseGeo(self):
        u'''
        :return: 返回选择的polygon 名称
        '''
        baseGeo = cmds.ls(sl=True)
        if len(baseGeo) == 1:
            if self.mesh_judge(baseGeo):
                return baseGeo[0]
            else:
                om.MGlobal_displayWarning('QBJ_Tip : Please select "polygon" !! ')
        else:
            om.MGlobal_displayWarning('QBJ_Tip : Please select only one object !! ')


    def return_defaultTargetGeo(self,baseGeo):
        if baseGeo:
            targetGeo = baseGeo + '_target'
            if cmds.ls(targetGeo):
                return targetGeo


    def load_targetGeo(self):
        targetGeo = cmds.ls(sl=True)
        if len(targetGeo) == 1:
            if self.mesh_judge(targetGeo):
                return targetGeo[0]
            else:
                om.MGlobal_displayWarning('QBJ_Tip : Please select "polygon" !! ')
        else:
            om.MGlobal_displayWarning('QBJ_Tip : Please select only one object !! ')


    def get_blendshape(self,baseGeo):
        if baseGeo:
            baseGeo_history = cmds.listHistory(baseGeo,pruneDagObjects=True)
            bs_node = cmds.ls(baseGeo_history,type='blendShape')
            if bs_node :
                return bs_node
            else:
                return None


    def add_blendShape(self,baseGeo):
        # 检查场景中是否存在targetGeoGrp，如果没有就创建
        targetGeoGrp = '{}_bsTarget_Grp'.format(baseGeo)
        if not cmds.objExists(targetGeoGrp):
            targetGeoGrp = cmds.group(name='{}_bsTarget_Grp'.format(baseGeo), empty=True, world=True)

        # 给baseGeo添加blendShape
        if  baseGeo:
            default_targetGeoName = baseGeo + '_target'
            if self.return_defaultTargetGeo(baseGeo):
                targetGeo = self.return_defaultTargetGeo(baseGeo)
                if not self.get_blendshape(baseGeo):
                    blendShapeNode = cmds.blendShape(baseGeo,
                                                     name='{}_bs'.format(baseGeo),frontOfChain=True,tc=True)
                    return default_targetGeoName,blendShapeNode
            else:
                targetGeo = cmds.duplicate(baseGeo,name = '{}_target'.format(baseGeo))
                cmds.parent(targetGeo, targetGeoGrp)
                cmds.setAttr('{}.v'.format(targetGeo[0]),0)
                cmds.select(cl=True)
                if not self.get_blendshape(baseGeo):
                    blendShapeNode = cmds.blendShape( baseGeo,
                                                     name='{}_bs'.format(baseGeo), frontOfChain=True, tc=True)
                    return targetGeo[0],blendShapeNode


    def del_blendShape(self,bs_node):
       if bs_node:
           cmds.delete(bs_node)


    def del_targetGeo(self,targetGeo):
        if targetGeo:
            cmds.delete(targetGeo)


    def create_finger_PoseGrp(self,joint,fingerPoseDict):
        allPoseGrp = 'QBJ_all_PoseGrp'
        # 如果没有allPoseGrp，就创建一个
        if not cmds.objExists(allPoseGrp):
            allPoseGrp = cmds.group(name='QBJ_all_PoseGrp',empty=True,world=True)
            cmds.select(cl=True)

        # 生成finger_poseGrp
        if not cmds.objExists('{}_poseGrp'.format(joint)):
            finger_poseGrp = cmds.group(name='{}_poseGrp'.format(joint),empty=True, parent=allPoseGrp)
            cmds.select(cl=True)
            finger_poseHide = cmds.group(name='{}_poseGrp_Hide'.format(joint), empty=True,parent=finger_poseGrp)

            for attr in self.default_attribute_list:
                cmds.setAttr('{}{}'.format(finger_poseGrp, attr), lock=True, keyable=False, channelBox=False)
                cmds.setAttr('{}{}'.format(finger_poseHide, attr), lock=True, keyable=False, channelBox=False)

            # 将fingerPoseList中的item，添加进finger_poseGrp的属性
            animNodeList = []
            for pose,value in fingerPoseDict.items():
                cmds.addAttr(finger_poseGrp,longName = pose,attributeType='double',keyable=True)

                # 将fingerPoseList中的pose,value，添加进finger_poseGrp_Hide的,并隐藏
                firstValue = value[0]
                secondValue = value[1]
                thirdValue = value[2]

                cmds.addAttr(finger_poseHide, longName='{}'.format(pose),
                             attributeType='double3',
                             keyable=False, readable=False)

                cmds.addAttr(finger_poseHide, longName='{}_01'.format(pose),
                             attributeType='double',
                             parent=pose,
                             keyable=False)

                cmds.addAttr(finger_poseHide, longName='{}_02'.format(pose),
                             attributeType='double',
                             parent=pose,
                             keyable=False)

                cmds.addAttr(finger_poseHide, longName='{}_03'.format(pose),
                             attributeType='double',
                             parent=pose,
                             keyable=False)

                cmds.setAttr('{}.{}'.format(finger_poseHide, pose),
                             firstValue, secondValue, thirdValue, keyable=False, channelBox=False)

                # 创建animNode节点
                animNode = cmds.createNode('animCurveUU',name='{}_animUU'.format(pose))
                animNodeList.append(animNode)
                # 设置animNode节点
                cmds.setAttr('{}.preInfinity'.format(animNode), 0)
                cmds.setAttr('{}.postInfinity'.format(animNode), 0)

                cmds.setKeyframe(animNode,float=0,value=0, itt='Linear', ott='Linear')
                cmds.setKeyframe(animNode, float=value[1], value=1, itt='Linear',
                                 ott='Linear')
                cmds.connectAttr('{}.output'.format(animNode),'{}.{}'.format(finger_poseGrp,pose))

            # 将骨骼上的旋转值，连接到对应的animNode上
            for node in animNodeList:
                fingerJoint =  node.split('_')[0] + '_' +node.split('_')[1]
                cmds.connectAttr('{}.ry'.format(fingerJoint),'{}.input'.format(node))


    def update_PoseLocPosition(self,ListWidget_01):
        # 获取当前选择的ListWidget item
        currectSelectItem = ListWidget_01.currentItem().text()

        if not currectSelectItem.startswith('-'):
            # 根据命名获取到对应的poseLoc和poseReaderLoc,重新放置poseLoc位置
            currectPoseLoc = currectSelectItem + '_loc'
            currectPoseReaderLoc = currectSelectItem.split('_')[0] + '_' + currectSelectItem.split('_')[
                1] + '_poseReader_loc'
            # 将PoseLoc定位到新的位置

            for axis in ['tx','ty','tz']:
                cmds.setAttr('{}.{}'.format(currectPoseLoc,axis),lock=False)

            locParentConstraint = cmds.parentConstraint(currectPoseReaderLoc,currectPoseLoc,maintainOffset=False)
            cmds.delete(locParentConstraint)

            for axis in ['tx', 'ty', 'tz']:
                cmds.setAttr('{}.{}'.format(currectPoseLoc, axis), lock=True)


    def update_poseHide_Info(self,ListWidget_01):
        # 获取当前选择到的控制器
        selectCtrl = cmds.ls(sl=True, type='transform')

        # 获取当前选择的ListWidget item
        currectSelectItem = ListWidget_01.currentItem().text()

        if not currectSelectItem.startswith('-'):
            fkCtrl = 'FK' + currectSelectItem.split('_')[0]+'_'+currectSelectItem.split('_')[1]
            poseGrp_Hide = currectSelectItem.split('_')[0]+'_'+currectSelectItem.split('_')[1] + '_poseGrp_Hide'
            attr = currectSelectItem.split('_')[-1]

            # 如果所选的控制器是正确的控制器，则获取此时控制器上的rotate数值，并将数值重新设置给对应的属性
            if selectCtrl:
                if selectCtrl[0] == fkCtrl:
                    valueList = [cmds.getAttr('{}.{}'.format(selectCtrl[0],axis)) for axis in ['rx','ry','rz']]
                    cmds.setAttr('{}.{}'.format(poseGrp_Hide,attr),valueList[0],valueList[1],valueList[2])
                else:
                    om.MGlobal_displayError('QBJ_Tip : Please select relevant controller !!!')
            else:
                om.MGlobal_displayError('QBJ_Tip : Please select one controller !!!')


    def update_animNode(self,ListWidget_01):
        # 获取当前选择的ListWidget item
        currectSelectItem = ListWidget_01.currentItem().text()
        poseGrp_Hide = currectSelectItem.split('_')[0] + '_' + currectSelectItem.split('_')[1] + '_poseGrp_Hide'
        current_animNode = currectSelectItem+'_animUU'
        direction = currectSelectItem.split('_')[-1]
        valueList =  cmds.getAttr('{}.{}'.format(poseGrp_Hide,direction))
        valueIndex = self.angleReadableDict[direction]
        print valueList,valueIndex
        cmds.keyframe(current_animNode, index=(1,1),floatChange= valueList[0][valueIndex],option='over', absolute=True)


