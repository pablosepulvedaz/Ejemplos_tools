'''
This is containing the base class for maya objects
'''

import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds


class MayaObject(object):
    '''
    '''
    def __init__(self,name):
        '''
        '''
        if name:
            self._name = name
        else:
            self._name = str()
        print self._name
        self.setMObject(self._name)
        self.setDagPath(self._name)
    
    # GET
    @staticmethod
    def getMObject(name):
        '''
        '''
        try:
            selList = OpenMaya.MSelectionList()
            selList.add(name)
            obj = selList.getDependNode(0)
        except:
            raise RuntimeError("{0} does not exist in the scene.".format(name))

        return obj

    @staticmethod
    def getDagPath(name):
        '''
        '''
        try:
            selList = OpenMaya.MSelectionList()
            selList.add(name)
            dag = selList.getDagPath(0)
        except:
            raise RuntimeError("{0} does not exist in the scene.".format(name))

        return dag

    def getPartialPath(self):
        '''
        '''
        return self._dag.partialPathName()

    def getFullPath(self):
        '''
        '''
        return self._dag.fullPathName()

    def getName(self):
        """
        """
        return self._dag.partialPathName().split("|")[-1]

    def exists(self):
        """
        """
        if cmds.objExists(self.getPartialPath()):
            return True

        return False

    # SET
    def setDagPath(self,value):
        """
        """
        if not cmds.objExists(value):
            self._dag = OpenMaya.MDagPath()
            return

        self._dag = self.getDagPath(value)

    def setMObject(self,value):
        """
        """
        if not cmds.objExists(value):
            self._object = OpenMaya.MObject()
            return

        self._object = self.getMObject(value)

    def setName(self,value):
        """
        """
        if "_name" in dir(self):
            self._name = value
            self.setMObject(value)
            self.setDagPath(value)
