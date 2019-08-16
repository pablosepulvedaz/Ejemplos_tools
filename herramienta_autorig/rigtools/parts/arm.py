"""
This module stores our Limb class.
"""


import maya.cmds as cmds
import rigtools.parts.limb as rigLimb
import rigtools.libs.transform as rigTransform
import rigtools.libs.joint as rigJoint
import rigtools.libs.name as rigName
import rigtools.libs.control as rigControl
reload(rigLimb)

class Arm(rigLimb.Limb):
    def __init__(self,name):
        """
        Constructor method
        """
        super(Arm,self).__init__(name)
        self._clavicleJoint = rigJoint.Joint("{0}_clavicle_{1}".format(name,rigName.BIND),
                            position=(1,25,0),
                            parent=self._bindGroup)

        # change the start position of the joints
        self._startJoint.setParent(self._clavicleJoint)
        self._startJoint.setPosition((2,25,0))

        self._middleJoint.setPosition((7,25,-2))

        self._endJoint.setPosition((12,25,0))


    def setup(self):
        """
        """
        super(Arm,self).setup()
        # move master guide to clavicle position
        # gather children of master guide
        masterGuideChildList = cmds.listRelatives(self._masterGuide.getPartialPath(),c=True,type="transform") or list()
        
        # parent the master guide children to the world so we can re-position it.
        if masterGuideChildList:
            cmds.parent(masterGuideChildList,w=True)

        self._masterGuide.setPosition(self._clavicleJoint.getPosition())

        # re-parent children back under the master guide
        if masterGuideChildList:
            cmds.parent(masterGuideChildList,self._masterGuide.getPartialPath())

        clavicleGuide = self._createGuide(self._clavicleJoint,rigName.SIDECOLOR[rigName.getSide(self._name)])

        clavicleAimOrientNode = rigTransform.Transform("{0}_aim".format(self._clavicleJoint.getName()),
                                                        position=self._startJoint.getPosition(),
                                                        parent=clavicleGuide)

        clavicleAimOrientNode.create()

        # make connections to the constraint
        aimAxisNode = cmds.listConnections("{0}.aimAxis".format(self._masterGuide.getPartialPath()))[0]
        upAxisNode = cmds.listConnections("{0}.upAxis".format(self._masterGuide.getPartialPath()))[0]

        cst = cmds.aimConstraint(clavicleAimOrientNode.getPartialPath(),self._clavicleJoint.getPartialPath(),wut="vector",aim=(1,0,0),u=(0,1,0),wu=(0,1,0))[0]
        cmds.connectAttr("{0}.output".format(aimAxisNode),"{0}.aimVector".format(cst),f=True)
        cmds.connectAttr("{0}.output".format(upAxisNode),"{0}.upVector".format(cst),f=True)
        cmds.parent(cst,self._guideGroup.getPartialPath())



    def build(self):
        """
        """
        super(Arm,self).build()

        # get ik system data
        ikJoints = self._ikfkSystem.getIkJoints()
        ctrl = rigControl.Control(name=self._clavicleJoint.getPartialPath().replace(rigName.BIND,rigName.CONTROL),
                                        position=cmds.xform(self._clavicleJoint.getPartialPath(),q=True,ws=True,t=True),
                                        parent=self._rigGroup,
                                        shape="circle",
                                        color=rigName.SIDECOLOR[rigName.getSide(self._name)])
        ctrl.create()
        ctrl.setMatrix(cmds.xform(self._clavicleJoint.getPartialPath(),q=True,ws=True,m=True))

        # constrain the joints to the controls
        cmds.pointConstraint(ctrl.getPartialPath(),self._clavicleJoint.getPartialPath())
        cmds.orientConstraint(ctrl.getPartialPath(),self._clavicleJoint.getPartialPath())


        cmds.parentConstraint(ctrl.getPartialPath(),ikJoints[0],mo=True)
        self._fkControls[0].setParent(ctrl)


    def postBuild(self):
        """
        """
        pass