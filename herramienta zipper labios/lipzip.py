import maya.cmds as mc
#ESTO ES PARA CONVERTIR LOS JOINT EN UNA LISTA
lipJoints= mc.ls(sl=True)
#ESTO AGRUPA LOS JOINTS Y LES CAMBIA EL NOMBRE AL GRUPO GRP
#TENER NOMBRADO EL JOINT JAW COMO jaw_bind
for joint in lipJoints:
    grp = mc.createNode('transform', n = joint.replace('bind','grp'))
    mc.delete(mc.parentConstraint('jaw_bind',grp))
    mc.parent(joint,grp)

#names grups lip_open_grp  lip__closed_grp lip_open_grp1
#                           lip_ct_tp_Closed_grp lip_ct_tp_grpBind
#TODO ESO JUNTO SELECIONAMOS GRUPOS DE JOINTS ZIP
#skull_rotation_lip_grp hacer GRUPO EN LA MISMA POSICION QUE EL JOINT JAW
#   
groups = mc.ls(sl=True)
for g in groups:
    cons= mc.parentConstraint('skull_rotation_lip_grp','jaw_bind', g)[0]
    mc.addAttr('jaw_ctl', longName='%s' %g, defaultValue=0.0, minValue=0.0, maxValue=1.0,k= True, h= False )
    reverse = mc.createNode('reverse', n= '%s_reverse' %g)
    mc.connectAttr('jaw_ctl.%s' %g, '%s.skull_rotation_lip_grpW0' %cons)
    mc.connectAttr('jaw_ctl.%s' %g, '%s.inputX' %reverse)
    mc.connectAttr('%s.outputX' %reverse, '%s.jaw_bindW1' %cons)
    
groups = mc.ls(sl=True)
for g in groups:
    cons= mc.parentConstraint('skull_rotation_lip_grp','jaw_bind', g)[0]
    mc.addAttr('jaw_ctl', longName='%s' %g, defaultValue=0.0, minValue=0.0, maxValue=1.0,k= True, h= False )
    reverse = mc.createNode('reverse', n= '%s_reverse' %g)
    mc.connectAttr('jaw_ctl.%s' %g, '%s.skull_rotation_lip_grpW0' %cons)
    mc.connectAttr('jaw_ctl.%s' %g, '%s.inputX' %reverse)
    mc.connectAttr('%s.outputX' %reverse, '%s.jaw_bindW1' %cons)

    blender= mc.createNode('blendTwoAttr', n= '%s_blendTwoAttr' %g)
    nameOpen = g.replace('grpBind','grp')
    nameClosed= g.replace('grpBind','Closed_grp')
    mc.connectAttr('jaw_ctl.%s' %nameOpen, '%s.input[0]' %blender)
    mc.connectAttr('jaw_ctl.%s' %nameClosed, '%s.input[1]' %blender)
    mc.connectAttr('%s.output' %blender, 'jaw_ctl.%s' %g)

     