'''

'''
import maya.cmds as cmds
def switch(node,attribute,switchAttributes,switchValues,defaultValue=0):
    '''
    Description

    example::
        switch("master_l_guide",attribute="aimAxis",["X","Y","Z","-X","-Y",-Z"],[[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]])

    :param node: Node you want attribute on.
    :type node: str

    :param attribute: Attribute to create for the switch 
    :type attribute: str

    :param switchAttributes: Array of strings you want on you switch attribute
    :type: list | tuple

    :param switchValues: Array of double3 vector values you want for your switch
    :type switchValues: list | tuple

    :return: Return the choice node created by this function
    :rtype: str
    ''' 
    if cmds.objExists(node):
        if not cmds.objExists("{0}.{1}".format(node,attribute)):
            cmds.addAttr(node,ln=attribute,at="enum",enumName=":".join(switchAttributes),keyable=True,dv=defaultValue)


    #create the choice node
    choiceNode = cmds.createNode("choice",n="{0}_choice".format(node))

    for i,value in enumerate(switchValues):
        cmds.addAttr(choiceNode,ln="choice{0}".format(i),at="double3",keyable=True)
        cmds.addAttr(choiceNode,ln="choice{0}_X".format(i),at="double",keyable=True,parent="choice{0}".format(i),dv=value[0])
        cmds.addAttr(choiceNode,ln="choice{0}_Y".format(i),at="double",keyable=True,parent="choice{0}".format(i),dv=value[1])
        cmds.addAttr(choiceNode,ln="choice{0}_Z".format(i),at="double",keyable=True,parent="choice{0}".format(i),dv=value[2])
        cmds.connectAttr("{0}.choice{1}".format(choiceNode,i),"{0}.input[{1}]".format(choiceNode,i),f=True)

    cmds.connectAttr("{0}.{1}".format(node,attribute),"{0}.selector".format(choiceNode),f=True)

    return choiceNode




def lock(node,attributes):
    """
    """
    if not cmds.objExists(node):
        raise RuntimeError("{0} does not exist in the current Maya session.".format(node))
    if isinstance(attributes,basestring):
        attributes = [attributes]

    if not isinstance(attributes,(tuple,list)):
        raise TypeError("{0} must be a list or a tuple of attributes.")

    for attribute in attributes:
        cmds.setAttr("{0}.{1}".format(node,attribute),lock=True)

def hide(node,attributes):
    """
    """
    if not cmds.objExists(node):
        raise RuntimeError("{0} does not exist in the current Maya session.".format(node))
    if isinstance(attributes,basestring):
        attributes = [attributes]

    if not isinstance(attributes,(tuple,list)):
        raise TypeError("{0} must be a list or a tuple of attributes.")
        
    for attribute in attributes:
        cmds.setAttr("{0}.{1}".format(node,attribute),keyable=False,channelBox=False)

def lockAndHide(node,attributes):
    lock(node,attributes)
    hide(node,attributes)