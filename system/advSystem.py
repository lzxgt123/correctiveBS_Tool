# -*- coding: utf-8 -*-
# .@FileName:advSystem
# .@Date....:2022-04-06   23：04
# .@Aurhor..:QianBinJie
# .@Contact.:1075064966@qq.com
'''
launch :
        import advSystem as QBJ_FileName
        reload(FileName)
        FileName.main()
'''

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import collections

# arm_ADV_poseDict = {
    #     'FKScapula_L': [u'-----肩胛-----', 'Scapula_L_Up', 'Scapula_L_Down', 'Scapula_L_Front', 'Scapula_L_Back'],
    #     'FKShoulder_L': [u'-----上臂-----', 'Shoulder_L_Up', 'Shoulder_L_Down', 'Shoulder_L_Front', 'Shoulder_L_Back',
    #                      'Shoulder_L_UpFront', 'Shoulder_L_UpBack', 'Shoulder_L_DownFront', 'Shoulder_L_DownBack'],
    #     'FKElbow_L': [u'-----肘部-----', 'Elbow_L_Front'],
    #     'FKWrist_L': [u'-----手腕-----', 'Wrist_L_Up', 'Wrist_L_Down', 'Wrist_L_Front', 'Wrist_L_Back', 'Wrist_L_UpFront',
    #                   'Wrist_L_UpBack', 'Wrist_L_DownFront', 'Wrist_L_DownBack']
    # }
    # leg_ADV_poseDict = {
    #     'FKHip_L': [u'-----腿部-----', 'Hip_L_Up', 'Hip_L_Down', 'Hip_L_Front', 'Hip_L_Back',
    #                 'Hip_L_UpFront', 'Hip_L_UpBack', 'Hip_L_DownFront', 'Hip_L_DownBack'],
    #     'FKKnee_L': [u'-----膝盖-----', 'Knee_L_Back'],
    #     'FKHip_L': [u'-----脚踝-----', 'Ankle_L_Up', 'Ankle_L_Down', 'Ankle_L_Front', 'Ankle_L_Back', 'Ankle_L_UpFront',
    #                   'Ankle_L_UpBack', 'Ankle_L_DownFront', 'Ankle_L_DownBack']
    # }
# finger_ADV_poseDict = {
    #     'FKIndexFinger1_L': [u'-----食指-----', 'IndexFinger1_L_Down', 'IndexFinger1_L_Up'],
    #     'FKIndexFinger2_L': ['IndexFinger2_L_Down', 'IndexFinger2_L_Up'],
    #     'FKIndexFinger3_L': ['IndexFinger3_L_Down', 'IndexFinger3_L_Up'],
    #     'FKMiddleFinger1_L': [u'-----中指-----', 'MiddleFinger1_L_Down', 'MiddleFinger1_L_Up'],
    #     'FKMiddleFinger2_L': ['MiddleFinger2_L_Down', 'MiddleFinger2_L_Up'],
    #     'FKMiddleFinger3_L': ['MiddleFinger3_L_Down', 'MiddleFinger3_L_Up'],
    #     'FKRingFinger1_L': [u'-----无名指-----', 'RingFinger1_L_Down', 'RingFinger1_L_Up'],
    #     'FKRingFinger2_L': ['RingFinger2_L_Down', 'RingFinger2_L_Up'],
    #     'FKRingFinger3_L': ['RingFinger3_L_Down', 'RingFinger3_L_Up'],
    #     'FKPinkyFinger1_L': [u'-----小拇指-----', 'PinkyFinger1_L_Down', 'PinkyFinger1_L_Up'],
    #     'FKPinkyFinger2_L': ['PinkyFinger2_L_Down', 'PinkyFinger2_L_Up'],
    #     'FKPinkyFinger3_L': ['PinkyFinger3_L_Down', 'PinkyFinger3_L_Up'],
    #     'FKThumbFinger1_L': [u'-----大拇指-----', 'ThumbFinger1_L_Down', 'ThumbFinger1_L_Up'],
    #     'FKThumbFinger2_L': ['ThumbFinger2_L_Down', 'ThumbFinger2_L_Up'],
    #     'FKThumbFinger3_L': ['ThumbFinger3_L_Down', 'ThumbFinger3_L_Up']
    # }

# torso_ADV_poseDict = {
    #     'FKHead_M': [u'-----头部-----', 'Head_Front', 'Head_Back', 'Head_Left', 'Head_Right'],
    #     'FKNeck_M': [u'-----颈部-----', 'Neck_Front', 'Neck_Back', 'Neck_Left', 'Neck_Right'],
    #     'FKChest_M': [u'-----胸腔-----', 'Chest_Front', 'Chest_Back', 'Chest_Left', 'Chest_Right'],
    #     'FKSpine1_M': [u'-----躯干-----', 'Spine1_Front', 'Spine1_Back', 'Spine1_Left', 'Spine1_Right'],
    #     'FKSpine2_M': ['Spine2_Front', 'Spine2_Back', 'Spine2_Left', 'Spine2_Right']
    # }

class advSystem(object):

    armPoseDefaultDict = []
    arm_ADV_poseDict = collections.OrderedDict(armPoseDefaultDict)
    arm_ADV_poseDict['FKScapula_L'] = [u'-----肩胛-----', 'Scapula_L_Up', 'Scapula_L_Down', 'Scapula_L_Front',
                                       'Scapula_L_Back']
    arm_ADV_poseDict['FKShoulder_L'] =  [u'-----上臂-----', 'Shoulder_L_Up', 'Shoulder_L_Down', 'Shoulder_L_Front',
                                         'Shoulder_L_Back', 'Shoulder_L_UpFront', 'Shoulder_L_UpBack',
                                         'Shoulder_L_DownFront', 'Shoulder_L_DownBack']
    arm_ADV_poseDict['FKElbow_L'] = [u'-----肘部-----', 'Elbow_L_Front']
    arm_ADV_poseDict['FKWrist_L'] = [u'-----手腕-----', 'Wrist_L_Up', 'Wrist_L_Down', 'Wrist_L_Front', 'Wrist_L_Back',
                                     'Wrist_L_UpFront','Wrist_L_UpBack', 'Wrist_L_DownFront', 'Wrist_L_DownBack']

    legPoseDefaultDict = []
    leg_ADV_poseDict = collections.OrderedDict(legPoseDefaultDict)
    leg_ADV_poseDict['FKHip_L'] = [u'-----腿部-----', 'Hip_L_Up', 'Hip_L_Down', 'Hip_L_Front', 'Hip_L_Back',
                                    'Hip_L_UpFront', 'Hip_L_UpBack', 'Hip_L_DownFront', 'Hip_L_DownBack']
    leg_ADV_poseDict['FKKnee_L'] = [u'-----膝盖-----', 'Knee_L_Back']
    leg_ADV_poseDict['FKAnkle_L'] = [u'-----脚踝-----', 'Ankle_L_Up', 'Ankle_L_Down', 'Ankle_L_Front', 'Ankle_L_Back',
                                   'Ankle_L_UpFront','Ankle_L_UpBack', 'Ankle_L_DownFront', 'Ankle_L_DownBack']

    fingerPoseDefaultDict = []
    finger_ADV_poseDict = collections.OrderedDict(fingerPoseDefaultDict)
    finger_ADV_poseDict['FKIndexFinger1_L'] = [u'-----食指-----', 'IndexFinger1_L_Down', 'IndexFinger1_L_Up']
    finger_ADV_poseDict['FKIndexFinger2_L'] = ['IndexFinger2_L_Down', 'IndexFinger2_L_Up']
    finger_ADV_poseDict['FKIndexFinger3_L'] = ['IndexFinger3_L_Down', 'IndexFinger3_L_Up']
    finger_ADV_poseDict['FKMiddleFinger1_L'] = [u'-----中指-----', 'MiddleFinger1_L_Down', 'MiddleFinger1_L_Up']
    finger_ADV_poseDict['FKMiddleFinger2_L'] = ['MiddleFinger2_L_Down', 'MiddleFinger2_L_Up']
    finger_ADV_poseDict['FKMiddleFinger3_L'] = ['MiddleFinger3_L_Down', 'MiddleFinger3_L_Up']
    finger_ADV_poseDict['FKRingFinger1_L'] = [u'-----无名指-----', 'RingFinger1_L_Down', 'RingFinger1_L_Up']
    finger_ADV_poseDict['FKRingFinger2_L'] = ['RingFinger2_L_Down', 'RingFinger2_L_Up']
    finger_ADV_poseDict['FKRingFinger3_L'] = ['RingFinger3_L_Down', 'RingFinger3_L_Up']
    finger_ADV_poseDict['FKPinkyFinger1_L'] = [u'-----小拇指-----', 'PinkyFinger1_L_Down', 'PinkyFinger1_L_Up']
    finger_ADV_poseDict['FKPinkyFinger2_L'] = ['PinkyFinger2_L_Down', 'PinkyFinger2_L_Up']
    finger_ADV_poseDict['FKPinkyFinger3_L'] = ['PinkyFinger3_L_Down', 'PinkyFinger3_L_Up']
    finger_ADV_poseDict['FKThumbFinger1_L'] = [u'-----大拇指-----', 'ThumbFinger1_L_Down', 'ThumbFinger1_L_Up']
    finger_ADV_poseDict['FKThumbFinger2_L'] = ['ThumbFinger2_L_Down', 'ThumbFinger2_L_Up']
    finger_ADV_poseDict['FKThumbFinger3_L'] = ['ThumbFinger3_L_Down', 'ThumbFinger3_L_Up']

    torsoPoseDefaultDict = []
    torso_ADV_poseDict = collections.OrderedDict(torsoPoseDefaultDict)
    torso_ADV_poseDict['FKHead_M'] = [u'-----头部-----', 'Head_Front', 'Head_Back', 'Head_Left', 'Head_Right']
    torso_ADV_poseDict['FKNeck_M'] = [u'-----颈部-----', 'Neck_Front', 'Neck_Back', 'Neck_Left', 'Neck_Right']
    torso_ADV_poseDict['FKChest_M'] = [u'-----胸腔-----', 'Chest_Front', 'Chest_Back', 'Chest_Left', 'Chest_Right']
    torso_ADV_poseDict['FKSpine1_M'] = [u'-----躯干-----', 'Spine1_Front', 'Spine1_Back', 'Spine1_Left', 'Spine1_Right']
    torso_ADV_poseDict['FKSpine2_M'] = ['Spine2_Front', 'Spine2_Back', 'Spine2_Left', 'Spine2_Right']


    def __init__(self):
        pass

    def create_armPoseBrige(self):

        for ctrl in self.arm_ADV_poseDict.keys():
            joint = ctrl.strip('FK')
            if cmds.objExists(ctrl):
                pass
        print 'armPose>>>>>>>'


    def create_armTargets(self,baseGeo,targetGeo,blendShapeNode):
        self.create_Targets(baseGeo,targetGeo,blendShapeNode,self.arm_ADV_poseDict)


    def create_legPoseBrige(self):
        print 'legPose>>>>>>>'


    def create_legTargets(self,baseGeo,targetGeo,blendShapeNode):
        self.create_Targets(baseGeo,targetGeo,blendShapeNode,self.leg_ADV_poseDict)


    def create_fingerPoseBrige(self):
        print 'fingerPose>>>>>>>'


    def create_fingerTargets(self,baseGeo,targetGeo,blendShapeNode):
        self.create_Targets(baseGeo,targetGeo,blendShapeNode,self.finger_ADV_poseDict)


    def create_torsoPoseBrige(self):
        print 'fingerPose>>>>>>>'


    def create_torsoTargets(self,baseGeo,targetGeo,blendShapeNode):
        self.create_Targets(baseGeo,targetGeo,blendShapeNode,self.torso_ADV_poseDict)


    def create_Targets(self,baseGeo,targetGeo,blendShapeNode,poseDict):

        bs_target_list = []
        for ctrl, poseGrp in poseDict.items():
            if cmds.objExists(ctrl):
                for pose in poseGrp:
                    if not pose.startswith('-'):
                        bs_target = cmds.duplicate(targetGeo, name='{}_{}'.format(baseGeo, pose))
                        bs_target_list.append(bs_target[0])

        for i in range(len(bs_target_list),):

            if cmds.blendShape(blendShapeNode, q=True, target=True):
                currrectTargetNumber = len(cmds.blendShape(blendShapeNode, q=True, target=True))
            else:
                currrectTargetNumber = 0

            cmds.blendShape(blendShapeNode, edit=True, t =( str(baseGeo) , currrectTargetNumber, str(bs_target_list[i]),1))
