"""
This is a module that store the base class for 
all of our rig parts (components).
"""


import maya.cmds as cmds
import rigtools.libs.transform as rigTransform
import rigtools.libs.control as rigControl
import rigtools.libs.name as rigName
import rigtools.libs.joint as rigJoint
reload(rigControl)

cmds.loadPlugin("matrixNodes",quiet=True)

class Part(object):
    def __init__(self,name):
        """
        Constructor method
        """
        self._name = name
        
        # setup variables
        self._setupGroup = rigTransform.Transform("{0}_setup".format(name))
        self._bindGroup = rigTransform.Transform("{0}_bind".format(name),parent=self._setupGroup)
        self._guideGroup = rigTransform.Transform("{0}_guide".format(name),parent=self._setupGroup)
        self._masterGuide = rigControl.Control("{0}_master_{0}".format(name,rigName.GUIDE),
                                    position=(0,0,0),
                                    parent= self._guideGroup,
                                    shape="circle",
                                    color = rigName.DARKRED)

        # build variables
        self._rigGroup = rigTransform.Transform("{0}_rig".format(name))
        
    # GET
    def _getSide(self):
        """
        """
        side = rigName.getSide(self._name)
        if not side:
            raise RuntimeError("can't find side based on name template in rigtools.libs.name!")

        return side

    def setup(self):
        """
        """
        self._setupGroup.create()
        self._bindGroup.create()
        self._guideGroup.create()
        self._masterGuide.create()
        self._masterGuide.setScale(2)

    def postSetup(self):
        """
        """
        joints = cmds.listRelatives(self._bindGroup.getPartialPath(),ad=True,type="joint") or list()
        joints.reverse()
        cmds.addAttr(self._masterGuide.getPartialPath(),ln="displayAxis",at="enum",enumName="Off:On",keyable=True)
        for jnt in joints:
            cmds.connectAttr("{0}.displayAxis".format(self._masterGuide.getPartialPath()),"{0}.displayLocalAxis".format(jnt))
            cmds.setAttr("{0}.overrideEnabled".format(jnt),1)
            cmds.setAttr("{0}.overrideDisplayType".format(jnt),2)

    def runSetup(self):
        """
        """
        self.setup()
        self.postSetup()

    def preBuild(self):
        """
        """
        if self._guideGroup.exists():
            cmds.delete(self._guideGroup.getPartialPath())

        joints = cmds.listRelatives(self._bindGroup.getPartialPath(),ad=True,type="joint")
        joints.reverse()
        rigJoint.Joint.rotateToOrient(joints)
    
    def build(self):
        """
        """
        self._rigGroup.create()

        self._bindGroup.setParent(self._rigGroup.getPartialPath())
        
        if self._setupGroup.exists():
            cmds.delete(self._setupGroup.getFullPath())

    def postBuild(self):
        """
        """
        pass

    def runBuild(self):
        """
        """
        self.preBuild()
        self.build()
        self.postBuild()

    def _createGuide(self,joint,color=rigName.BLUE):
        '''
        This will create a guide

        :param joint: The name of the joint you want to create a guide for.
        :type joint: rigtools.libs.joint.Joint | str

        :param color: Color you want to set you control to.
        :type color: int

        :return: guide that was created for the joint
        :rtype: rigtools.libs.control.Control
        '''
        # ERROR CHECKING--------------
        if isinstance(joint,rigTransform.Transform):
            if joint.exists():
                position = joint.getPosition()
                joint = joint.getName()
            else:
                raise RuntimeError("{0} does not exist in the current Maya session!".format(joint.getName()))
        elif isinstance(joint,basestring):
            if cmds.objExists(joint):
                position = cmds.xform(joint,q=True,ws=True,t=True)
            else:
                raise RuntimeError("{0} does not exist in the current Maya session!".format(joint.getName()))
        else:
            raise TypeError('You did not pass in the correct data type.\nYou must pass a "rigtools.libs.joint.Joint" object or a "str".')


        # create the guide.
        guide = rigControl.Control("{0}_{1}".format(joint,rigName.GUIDE),
                                    position=position,
                                    parent= self._masterGuide,
                                    shape="sphere",
                                    color = color)
        guide.create()

        # create constraint and parent to guides group
        cst = cmds.pointConstraint(guide.getPartialPath(),joint)[0]
        cmds.parent(cst,self._guideGroup.getPartialPath())

        return guide
