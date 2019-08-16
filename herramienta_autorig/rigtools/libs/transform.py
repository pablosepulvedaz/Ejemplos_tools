'''
This is containing the base class for maya objects
'''

import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
import rigtools.libs.mayaObject as rigMayaObject
reload(rigMayaObject)

class Transform(rigMayaObject.MayaObject):
    '''
    '''
    def __init__(self,name,position=(0,0,0),parent=None):
        '''
        '''
        super(Transform,self).__init__(name)

        # private members

        #protected
        # this variable gets detroyed during create.
        self.setParent(parent)
        self._position = position
    
    # GET
    def getParentPartialPath(self):
        '''
        '''
        if self._parent:
            return self._parent.getPartialPath()

        return None

    def getParentFullPath(self):
        '''
        '''
        if self._parent:
            return self._parent.getFullPath()

        return None

    def getParentName(self):
        """
        """
        if self._parent:
            return self._parent.getPartialPath().split("|")[-1]

        return None

    def getPosition(self,worldSpace=True):
        '''
        '''
        if worldSpace:
            return cmds.xform(self.getPartialPath(),q=True,ws=True,t=True)

        return cmds.xform(self.getPartialPath(),q=True,r=True,t=True)

    # SET
    def setParent(self,value):
        '''
        '''
        if not value:
            self._parent = None
            return

        if isinstance(value,Transform):
            print "hello--->  ",value
            self._parent = value
        else:
            self._parent = Transform(value)

        if self._parent.exists():
            if self.getFullPath():
                parentList = cmds.listRelatives(self.getFullPath(),p=True,f=True)
                if parentList:
                    if parentList[0] != self._parent.getFullPath():
                        cmds.parent(self.getFullPath(),self._parent.getFullPath()) 
                else:
                    cmds.parent(self.getFullPath(),self._parent.getFullPath()) 

    def setPosition(self,value):
        """
        """
        if self.exists():
            cmds.xform(self.getPartialPath(),ws=True,t=value)

        self._position = value

    def setMatrix(self,value):
        """
        """
        if self.exists():
            cmds.xform(self.getPartialPath(),ws=True,m=value)

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
            newNode = cmds.createNode("transform",n=self._name)
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