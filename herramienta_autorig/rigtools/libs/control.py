import maya.cmds as cmds
import rigtools
import rigtools.libs.transform as rigTransform
import rigtools.libs.name as rigName
import rigtools.libs.jsonTranslator as jsonTranslator
import rigtools.libs.curve as rigCurve
reload(rigCurve)
import os
reload(jsonTranslator)

class Control(rigTransform.Transform):
    def __init__(self,name,position=(0,0,0),parent=None,shape="circle",color=rigName.LIGHTGREY):
        '''
        '''
        self._null = rigTransform.Transform(name="{0}_{1}".format(name,rigName.NULL),
                                            position=position,
                                            parent=parent)

        super(Control,self).__init__(name,position,parent)

        
        self._shape = shape
        self.setColor(color)

    # GET
    def getNull(self):
        '''
        '''
        return self._null

    def getNullPartialPath(self):
        '''
        '''
        return self._null.getPartialPath()

    def getNullFullPath(self):
        '''
        '''
        return self._null.getFullPath()

    def getColor(self):
        """
        Return color index

        :return: Index of color being used for this control
        :rtype: int
        """
        return self._color

    def getParentName(self):
        '''
        '''
        return self._null.getParentName()

    def getShape(self):
        '''
        '''
        dag = self._dag.getPath()
        shape = self._dag.extendToShape().partialPathName()
        self._dag = dag
        return shape

    def getShapeList(self):
        '''
        '''
        return cmds.listRelatives(self.getPartialPath(),c=True,shapes=True)

    # SET
    def setParent(self,value):
        '''
        '''
        self._null.setParent(value)

    def setPosition(self,value):
        '''
        '''
        self._null.setPosition(value)

    def setMatrix(self,value):
        '''
        '''
        self._null.setMatrix(value)

    def setColor(self,value):
        """

        """
        if isinstance(value,int):
            pass
        elif isinstance(value, float):
            value = int(value)
        else:
            raise TypeError("{0} must be an integer".format(value))

        if self.exists():
            for shape in self.getShapeList():
                cmds.setAttr("{0}.overrideEnabled".format(shape),1)
                cmds.setAttr("{0}.overrideColor".format(shape),value)
        
        self._color = value

    def setScale(self,value):
        """
        """
        cmds.scale(value,value,value,
            cmds.ls("{0}.cv[*]".format(self.getPartialPath()))[0],
            xyz=True)

    def create(self):
        """
        Abstract create method that will not create anything.
        """
        if not self._name:
            return

        self._null.setName("{0}_{1}".format(self._name,rigName.NULL))
        self._null.create()

        translator = jsonTranslator.JsonTranslator(rigtools.CONTROL_LIBRARY)
        data = translator.read()

        if cmds.objExists(self._name):
            newNode = self._name
            cmds.parent(newNode,self._null.getPartialPath())
        else:
            if self._shape in data.keys():
                newNode = cmds.rename(rigCurve.load(self._shape,rigtools.CONTROL_LIBRARY),self._name)
            else:
                newNode = cmds.circle(ch=False,name=self._name)[0]
            cmds.xform(newNode,ws=True,t=self._position)
            cmds.parent(newNode,self._null.getPartialPath())

        self.setMObject(newNode)
        self.setDagPath(newNode)

        self.setColor(self._color)
        
        del(self._name)


    def save(self,filepath,append=True):
        '''
        '''
        translator = jsonTranslator.JsonTranslator(filepath)

        data = dict()

        if os.path.isfile(filepath):
            data = translator.read()

        if not cmds.objExists(self.getPartialPath()):
            return 

        # controls dictionary data
        data[self.getPartialPath()] = {"shapes":dict(),"color":self.getColor(),"parent":self.getParentName()}
        # gather the control information.
        for shape in self.getShapeList():
            data[self.getPartialPath()]["shapes"][shape] = dict()
            data[self.getPartialPath()]["shapes"][shape]['svPosition'] = rigCurve.getPoints(shape)

            data[self.getPartialPath()]["shapes"][shape]['degree'] = cmds.getAttr("{0}.degree".format(shape))

        data[self.getPartialPath()]["dagPath"] = self.getFullPath()
        data[self.getPartialPath()]["worldPosition"] = self.getPosition()

        translator.setData(data)
        translator.write()

        
        




