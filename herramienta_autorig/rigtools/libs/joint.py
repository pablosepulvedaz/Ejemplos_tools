import maya.cmds as cmds

import rigtools.libs.transform as rigTransform
reload(rigTransform)

class Joint(rigTransform.Transform):
    def __init__(self,name,position=(0,0,0),parent=None):
        '''
        '''
        super(Joint,self).__init__(name,position,parent)

    def create(self):
        """
        Abstract create method that will not create anything.
        """
        if not self._name:
            return

        cmds.select(cl=True)
        if cmds.objExists(self._name):
            newNode = self._name
        else:
            newNode = cmds.joint(n=self._name)
            cmds.xform(newNode,ws=True,t=self._position)

        self.setMObject(newNode)
        self.setDagPath(newNode)

        if self._parent:
            if cmds.objExists(self._parent.getPartialPath()):
                cmds.parent(newNode,self._parent.getPartialPath())
            else:
                self._parent.create()
                cmds.parent(newNode,self._parent.getPartialPath())
        
        del(self._name)

    @staticmethod
    def rotateToOrient(joints):
        """
        """
        for jnt in joints:
            parent = cmds.listRelatives(jnt,p=True)
            ort = cmds.xform(jnt,q=True,ws=True,rotation=True)
            rotOrder = cmds.xform(jnt,q=True,roo=True)
            if parent:
                cmds.parent(jnt,w=True)
            cmds.setAttr(jnt+".rotateOrder", 0)
            cmds.setAttr(jnt+".r",0,0,0)
            cmds.setAttr(jnt+".jo",*ort)
            cmds.xform(jnt,roo=rotOrder)
            if parent:
                cmds.parent(jnt,parent)


