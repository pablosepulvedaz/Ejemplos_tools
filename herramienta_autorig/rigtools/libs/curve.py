"""
"""

import rigtools.libs.transform as rigTransform
import rigtools.libs.jsonTranslator as jsonTranslator
import maya.cmds as cmds
import os

def save(curves,filepath,append=True):
    '''
    '''
    translator = jsonTranslator.JsonTranslator(filepath)

    data = dict()

    if append:
        if os.path.isfile(filepath):
            data = translator.read()

    if not isinstance(curves,(tuple,list)):
        curves = [curves]

    for curve in curves:
        if not cmds.objExists(curve):
            return 

        # controls dictionary data
        data[curve] = {"shapes":dict()}
        # gather the control information.
        for shape in cmds.listRelatives(curve,c=True,shapes=True):
            data[curve]["shapes"][shape] = dict()
            data[curve]["shapes"][shape]['cvsPositions'] = getPoints(shape)
            data[curve]["shapes"][shape]['degree'] = cmds.getAttr("{0}.degree".format(shape))

    translator.setData(data)
    translator.write()

def load(curve,filepath):
    '''
    '''
    translator = jsonTranslator.JsonTranslator(filepath)
    data = translator.read()

    parent = None
    transforms = list()
    for shape in data[curve]["shapes"]:
        if cmds.objExists(curve):
            parent = curve
        shapeCurve = createCurve(data[curve]["shapes"][shape]['cvsPositions'],data[curve]["shapes"][shape]['degree'],curve)
        if parent:
            cmds.parent(cmds.listRelatives(shapeCurve,c=True,shapes=True)[0],parent,s=True,r=True)
            transforms.append(shapeCurve)
    if transforms:
        cmds.delete(transforms)
    return curve

    

def createCurve(points,degree=1,name="curve"):
    """
    """
    knotList = list()
    # 3 
    if degree == 3:
        knotList = [0,0]
        knotList.extend(range(len(points) - 2))
        knotList.extend([knotList[-1],knotList[-1]])
    elif degree == 1:
        # 1
        knotList = range(len(points))

    if knotList:
        curve = cmds.curve (degree = degree, point = points, knot = knotList)
        curve = cmds.rename(curve,name)

    return curve

def getCVs(name):
    """

    """
    if cmds.objExists(name):
        return cmds.ls("{0}.cv[*]".format(name),flatten=True)

def getPoints(name):
    """
    """
    points = list()

    for cv in getCVs(name):
        points.append(cmds.xform(cv,q=True,ws=True,t=True))

    return points












