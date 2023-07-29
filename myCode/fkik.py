import maya.cmds as mc
import maya.mel as mel


def fkik(sel):
    side     = 'l'
    sel      =['l_arm_JNT','l_elbow_JNT','l_wrist_JNT']
    mylistFK = mc.duplicate(sel,n=side+'_armFK_JNT')
    mylistIK = mc.duplicate(sel,n=side+'_armIK_JNT')
    
    switch_loc = mc.spaceLocator(name='ikfk_switch')
    mc.addAttr(switch_loc,ln='fkik',at='long',min=0,max=1,k=True)    
        
    for sides in side:                   
        fk_reElbow = mc.rename(sides+'_armFK_JNT1',sides+'_elbowFK_JNT')
        fk_reWrist = mc.rename(sides+'_armFK_JNT2',sides+'_wristFK_JNT')
        ik_reElbow = mc.rename(sides+'_armIK_JNT1',sides+'_elbowIK_JNT')
        ik_reWrist = mc.rename(sides+'_armIK_JNT2',sides+'_wristIK_JNT')
                
        part = ['arm','elbow','wrist']    
        for parts in part:
            fkSwitchCons  = mc.parentConstraint(sides+'_'+parts+'FK_JNT',sides+'_'+parts+'_JNT',mo=True)
            ikSwitchCons  = mc.parentConstraint(sides+'_'+parts+'IK_JNT',sides+'_'+parts+'_JNT',mo=True)
            fk_ctrl       = mc.CreateNURBSCircle()
            fk_rename     = mc.rename(sides+'_'+parts+'FK_CTRL')     
            fk_grp        = mc.group(n=sides+'_'+parts+'FK_GRP')
            fk_matchTrans = mc.matchTransform(sides+'_'+parts+'FK_GRP',sides+'_'+parts+'FK_JNT')
            fk_parentCon  = mc.parentConstraint(sides+'_'+parts+'FK_CTRL',sides+'_'+parts+'FK_JNT',mo=True)
            mc.setDrivenKeyframe(sides+'_'+parts+'_JNT_parentConstraint1', currentDriver='ikfk_switch.fkik', driverValue=0, attribute= sides+'_'+parts+'FK_JNTW0', value=1)
            mc.setDrivenKeyframe(sides+'_'+parts+'_JNT_parentConstraint1', currentDriver='ikfk_switch.fkik', driverValue=1, attribute= sides+'_'+parts+'FK_JNTW0', value=0)
            mc.setDrivenKeyframe(sides+'_'+parts+'_JNT_parentConstraint1', currentDriver='ikfk_switch.fkik', driverValue=0, attribute= sides+'_'+parts+'IK_JNTW1', value=0)
            mc.setDrivenKeyframe(sides+'_'+parts+'_JNT_parentConstraint1', currentDriver='ikfk_switch.fkik', driverValue=1, attribute= sides+'_'+parts+'IK_JNTW1', value=1)

        
        fkSwitchCons = mc.parentConstraint(sides+'_'+parts+'FK_JNT',sides+'_'+parts+'_JNT',mo=True)
        ikSwitchCons = mc.parentConstraint(sides+'_'+parts+'IK_JNT',sides+'_'+parts+'_JNT',mo=True)

        mc.parent(side+'_wristFK_GRP',side+'_elbowFK_CTRL')
        mc.parent(side+'_elbowFK_GRP',side+'_armFK_CTRL')
        
        ikPart        = 'arm'   
        ik_sel        = mc.select(sides+'_armIK_JNT',sides+'_wristIK_JNT')
        ik_handle     = mc.ikHandle(ik_sel,name=sides+'_'+ikPart+'IK_handle')     
        ik_ctrl       = mc.CreateNURBSCircle()
        ik_rename     = mc.rename(sides+'_'+ikPart+'IK_CTRL')     
        ik_grp        = mc.group(n=sides+'_'+ikPart+'IK_GRP')
        ik_matchTrans = mc.matchTransform(sides+'_'+ikPart+'IK_GRP',sides+'_'+ikPart+'IK_handle')
        ik_parentCon  = mc.pointConstraint(sides+'_'+ikPart+'IK_CTRL',sides+'_'+ikPart+'IK_handle',mo=True)
        
        mc.setDrivenKeyframe(sides+'_'+ikPart+'FK_GRP', currentDriver='ikfk_switch.fkik', driverValue=0, attribute= 'visibility', value=1)
        mc.setDrivenKeyframe(sides+'_'+ikPart+'FK_GRP', currentDriver='ikfk_switch.fkik', driverValue=1, attribute= 'visibility', value=0)
        
        mc.setDrivenKeyframe(sides+'_'+ikPart+'IK_GRP', currentDriver='ikfk_switch.fkik', driverValue=0, attribute= 'visibility', value=0)
        mc.setDrivenKeyframe(sides+'_'+ikPart+'IK_GRP', currentDriver='ikfk_switch.fkik', driverValue=1, attribute= 'visibility', value=1)
        