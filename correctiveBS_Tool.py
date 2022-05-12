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
import cvshapeinverter
import collections
import maya.cmds as cmds
import  pymel.core as pm
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
        obj = pm.PyNode(object[0])
        objShape = obj.getShape()
        if objShape:
            objShapeType = objShape.nodeType()
            if objShapeType == 'mesh':
                return True
            else:
                return None
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


    def return_defaultTargetGeo(self, baseGeo):
        if baseGeo:
            targetGeo = baseGeo + '_target'
            if cmds.objExists(targetGeo):
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

    def add_bsTargetInfo(self,baseGeo,allPoseList):
        '''
        在bsTargetGrp组上添加每一个pose，用来记录pose对应生成的bsTarget信息
        :param baseGeo: 修型目标
        :return: None
        '''
        bsTargetGrp = '{}_bsTarget_Grp'.format(baseGeo)
        bsTargetGrp_attrs= []
        if cmds.listAttr(bsTargetGrp,userDefined=True):
            bsTargetGrp_attrs = [attr for attr in cmds.listAttr(bsTargetGrp,userDefined=True)]

        if bsTargetGrp:
            for pose in allPoseList:
                if not pose.startswith('-'):
                    if pose not in bsTargetGrp_attrs:
                        cmds.addAttr(bsTargetGrp,longName='%s'%pose,dataType='string',keyable=False)
                        # cmds.setAttr('{}.{}'.format(bsTargetGrp, pose), '{};'.format(pose), type='string')


    def add_blendShape(self,baseGeo,targetGeo,allPoseList):
        # 检查场景中是否存在targetGeoGrp，如果没有就创建
        bsTargetGrp = '{}_bsTarget_Grp'.format(baseGeo)
        if not cmds.objExists(bsTargetGrp):
            bsTargetGrp = cmds.group(name='{}_bsTarget_Grp'.format(baseGeo), empty=True, world=True)
            self.add_bsTargetInfo(baseGeo,allPoseList)

        # 给baseGeo添加blendShape
        if  baseGeo:
            default_targetGeoName = baseGeo + '_target'
            if targetGeo:
                if not self.get_blendshape(baseGeo):
                    blendShapeNode = cmds.blendShape(baseGeo,
                                                     name='{}_bs'.format(baseGeo),frontOfChain=True,tc=True)
                    return default_targetGeoName,blendShapeNode
            else:
                targetGeo = cmds.duplicate(baseGeo,name = '{}_target'.format(baseGeo))
                cmds.parent(targetGeo, bsTargetGrp)
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


    def update_PoseLocPosition(self,pose):

        if not pose.startswith('-'):
            # 根据命名获取到对应的poseLoc和poseReaderLoc,重新放置poseLoc位置
            currectPoseLoc = pose + '_loc'
            currectPoseReaderLoc = pose.split('_')[0] + '_' + pose.split('_')[
                1] + '_poseReader_loc'
            # 将PoseLoc定位到新的位置

            for axis in ['tx','ty','tz']:
                cmds.setAttr('{}.{}'.format(currectPoseLoc,axis),lock=False)

            locParentConstraint = cmds.parentConstraint(currectPoseReaderLoc,currectPoseLoc,maintainOffset=False)
            cmds.delete(locParentConstraint)

            for axis in ['tx', 'ty', 'tz']:
                cmds.setAttr('{}.{}'.format(currectPoseLoc, axis), lock=True)


    def update_poseHide_Info(self,pose):
        # 获取当前选择到的控制器
        selectCtrl = cmds.ls(sl=True, type='transform')

        if not pose.startswith('-'):
            fkCtrl = 'FK' + pose.split('_')[0]+'_'+pose.split('_')[1]
            poseGrp_Hide = pose.split('_')[0]+'_'+pose.split('_')[1] + '_poseGrp_Hide'
            attr = pose.split('_')[-1]

            # 如果所选的控制器是正确的控制器，则获取此时控制器上的rotate数值，并将数值重新设置给对应的属性
            if selectCtrl:
                if selectCtrl[0] == fkCtrl:
                    valueList = [cmds.getAttr('{}.{}'.format(selectCtrl[0],axis)) for axis in ['rx','ry','rz']]
                    cmds.setAttr('{}.{}'.format(poseGrp_Hide,attr),valueList[0],valueList[1],valueList[2])
                else:
                    om.MGlobal_displayError('QBJ_Tip : Please select relevant controller !!!')
            else:
                om.MGlobal_displayError('QBJ_Tip : Please select one controller !!!')


    def update_animNode(self,pose):

        poseGrp_Hide = pose.split('_')[0] + '_' + pose.split('_')[1] + '_poseGrp_Hide'
        current_animNode = pose+'_animUU'
        direction = pose.split('_')[-1]
        valueList =  cmds.getAttr('{}.{}'.format(poseGrp_Hide,direction))
        valueIndex = self.angleReadableDict[direction]
        cmds.keyframe(current_animNode, index=(1,1),floatChange= valueList[0][valueIndex],option='over', absolute=True)


    def update_fingerPoseHide_Info(self,pose):
        # 获取当前选择到的控制器
        selectCtrl = cmds.ls(sl=True, type='transform')

        if not pose.startswith('-'):
            fkCtrl = 'FK' + pose.split('_')[0] + '_' + pose.split('_')[1]
            poseGrp_Hide = 'Finger_L_poseGrp_Hide'

            # 如果所选的控制器是正确的控制器，则获取此时控制器上的rotate数值，并将数值重新设置给对应的属性
            if selectCtrl:
                if selectCtrl[0] == fkCtrl:
                    valueList = [cmds.getAttr('{}.{}'.format(selectCtrl[0], axis)) for axis in ['rx', 'ry', 'rz']]
                    cmds.setAttr('{}.{}'.format(poseGrp_Hide, pose), valueList[0], valueList[1], valueList[2])
                else:
                    om.MGlobal_displayError('QBJ_Tip : Please select relevant controller !!!')
            else:
                om.MGlobal_displayError('QBJ_Tip : Please select one controller !!!')


    def update_fingerAnimNode(self,pose):

        poseGrp_Hide = 'Finger_L_poseGrp_Hide'
        current_animNode = pose+'_animUU'
        direction = pose.split('_')[-1]
        valueList =  cmds.getAttr('{}.{}'.format(poseGrp_Hide,pose))
        valueIndex = self.angleReadableDict[direction]
        cmds.keyframe(current_animNode, index=(0,0),floatChange= valueList[0][valueIndex],option='over', absolute=True)


    def set_refVis(self,geo):
        if geo:
            cmds.setAttr('{}Shape.overrideDisplayType'.format(geo),2)

    def set_normalVis(self,geo):
        if geo:
            cmds.setAttr('{}Shape.overrideDisplayType'.format(geo),0)


    def set_GeoVisAnimation(self,baseGeo,sculptGeo):
        baseGeo_AnimNode = cmds.createNode('animCurveTU',name = '{}_vis_animNode'.format(baseGeo),
                                           skipSelect=True)
        cmds.connectAttr('{}.output'.format(baseGeo_AnimNode),'{}.v'.format(baseGeo))
        cmds.setKeyframe(baseGeo_AnimNode,t=20,v=1,inTangentType='Spline',outTangentType='Stepped')
        cmds.setKeyframe(baseGeo_AnimNode, t=21, v=0, inTangentType='Spline', outTangentType='Stepped')

        sculptGeo_AnimNode = cmds.createNode('animCurveTU', name='{}_vis_animNode'.format(sculptGeo),
                                           skipSelect=True)
        cmds.connectAttr('{}.output'.format(sculptGeo_AnimNode), '{}.v'.format(sculptGeo))
        cmds.setKeyframe(sculptGeo_AnimNode, t=20, v=0, inTangentType='Spline', outTangentType='Stepped')
        cmds.setKeyframe(sculptGeo_AnimNode, t=21, v=1, inTangentType='Spline', outTangentType='Stepped')


    def del_GeoVisAnimation(self,baseGeo,sculptGeo):
        '''
        删除baseGeo和sculptGeo上的显示动画
        :param baseGeo:
        :param sculptGeo:
        :return:
        '''
        baseGeo_AnimNode = '{}_vis_animNode'.format(baseGeo)
        sculptGeo_AnimNode = '{}_vis_animNode'.format(sculptGeo)
        # 如果存在以下两个动画节点,就删除
        if baseGeo_AnimNode:
            cmds.delete(baseGeo_AnimNode)

        if sculptGeo_AnimNode:
            cmds.delete(sculptGeo_AnimNode)
        # 将baseGeo设置为显示
        cmds.setAttr('{}.v'.format(baseGeo),1)


    def enterSculptMode(self,baseGeo,bsNode,pose,targetOri_Geo,mirror,poseGrp):
        sculptGeo = '{}_{}_sculpt'.format(baseGeo, pose)

        # 检查场景中是否在target_Geo，没有就创建，并放置于bsTarget_Grp中
        self.create_targetGeo(baseGeo, pose, targetOri_Geo, mirror)
        # 将生成的 target
        self.add_newTargetGeo_To_BsNode(baseGeo, pose, targetOri_Geo, mirror, bsNode,poseGrp)
        # 创建修型所需的临时雕刻模型组
        self.create_tempSculptGrp(baseGeo,bsNode,pose,targetOri_Geo)
        # 获取baseGeo,并将其设置为参考模式
        self.set_refVis(baseGeo)
        # 设置baseGe,sculptGeo显示动画
        self.set_GeoVisAnimation(baseGeo, sculptGeo)


    def create_tempSculptGrp(self,baseGeo,bsNode,pose,targetOri_Geo):
        tempSculptGrp = '{}_tempSculptGrp'.format(pose)
        # 检查场景中是否存在 tempSculptGrp
        if not cmds.objExists(tempSculptGrp):
            # 创建tempSculptGrp
            tempSculptGrp = cmds.group(name='{}_tempSculptGrp'.format(pose),world=True,empty=True)

        # 复制baseGeo，得到sculptGeo,并将显示模式设置为正常
        sculptGeo = cmds.duplicate(baseGeo,name = '{}_{}_sculpt'.format(baseGeo,pose))
        self.set_sculptGeo_color(sculptGeo)

        # 创建inverted_Geo
        inverted_Geo = cvshapeinverter.invert(baseGeo, sculptGeo)
        cmds.rename(inverted_Geo,'{}_inverted'.format(sculptGeo))
        inverted_neg_Geo = cmds.duplicate(inverted_Geo,name = '{}_neg'.format(inverted_Geo))

        # 将sculptGeo，inverted_Geo，inverted_neg_Geo放在tempSculptGrp组内
        cmds.parent(sculptGeo,inverted_Geo,inverted_neg_Geo,tempSculptGrp)


    def create_targetGeo(self,baseGeo,pose,targetOri_Geo,mirror):
        '''
        检查场景中是否在target_Geo 和 R_target_Geo，没有就创建，并放置于bsTarget_Grp中
        :param baseGeo:
        :param pose:
        :param targetOri_Geo:
        :param mirror:
        :return:
        '''
        target_Geo = '{}_{}'.format(baseGeo, pose)
        R_target_Geo = '{}_{}'.format(baseGeo, pose.replace('L_', 'R_'))
        bsTarget_Grp = '{}_bsTarget_Grp'.format(baseGeo)
        targetGeoList = []

        # 检查场景中是否有 bsTarget_Grp ，没有就报错并返回
        if not cmds.objExists(bsTarget_Grp):
            om.MGlobal_displayError('QBJ_Tip : Can not find {} !!!'.format(bsTarget_Grp))
            return None

        # 检查场景中是否存在 target_Geo 和 R_target_Geo,没有就创建
        if not cmds.objExists(target_Geo):
            target_Geo = cmds.duplicate(targetOri_Geo, name='{}_{}'.format(baseGeo, pose))
            targetGeoList.append(target_Geo)

        if not cmds.objExists(R_target_Geo):
            if mirror:
                R_target_Geo = cmds.duplicate(targetOri_Geo, name='{}_{}'.format(baseGeo, pose.replace('L_', 'R_')))
                targetGeoList.append(R_target_Geo)
        # 将 target_Geo和R_target_Geo 放置在bsTarget_Grp中
        cmds.parent(target_Geo, R_target_Geo, bsTarget_Grp)

        return targetGeoList


    def add_newTargetGeo_To_BsNode(self, baseGeo, pose, targetOri_Geo, mirror, bsNode,poseGrp):
        targetGeoList = self.create_targetGeo(baseGeo, pose, targetOri_Geo, mirror)
        index = len(cmds.aliasAttr(bsNode, q=True))
        # 如果存在 新增的修型目标体，就把他添加进 blendShape 中
        if targetGeoList:
            for target in targetGeoList:
                if not self.exist_Target(bsNode, target):
                    cmds.blendShape(bsNode, edit=True, t=(baseGeo, index, target, 1.0))
                    self.connect_poseGrp_to_target(baseGeo,pose,bsNode,poseGrp,target)
                    index += 1


    def connect_poseGrp_to_target(self,baseGeo,pose,bsNode,poseGrp,target):

        # 创建一个animUU 节点
        animCurveUU_node = cmds.createNode('animCurveUU',name ='{}_{}_{}'.format(baseGeo,pose,bsNode))

        # 将 animUU上的 input 和 output 属性分别连接给poseGrp 和 blendShape上的target
        cmds.connectAttr('{}.{}'.format(poseGrp,pose),'{}.input'.format(animCurveUU_node))
        cmds.connectAttr('{}.output'.format(animCurveUU_node),'{}.{}'.format(bsNode,target))

        # 设置 animCurveUU_node上的属性，将
        cmds.setKeyframe(animCurveUU_node, float=0, value=0, itt='Flat', ott='Flat')
        cmds.setKeyframe(animCurveUU_node, float=45, value=0, itt='Flat', ott='Flat')




    def exist_Target(self,bsNode,target):
        allTargets = cmds.aliasAttr(bsNode, q=True)
        targetName = []
        for i in range(0, len(allTargets), 2):
            targetName.append(allTargets[i])
        if target in targetName:
            return True
        else:
            return None


    def set_sculptGeo_color(self,sculptGeo):
        sculptGeo_blinn = '{}_rigSculpt_skin'.format(sculptGeo)
        rigSculpt_skinSG = '{}_SG'.format(sculptGeo_blinn)
        # 如果场景中没有sculptGeo_blinn ,就创建
        if not cmds.objExists(sculptGeo_blinn):
            sculptGeo_blinn = cmds.shadingNode('blinn', asShader=True,name='rigSculpt_skin')
            pm.mel.assignCreatedShader("blinn" ,'',sculptGeo_blinn,sculptGeo)
            # 设置 sculptGeo_blinn 参数
            color = [0.168, 0.434, 0.679]
            ambientColor = [0.1, 0.1, 0.1]
            eccentricity = [0.5]
            cmds.setAttr('{}.color'.format(sculptGeo_blinn), color[0], color[1], color[2], type='double3')
            cmds.setAttr('{}.ambientColor'.format(sculptGeo_blinn), ambientColor[0], ambientColor[1], ambientColor[2],
                         type='double3')
            cmds.setAttr('{}.eccentricity'.format(sculptGeo_blinn), eccentricity[0])
        else:
            cmds.sets(sculptGeo,forceElement=rigSculpt_skinSG,edit=True)


    # def check_exists_bsTargetInfo(self,baseGeo,pose):
    #     if baseGeo:
    #      bsTargetGrp = '{}_bsTarget_Grp'.format(baseGeo)
    #      if bsTargetGrp:
    #          if not pose.startswith('-'):
    #             bsTargetInfo = cmds.getAttr('{}.{}'.format(bsTargetGrp, pose))
    #             if bsTargetInfo:
    #                 bsTargetList = bsTargetInfo.split(';')
    #                 return bsTargetList
    #             else:
    #                 return None


    def set_bsTargetInfo(self,baseGeo,pose,target):
        bsTargetGrp = '{}_bsTarget_Grp'.format(baseGeo)
        if cmds.objExists(bsTargetGrp):
            attrStr = cmds.getAttr('{}.{}'.format(bsTargetGrp,pose))
            attrList = [s for s in attrStr.split(';') if s != '']
            if target not in attrList:
                newAttrStr = ';'.join(attrList) + ';' + target + ';'
                cmds.setAttr('{}.{}'.format(bsTargetGrp,pose),newAttrStr,type='string')


    def del_tempSculptGrp(self,pose):
        tempSculptGrp = '{}_tempSculptGrp'.format(pose)
        if tempSculptGrp:
            cmds.delete(tempSculptGrp)


    def bsTarget_input_dialog(self):
        WINDOW_NAME = 'AddTargetWin'
        if cmds.window(WINDOW_NAME, exists=True):
            cmds.deleteUI(WINDOW_NAME)

        main_Win = cmds.window(WINDOW_NAME,title='Add target')
        main_layout =cmds.columnLayout(adjustableColumn=True)


        cmds.showWindow(main_Win)