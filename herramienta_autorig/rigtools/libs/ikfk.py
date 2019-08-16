"""
This is for all ikfk functions and classes that deal with IK/FK
functionality.
"""
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import rigtools.libs.name as rigName
reload(rigName)
import rigtools.libs.joint as rigJoint

class IkFkBase(object):
    def __init__(self,joints):
        """
        This is the constructor method. 

        :param joints: This should be the joints you want to use for the system
        :type joints: list | tuple
        """
        # protected members.
        self.setOriginalJoints(joints)
        self._ikJoints = list()
        self._fkJoints = list()
        self._blendJoints = list()
        self._group = "ikfk_{0}".format(rigName.GROUP)

    # GET
    def getIkJoints(self):
        """
        Return the IK joints for this class.

        :return: Ik joints
        :rtype: list
        """
        return self._ikJoints

    def getFkJoints(self):
        """
        Return the FK joints for this class.

        :return: FK joints
        :rtype: list
        """
        return self._fkJoints

    def getBlendJoints(self):
        """
        Return the BLEND joints for this class.

        :return: Blend joints
        :rtype: list
        """
        return self._blendJoints

    def getOriginalJoints(self):
        """
        Return the ORIGINAL joints for this class.

        :return: Original joints
        :rtype: list
        """
        return self._originalJoints

    def getGroup(self):
        """
        """
        return self._group

    # SET
    def setIkJoints(self,value):
        """
        Set the IK joints for this class to the value passed in.

        :param value: List of joints you want to be you IK joints
        :rtype: list | tuple
        """
        # check to see if "value" argument is a  list|tuple.
        if not isinstance(value,(list,tuple)):
            raise TypeError("{0} must be a list or tuple of strings (joint names).".format(value))
        
        self._ikJoints = value

    def setFkJoints(self,value):
        """
        Set the FK joints for this class to the value passed in.

        :param value: List of joints you want to be you FK joints
        :rtype: list | tuple
        """
        # check to see if "value" argument is a  list|tuple.
        if not isinstance(value,(list,tuple)):
            raise TypeError("{0} must be a list or tuple of strings (joint names).".format(value))

        self._fkJoints = value

    def setBlendJoints(self,value):
        """
        Set the BLEND joints for this class to the value passed in.

        :param value: List of joints you want to be you Blend joints
        :rtype: list | tuple
        """
        # check to see if "value" argument is a  list|tuple.
        if not isinstance(value,(list,tuple)):
            raise TypeError("{0} must be a list or tuple of strings (joint names).".format(value))

        self._blendJoints = value

    def setOriginalJoints(self,value):
        """
        Set the original joints for this class to the value passed in.

        :param value: List of joints you want to be you original joints
        :rtype: list | tuple
        """
        # check to see if "value" argument is a  list|tuple.
        if not isinstance(value,(list,tuple)):
            raise TypeError("{0} must be a list or tuple of strings (joint names).".format(value))

        self._originalJoints = value

    def setGroup(self,value):
        """
        """
        if not isinstance(value,basestring):
            return TypeError("{0} must be a string.".format(value))

        self._group = value

    def create(self):
        """
        Create the IK/FK system. 
        """

        # create the group if it does not exist in the Maya sesssion.
        if not cmds.objExists(self._group):
            cmds.createNode("transform",n=self._group)

        # create ikfk switchable attribute
        cmds.addAttr(self._group,ln="ikfk",at="double",min=0,max=1,dv=0,keyable=True)
        ikfkAttr = "{0}.ikfk".format(self._group)

        # 
        ikParent = self._group
        fkParent = self._group
        blendParent = self._group

        for jnt in self._originalJoints:
            ikJnt = cmds.duplicate(jnt,name="{0}_{1}".format(jnt,rigName.IK),rr=True,po=True)[0]
            fkJnt = cmds.duplicate(jnt,name="{0}_{1}".format(jnt,rigName.FK),rr=True,po=True)[0]
            blendJnt = cmds.duplicate(jnt,name="{0}_blend".format(jnt),rr=True,po=True)[0]

            # making connections between IK/FK joints and their corresponding blend joint.
            bcnRot = cmds.createNode("blendColors",name="{0}_rot_{1}".format(blendJnt,rigName.BLENDCOLORS))
            bcnTrs = cmds.createNode("blendColors",name="{0}_trs_{1}".format(blendJnt,rigName.BLENDCOLORS))
            # connect BlendColors rotate node
            cmds.connectAttr("{0}.rotate".format(fkJnt),"{0}.color1".format(bcnRot),f=True)
            cmds.connectAttr("{0}.rotate".format(ikJnt),"{0}.color2".format(bcnRot),f=True)

            # connect blendColors translate node
            cmds.connectAttr("{0}.translate".format(fkJnt),"{0}.color1".format(bcnTrs),f=True)
            cmds.connectAttr("{0}.translate".format(ikJnt),"{0}.color2".format(bcnTrs),f=True)

            # connect blendColors nodes to blend joint.
            cmds.connectAttr("{0}.output".format(bcnRot),"{0}.rotate".format(blendJnt),f=True)
            cmds.connectAttr("{0}.output".format(bcnTrs),"{0}.translate".format(blendJnt),f=True)

            # connect IK/FK attribute to the blendColors nodes.
            for bcn in (bcnRot,bcnTrs):
                cmds.connectAttr(ikfkAttr,"{0}.blender".format(bcn),f=True)


            # setting the parent for the joints
            cmds.parent(ikJnt,ikParent)
            cmds.parent(fkJnt,fkParent)
            cmds.parent(blendJnt,blendParent)

            # reset the parents.
            ikParent = ikJnt
            fkParent = fkJnt
            blendParent = blendJnt

            # adding each joint to their respective list
            self._ikJoints.append(ikJnt)
            self._fkJoints.append(fkJnt)
            self._blendJoints.append(blendJnt)

class IkFkLimb(IkFkBase):
    def __init__(self,joints):
        """
        This is the constructor.
        """
        super(IkFkLimb,self).__init__(joints)
        # set member variables.
        # public

        #private

        #protected
        self._handle = str()

    def setOriginalJoints(self,value):
        """
        Set the original joints for this class to the value passed in.

        :param value: List of joints you want to be you original joints
        :rtype: list | tuple
        """
        # check to see if "value" argument is a  list|tuple.
        if len(value) != 3:
            raise RuntimeError("This class can only take 3 joints.")

        super(IkFkLimb,self).setOriginalJoints(value)

    def setHandle(self,value):
        """
        """

        self._handle = value

    def getHandle(self):
        """
        """
        return self._handle


    @staticmethod
    def getPolevectorPosition(joints,multiplier=3):
        """
        :param joints: Joints you want to get the pole vector position for.
        :type joints: list | tuple

        :param multiplier: Scalar value for the pole vector.
        :type multiplier: int | float
        """ 
        if not isinstance(joints,(list,tuple)):
            raise TypeError("{0} must be a list or tuple of strings (joint names).".format(joints))
        elif len(joints) != 3:
            raise RuntimeError("This class can only take 3 joints.")
        elif not isinstance(multiplier,(int,float)):
            raise TypeError("{0} must be a number.".format(multiplier))

        # create joint variables
        startJoint = joints[0]
        middleJoint = joints[1]
        endJoint = joints[2]

        #get joint positions
        startPos = cmds.xform(startJoint,q=True,ws=True,t=True)
        middlePos = cmds.xform(middleJoint,q=True,ws=True,t=True)
        endPos = cmds.xform(endJoint,q=True,ws=True,t=True)

        # store joint positions in vectors
        startVector = OpenMaya.MVector(*startPos)
        middleVector = OpenMaya.MVector(*middlePos)
        endVector = OpenMaya.MVector(*endPos)

        # do the math for the pole vector.
        centerVector = (startVector + endVector) / 2
        diffVector = (middleVector - centerVector) * multiplier
        poleVector = diffVector + centerVector

        return (poleVector.x,poleVector.y,poleVector.z)

    def create(self):
        """
        """
        super(IkFkLimb,self).create()

        self.setHandle(cmds.ikHandle(sj=self._ikJoints[0],ee=self._ikJoints[-1],sol="ikRPsolver")[0])
        cmds.parent(self._handle,self._group)