import maya.cmds as mc
import maya.mel as mel

def fkik():
    sides     = ['l','r']
    switch_loc = mc.spaceLocator(name='ikfk_switch')
    mc.addAttr(switch_loc,ln='fkik',at='long',min=0,max=1,k=True)
    for side in sides:
        part      =['arm','elbow','wrist']
        sel       =[side+'_'+part[0]+'_JNT',side+'_'+part[1]+'_JNT',side+'_'+part[2]+'_JNT']
        pV_vector =[0,0,-5]
        mylistFK  = mc.duplicate(sel,n=side+'_'+part[0]+'FK_JNT')
        mylistIK  = mc.duplicate(sel,n=side+'_'+part[0]+'IK_JNT')
                        
        for sides in side:                   
            fk_reElbow = mc.rename(sides+'_'+part[0]+'FK_JNT1',sides+'_'+part[1]+'FK_JNT')
            fk_reWrist = mc.rename(sides+'_'+part[0]+'FK_JNT2',sides+'_'+part[2]+'FK_JNT')
            ik_reElbow = mc.rename(sides+'_'+part[0]+'IK_JNT1',sides+'_'+part[1]+'IK_JNT')
            ik_reWrist = mc.rename(sides+'_'+part[0]+'IK_JNT2',sides+'_'+part[2]+'IK_JNT')
                    
   
            for parts in part:
                fkSwitchCons  = mc.parentConstraint(sides+'_'+parts+'FK_JNT',sides+'_'+parts+'_JNT',mo=True)
                ikSwitchCons  = mc.parentConstraint(sides+'_'+parts+'IK_JNT',sides+'_'+parts+'_JNT',mo=True)
                fk_ctrl       = mc.CreateNURBSCircle()
                fk_rename     = mc.rename(sides+'_'+parts+'FK_CTRL')  
                fk_modify_grp = mc.group(n=sides+'_'+parts+'ModifyFK_GRP')   
                fk_grp        = mc.group(n=sides+'_'+parts+'OffsetFK_GRP')
                fk_matchTrans = mc.matchTransform(sides+'_'+parts+'OffsetFK_GRP',sides+'_'+parts+'FK_JNT')
                fk_parentCon  = mc.parentConstraint(sides+'_'+parts+'FK_CTRL',sides+'_'+parts+'FK_JNT',mo=True)
                mc.setDrivenKeyframe(sides+'_'+parts+'_JNT_parentConstraint1', currentDriver='ikfk_switch.fkik', driverValue=0, attribute= sides+'_'+parts+'FK_JNTW0', value=1)
                mc.setDrivenKeyframe(sides+'_'+parts+'_JNT_parentConstraint1', currentDriver='ikfk_switch.fkik', driverValue=1, attribute= sides+'_'+parts+'FK_JNTW0', value=0)
                mc.setDrivenKeyframe(sides+'_'+parts+'_JNT_parentConstraint1', currentDriver='ikfk_switch.fkik', driverValue=0, attribute= sides+'_'+parts+'IK_JNTW1', value=0)
                mc.setDrivenKeyframe(sides+'_'+parts+'_JNT_parentConstraint1', currentDriver='ikfk_switch.fkik', driverValue=1, attribute= sides+'_'+parts+'IK_JNTW1', value=1)
    
            
            fkSwitchCons = mc.parentConstraint(sides+'_'+parts+'FK_JNT',sides+'_'+parts+'_JNT',mo=True)
            ikSwitchCons = mc.parentConstraint(sides+'_'+parts+'IK_JNT',sides+'_'+parts+'_JNT',mo=True)
    
            mc.parent(side+'_'+part[2]+'OffsetFK_GRP',side+'_'+part[1]+'FK_CTRL')
            mc.parent(side+'_'+part[1]+'OffsetFK_GRP',side+'_'+part[0]+'FK_CTRL')
            
            ik_sel        = mc.select(sides+'_'+part[0]+'IK_JNT',sides+'_'+part[2]+'IK_JNT')
            ik_handle     = mc.ikHandle(ik_sel,name=sides+'_'+part[0]+'IK_handle')     
            ik_ctrl       = mc.CreateNURBSCircle()
            ik_rename     = mc.rename(sides+'_'+part[0]+'IK_CTRL')     
            ik_Modify_grp = mc.group(n=sides+'_'+part[0]+'IKModify_GRP')
            ik_grp        = mc.group(n=sides+'_'+part[0]+'OffsetIK_GRP')
            ik_matchTrans = mc.matchTransform(sides+'_'+part[0]+'OffsetIK_GRP',sides+'_'+part[0]+'IK_handle')
            ik_parentCon  = mc.pointConstraint(sides+'_'+part[0]+'IK_CTRL',sides+'_'+part[0]+'IK_handle',mo=True)
            
            pV_loc = mc.spaceLocator(name=sides+'_'+part[0]+'PV_LOC')
            pV_modify_grp = mc.group(n=sides+'_'+part[0]+'PVModify_GRP')
            pV_grp = mc.group(n=sides+'_'+part[0]+'OffsetPV_GRP')
            pV_matchTrans  = mc.matchTransform(sides+'_'+part[0]+'OffsetPV_GRP',sides+'_'+part[1]+'IK_JNT')
            if side == 'l':
                pV_vectorX = pV_vector[0]
                pV_vectorY = pV_vector[1]
                pV_vectorZ = pV_vector[2]
                pV_positionX = mc.setAttr(sides+'_'+part[0]+'PVModify_GRP.translateX',pV_vectorX)
                pV_positionY = mc.setAttr(sides+'_'+part[0]+'PVModify_GRP.translateY',pV_vectorY)
                pV_positionZ = mc.setAttr(sides+'_'+part[0]+'PVModify_GRP.translateZ',pV_vectorZ)
            if side == 'r':
                pV_vectorX = pV_vector[0]*-1
                pV_vectorY = pV_vector[1]*-1
                pV_vectorZ = pV_vector[2]*-1
                pV_positionX = mc.setAttr(sides+'_'+part[0]+'PVModify_GRP.translateX',pV_vectorX)
                pV_positionY = mc.setAttr(sides+'_'+part[0]+'PVModify_GRP.translateY',pV_vectorY)
                pV_positionZ = mc.setAttr(sides+'_'+part[0]+'PVModify_GRP.translateZ',pV_vectorZ)
            pV_Constraint  = mc.poleVectorConstraint(pV_loc,sides+'_'+part[0]+'IK_handle')
    
            mc.setDrivenKeyframe(sides+'_'+part[0]+'OffsetFK_GRP', currentDriver='ikfk_switch.fkik', driverValue=0, attribute= 'visibility', value=1)
            mc.setDrivenKeyframe(sides+'_'+part[0]+'OffsetFK_GRP', currentDriver='ikfk_switch.fkik', driverValue=1, attribute= 'visibility', value=0)            
            mc.setDrivenKeyframe(sides+'_'+part[0]+'OffsetIK_GRP', currentDriver='ikfk_switch.fkik', driverValue=0, attribute= 'visibility', value=0)
            mc.setDrivenKeyframe(sides+'_'+part[0]+'OffsetIK_GRP', currentDriver='ikfk_switch.fkik', driverValue=1, attribute= 'visibility', value=1)
            
            mc.setDrivenKeyframe(sides+'_'+part[0]+'OffsetPV_GRP', currentDriver='ikfk_switch.fkik', driverValue=0, attribute= 'visibility', value=1)
            mc.setDrivenKeyframe(sides+'_'+part[0]+'OffsetPV_GRP', currentDriver='ikfk_switch.fkik', driverValue=1, attribute= 'visibility', value=0)            
            mc.setDrivenKeyframe(sides+'_'+part[0]+'OffsetPV_GRP', currentDriver='ikfk_switch.fkik', driverValue=0, attribute= 'visibility', value=0)
            mc.setDrivenKeyframe(sides+'_'+part[0]+'OffsetPV_GRP', currentDriver='ikfk_switch.fkik', driverValue=1, attribute= 'visibility', value=1)
            