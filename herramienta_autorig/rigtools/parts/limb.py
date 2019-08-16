"""
This module stores our Limb class.
"""


import maya.cmds as cmds
import rigtools.parts.part as rigPart
import rigtools.libs.ikfk as rigIkFk
import rigtools.libs.name as rigName
import rigtools.libs.joint as rigJoint
import rigtools.libs.attribute as rigAttribute
import rigtools.libs.control as rigControl
import rigtools.libs.transform as rigTransform
reload(rigAttribute)
reload(rigName)
reload(rigIkFk)
reload(rigJoint)
reload(rigPart)

class Limb(rigPart.Part):
    def __init__(self,name):
        """
        Constructor method
        """
        super(Limb,self).__init__(name)
        self._startJoint = rigJoint.Joint("{0}_start_{1}".format(name,rigName.BIND),
                            position=(1,25,0),
                            parent=self._bindGroup)
        self._middleJoint = rigJoint.Joint("{0}_middle_{1}".format(name,rigName.BIND),
                            position=(6,25,-2),
                            parent=self._startJoint)
        self._endJoint = rigJoint.Joint("{0}_end_{1}".format(name,rigName.BIND),
                            position=(11,25,0),
                            parent=self._middleJoint)

    def setup(self):
        """
        """
        super(Limb,self).setup()
        # creating joints for the limb
        if not self._startJoint.exists():
            self._endJoint.create()
        else:
            self._startJoint.create()

        # Creating the guides.
        self._masterGuide.setPosition(self._startJoint.getPosition())
        startGuide = self._createGuide(self._startJoint,rigName.SIDECOLOR[rigName.getSide(self._name)])
        middleGuide = self._createGuide(self._middleJoint,rigName.SIDECOLOR[rigName.getSide(self._name)])
        endGuide = self._createGuide(self._endJoint,rigName.SIDECOLOR[rigName.getSide(self._name)])

        # create our aim and up vectors
        aimAxisNode = rigAttribute.switch(self._masterGuide.getPartialPath(),"aimAxis",["X","Y","Z","-X","-Y","-Z"],[[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]],defaultValue=0)
        upAxisNode = rigAttribute.switch(self._masterGuide.getPartialPath(),"upAxis",["X","Y","Z","-X","-Y","-Z"],[[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]],defaultValue=1)


        # Create our world up vector setup
        startGuideDCM = cmds.createNode("decomposeMatrix",n="{0}_{1}".format(startGuide.getPartialPath(),rigName.DECOMPOSEMATRIX))
        middleGuideDCM = cmds.createNode("decomposeMatrix",n="{0}_{1}".format(middleGuide.getPartialPath(),rigName.DECOMPOSEMATRIX))
        endGuideDCM = cmds.createNode("decomposeMatrix",n="{0}_{1}".format(endGuide.getPartialPath(),rigName.DECOMPOSEMATRIX))

        # make the connections to the from the guides to the matrix nodes.
        cmds.connectAttr("{0}.worldMatrix[0]".format(startGuide.getPartialPath()),"{0}.inputMatrix".format(startGuideDCM),f=True)
        cmds.connectAttr("{0}.worldMatrix[0]".format(middleGuide.getPartialPath()),"{0}.inputMatrix".format(middleGuideDCM),f=True)
        cmds.connectAttr("{0}.worldMatrix[0]".format(endGuide.getPartialPath()),"{0}.inputMatrix".format(endGuideDCM),f=True)

        #create plusMinusAverage nodes.
        pma1 = cmds.createNode("plusMinusAverage",n="{0}_001_pma".format(self._name))
        pma2 = cmds.createNode("plusMinusAverage",n="{0}_002_pma".format(self._name))
        cmds.setAttr("{0}.operation".format(pma1),2)
        cmds.setAttr("{0}.operation".format(pma2),2)

        # connect decomposeMatrix nodes to the plusMinusAverage nodes
        cmds.connectAttr("{0}.outputTranslate".format(startGuideDCM),"{0}.input3D[0]".format(pma1),f=True)
        cmds.connectAttr("{0}.outputTranslate".format(endGuideDCM),"{0}.input3D[1]".format(pma1),f=True)

        cmds.connectAttr("{0}.outputTranslate".format(startGuideDCM),"{0}.input3D[0]".format(pma2),f=True)
        cmds.connectAttr("{0}.outputTranslate".format(middleGuideDCM),"{0}.input3D[1]".format(pma2),f=True)

        # create and connect vector product node.
        vpn = cmds.createNode("vectorProduct",n="{0}_{1}".format(self._name,rigName.VECTORPRODUCT))
        cmds.setAttr("{0}.operation".format(vpn),2)
        cmds.setAttr("{0}.normalizeOutput".format(vpn),1)
        cmds.connectAttr("{0}.output3D".format(pma1),"{0}.input1".format(vpn),f=True)
        cmds.connectAttr("{0}.output3D".format(pma2),"{0}.input2".format(vpn),f=True)

        # create constraints
        cst = cmds.aimConstraint(middleGuide.getPartialPath(),self._startJoint.getPartialPath(),wut="vector",aim=(1,0,0),u=(0,1,0),wu=(0,0,-1))[0]
        cmds.parent(cst,self._guideGroup.getPartialPath())
        #connecting choice nodes to vector attributes
        cmds.connectAttr("{0}.output".format(aimAxisNode),"{0}.aimVector".format(cst),f=True)
        cmds.connectAttr("{0}.output".format(upAxisNode),"{0}.upVector".format(cst),f=True)
        cmds.connectAttr("{0}.output".format(vpn),"{0}.worldUpVector".format(cst),f=True)

        cst = cmds.aimConstraint(endGuide.getPartialPath(),self._middleJoint.getPartialPath(),wut="vector",aim=(1,0,0),u=(0,1,0),wu=(0,0,-1))[0]
        cmds.parent(cst,self._guideGroup.getPartialPath())
        #connecting choice nodes to vector attributes
        cmds.connectAttr("{0}.output".format(aimAxisNode),"{0}.aimVector".format(cst),f=True)
        cmds.connectAttr("{0}.output".format(upAxisNode),"{0}.upVector".format(cst),f=True)
        cmds.connectAttr("{0}.output".format(vpn),"{0}.worldUpVector".format(cst),f=True)

        cst = cmds.orientConstraint(self._middleJoint.getPartialPath(),self._endJoint.getPartialPath())[0]
        cmds.parent(cst,self._guideGroup.getPartialPath())

    def build(self):
        """
        """
        super(Limb,self).build()

        self._ikfkSystem = rigIkFk.IkFkLimb((self._startJoint.getPartialPath(),self._middleJoint.getPartialPath(),self._endJoint.getPartialPath()))
        self._ikfkSystem.create()
        self._ikfkSystem.setGroup(cmds.rename(self._ikfkSystem.getGroup(),"{0}_{1}".format(self._name,self._ikfkSystem.getGroup())))
        cmds.parent(self._ikfkSystem.getGroup(),self._rigGroup.getPartialPath())
        cmds.setAttr("{0}.v".format(self._ikfkSystem.getGroup()),0)

        ikJointList = self._ikfkSystem.getIkJoints()
        fkJointList = self._ikfkSystem.getFkJoints()
        #-------------------------------------------------
        #FK SYSTEM
        #-------------------------------------------------
        fkControls = list()
        parent = self._rigGroup
        for jnt in (fkJointList):
            # create new control.
            ctrl = rigControl.Control(name=jnt.replace("{0}_{1}".format(rigName.BIND,rigName.FK),rigName.CONTROL),
                                        position=cmds.xform(jnt,q=True,ws=True,t=True),
                                        parent=parent,
                                        shape="circle",
                                        color=rigName.SIDECOLOR[rigName.getSide(self._name)])
            ctrl.create()
            ctrl.setMatrix(cmds.xform(jnt,q=True,ws=True,m=True))

            # constrain the joints to the controls
            cmds.pointConstraint(ctrl.getPartialPath(),jnt)
            cmds.orientConstraint(ctrl.getPartialPath(),jnt)

            # name the ctrl as the new parent and append to control list
            parent = ctrl
            fkControls.append(ctrl)

        #-------------------------------------------------
        # IK SYSTEM
        #-------------------------------------------------
        # create ik controls.
        ikCtrl = rigControl.Control("{0}_{1}".format(self._name,rigName.CONTROL),
                                    position=self._endJoint.getPosition(),
                                    parent=self._rigGroup.getPartialPath(),
                                    shape="circle",
                                    color=rigName.SIDECOLOR[rigName.getSide(self._name)])
        ikCtrl.create()
        offsetJnt = rigJoint.Joint("{0}_offset".format(ikJointList[-1].replace("_{0}_".format(rigName.BIND),"")),parent=ikCtrl)
        offsetJnt.create()
        offsetJnt.setMatrix(cmds.xform(ikJointList[-1],q=True,ws=True,m=True))
        rigJoint.Joint.rotateToOrient([offsetJnt.getPartialPath()])
        cmds.parent(self._ikfkSystem.getHandle(),offsetJnt.getPartialPath())
        cmds.setAttr("{0}.v".format(offsetJnt.getPartialPath()),0)
        # renaming handle and setting the name back system
        self._ikfkSystem.setHandle(cmds.rename(self._ikfkSystem.getHandle(),"{0}_{1}".format(self._name,rigName.HANDLE)))
        # turn off the visibility of my ik handle
        cmds.setAttr("{0}.v".format(self._ikfkSystem.getHandle()),0)
        
        # orient constrain the last ik joint in the chain to my offset joint
        cmds.orientConstraint(offsetJnt.getPartialPath(),ikJointList[-1])

        # parent the ik handle
        pvPos = self._ikfkSystem.getPolevectorPosition((self._startJoint.getPartialPath(),self._middleJoint.getPartialPath(),self._endJoint.getPartialPath()))
        pvCtrl = rigControl.Control("{0}_pv_{1}".format(self._name,rigName.CONTROL),
                                    position=pvPos,
                                    parent=self._rigGroup.getPartialPath(),
                                    shape="circle",
                                    color=rigName.SIDECOLOR[rigName.getSide(self._name)])
        pvCtrl.create()
        cmds.poleVectorConstraint(pvCtrl.getPartialPath(),self._ikfkSystem.getHandle())

        for origJnt,blendJnt in zip(self._ikfkSystem.getOriginalJoints(),self._ikfkSystem.getBlendJoints()):
            cmds.parentConstraint(blendJnt,origJnt)

        #-------------------------------------------------
        # Param for IK/FK switching.
        #-------------------------------------------------
        # Create parameter node to drive ik/fk switching.

        paramLocator = cmds.spaceLocator()[0]
        paramNode = cmds.listRelatives(paramLocator,c=True,shapes=True)[0]
        paramNode = cmds.rename(paramNode,"{0}_param".format(self._name))

        # parent 
        cmds.parent(paramNode,pvCtrl.getPartialPath(),r=True,s=True)
        cmds.delete(paramLocator)
        del(paramLocator)
        cmds.setAttr("{0}.v".format(paramNode),0)

        # lock and hide attributes
        rigAttribute.lockAndHide(paramNode,["lpx","lpy","lpz","lsx","lsy","lsz"])

        # add ik/fk attribute to the param node
        cmds.addAttr(paramNode,ln="ikfk",at="double",min=0,max=1,dv=0,keyable=True)
        paramAttrIKFK = "{0}.ikfk".format(paramNode)

        # Loop through and create instance of paramNode on all of the controls.
        for ctrl in fkControls + [ikCtrl]:
            cmds.parent(paramNode,ctrl.getPartialPath(),r=True,s=True,add=True)

        # connect ikfk paramNode attr to the ikfk system attribute
        cmds.connectAttr(paramAttrIKFK,"{0}.ikfk".format(self._ikfkSystem.getGroup()),f=True)

        # hide controls when they shouldn't visible during ikfk switching.
        
        # create a reverse node 
        reverseNode = cmds.createNode("reverse",n="{0}_{1}".format(self._name,rigName.REVERSE))
        cmds.connectAttr("{0}.ikfk".format(self._ikfkSystem.getGroup()),"{0}.inputX".format(reverseNode),f=True)

        # param node ikfk attribute to the fk control visibility 
        for ctrl in fkControls:
            cmds.connectAttr(paramAttrIKFK,"{0}.v".format(ctrl.getShape()),f=True)

        # connect reverse node to the ik controls
        for ctrl in (ikCtrl,pvCtrl):
            cmds.connectAttr("{0}.outputX".format(reverseNode),"{0}.v".format(ctrl.getShape()),f=True)

        self._fkControls = fkControls

    def postBuild(self):
        """
        """
        del(self._fkControls)