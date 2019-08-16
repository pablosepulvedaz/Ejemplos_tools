'''
date:14/03/2018
version:Beta esta version es para exportar alembic y materiales
requerimiento:Believe sa
Implementacion: Python,wrap os, Frameworks(shutil),DevOps(SYS)
Prueba de modulo: hasta el momento no funciona nada bien solo es de exploracion.
'''
import os
import shutil
import maya.cmds as cmds
import sys
import platform
# mi Ventana
def Believetools():
    if cmds.window('abcShader',ex=True):
        cmds.deleteUI('abcShader',wnd=True)
    window = cmds.window('abcShader', title="Believe export Alembic" , sizeable=True )
    cmds.rowColumnLayout(numberOfColumns=1)
    #variable de entorno
    version='pablo sepulveda_V1'
    platform = sys.version
    cmds.setParent( '..' )
    #cmds.button(en=False,l=version)
    cmds.frameLayout(label="Materiales a Exportar") 
    cmds.rowColumnLayout(numberOfColumns=2,cw=[(1,200),(2,185)])
    cmds.rowColumnLayout(numberOfColumns=1)
    cmds.textScrollList("the_mod_list",w=200,h=170,bgc=(0.3,0.3,0.3))
    cmds.setParent( '..' )     
    cmds.rowColumnLayout(numberOfColumns=1)
    cmds.text(label=" ")    
    cmds.text(label="testeamos UI")
    cmds.text(label=" ")
    cmds.text(label=" ")     
    cmds.button(label="Selecciono_Mesh",h=30,w=200,c="load_mesh()")
    cmds.button(label="Remuevo_Mesh",h=30,w=200,c="remove_mesh()")    
    #Aqui ponemos los parents 
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    #Aqui ponemos los label para los nombres de ficheros //UI
    cmds.frameLayout(label="Salida del path:")
    cmds.rowColumnLayout(numberOfColumns=3,cw=[(1,90),(2,230),(3,60)])
    get_defaut_path = cmds.workspace(en="cache")
    cmds.text(fn="boldLabelFont",label="Salida path")
    the_out_abc_path = cmds.textField("thePath_to_out",ed=False,tx=get_defaut_path+"/")
    cmds.button(label="Set salida",c="set_path_output()")
    cmds.text(fn="boldLabelFont",label="nombre archivo")
    get_current_filename = cmds.file(q=True,sn=True)
    get_basename=os.path.splitext(os.path.basename(get_current_filename))
    cmds.textField("the_out_file_name",tx=get_basename[0])
    cmds.setParent( '..' ) 
    cmds.rowColumnLayout(numberOfColumns=4,cw=[(1,60),(2,100),(3,60),(4,100)])
    cmds.text(label="")
    cmds.button(label="shader out",c="MstcAlembicExport()")
    cmds.button(label="SG out",c="mstcSGexporter()")
    cmds.button(label="open path",c="open_path_output()")
    cmds.text(label="")    
    cmds.setParent( '..' )    
    cmds.setParent( '..' )    
    #niveles
    cmds.button( label='Selecciona el modelo para exportar alembic cache',h=30 ,command=('mstcalembicexporter()') )     
    cmds.button( label='Importar shaders',h=30 ,command=('importSGshader()') )           
    cmds.button( label='Aplicar shader al modelo',h=30 ,command=('MstcAlembicimport()') )     
    cmds.button( label='Close',h=30 ,command=('cmds.deleteUI(\"' + window + '\", window=True)') )
    cmds.text( label=' ', align='center', h=80)
    cmds.text( label=version, align='center', h=10,w=400)    
    #cmds.text( label='python'+platform, align='left' )
    cmds.setParent( '..' )
    cmds.showWindow( window )
#win def
def load_mesh():
    cmds.select(hi=True)
    get_all_mesh = cmds.ls(sl=True)
    get_all_mesh_string = ""
    for j in get_all_mesh:
        if cmds.nodeType(j) == "transform":
            get_all_mesh_string +=  "\""+ j  + "\","
    if len(get_all_mesh_string) != 0:
        cmds.textScrollList("the_mod_list",e=True,ra=True)
        exec("cmds.textScrollList(\"the_mod_list\",e=True,append=("+get_all_mesh_string[0:-1]+"))")

def remove_mesh():
    cmds.textScrollList("the_mod_list",e=True,ra=True)   
def open_path_output(): 
    get_tx_path=cmds.textField("thePath_to_out",q=True,tx=True)
    get_tx_path.replace("\\","/")
    if get_tx_path[-1]!="/":
        get_tx_path=get_tx_path+"/"
    os.startfile(get_tx_path)      
def set_path_output():
    get_path=cmds.fileDialog2(fileMode=3,caption="Ruta de la salida Believe")#NOTA aqui texto para la ventana pop de salida path
    if(str(get_path)!="None"):
        get_path_arr=str(get_path).split("'")
        cmds.textField("thePath_to_out",e=True,tx=get_path_arr[1]+"/")  
def mstcalembicexporter():
    maya.mel.eval('AlembicExportSelectionOptions;') 
    allModelGrp = cmds.ls(selection=True)  
def mstcSGexporter(): 
    outFolder = cmds.textField("thePath_to_out",q=True,tx=True)
    outName = cmds.textField("the_out_file_name",q=True,tx=True)
    outFile = outFolder + "/" + outName + "_sets.txt"
    outFile2 = outFolder + "/" + outName + "_shaderSG.txt"  
    outFile3 = outFolder + "/" + outName + "_shader.ma"
    cmds.file( rename=outFile3)
    cmds.file(force=True,exportSelected=True,type='mayaAscii')          
 
# alembic procedural copiar pegar

def MstcAlembicExport():
#--set el path de la ruta
    outFolder = cmds.textField("thePath_to_out",q=True,tx=True)
    outName = cmds.textField("the_out_file_name",q=True,tx=True)
    outFile = outFolder + "/" + outName + "_sets.txt"
    outFile2 = outFolder + "/" + outName + "_shaderSG.txt"  
    outFile3 = outFolder + "/" + outName + "_shaer.ma"        
#get obten todos los shadergroup //allshadGrp name
    #allMaterialGrp = cmds.ls(selection=True) //casi para todo es lo mismo. 
    allGeoGrp = cmds.textScrollList("the_mod_list",q=True,ai=True)    
    allGeos = []
    for i in range(len(allGeoGrp)):
        allGeoList = cmds.listRelatives(allGeoGrp[i], c = True, path = True)
        allGeos.extend(allGeoList)
    if allGeos == []:
        return
    #print allGeos  //Debug de lo que no necesito
#Busca shaders shadingeng
    allShdGrp = []
    for i in range(len(allGeos)):
        allConns = cmds.listConnections(allGeos[i], d = True, s = False)
        for j in range(len(allConns)):
            if cmds.nodeType(allConns[j]) == "shadingEngine":
                allShdGrp.append(allConns[j])           
    if allShdGrp == []:
        return
    #print allShdGrp    //Debug de nuevo                
    
    f = open(outFile, "w")
    for j in range(len(allGeoGrp)):
        f.writelines(allGeoGrp[j])
        f.writelines("\r\n") 
    f.close()       
    f = open(outFile2, "w")
    for j in range(len(allShdGrp)):
        f.writelines(allShdGrp[j])
        f.writelines("\r\n") 
    f.close()          
    # corremos Alembic nuevamente procedural
def MstcAlembicimport():
#Busco shader el .txt el path   
    outFolder = cmds.textField("thePath_to_out",q=True,tx=True)
    outName = cmds.textField("the_out_file_name",q=True,tx=True)
    outFile = outFolder + "/" + outName + "_sets.txt"
    outFile2 = outFolder + "/" + outName + "_shaderSG.txt"  
    outFile3 = outFolder + "/" + outName + "_shaer.ma"   
    
#leo ruta para los Set   
    if not os.access(outFile, os.R_OK):
        pass 
    f = open(outFile, "r")
    readContents = f.read()
    shaderList = readContents.split("\r\n")
    
#Leo ruta para los _"SG" shader groups 
    if not os.access(outFile2, os.R_OK):
        pass 
    f = open(outFile2, "r")
    readContents = f.read()
    SGList = readContents.split("\r\n")
# Busco en la Lista y Reemplazo
    shaderList.pop()  #borro el ultimo.
    SGList.pop() 
    count = 0
    for j in shaderList:
        j1 = str(j)
        #j2 = j1.replace("]","] ") // esto es para la lista
        j3 = 'select -r ' + j1
        maya.mel.eval(j3)
        cmds.sets( e=True, fe=(SGList[count]))
        cmds.select(clear=True)
        #pinto el contador 
        count += 1
#busco el Shape de la Geometria     
    # importo el alembic proceduralmente desde maya esto es llamarlo directamente
def importSGshader():
    outFolder = cmds.textField("thePath_to_out",q=True,tx=True)
    outName = cmds.textField("the_out_file_name",q=True,tx=True)
    outFile = outFolder + "/" + outName + "_sets.txt"
    outFile2 = outFolder + "/" + outName + "_shaderSG.txt"  
    outFile3 = outFolder + outName + "_shader.ma"  
    abcimportname = 'file -import -type "mayaAscii" -ra true -mergeNamespacesOnClash true -namespace ":" -options "v=0;p=17;f=0"  -pr '+'"'
    abcimportname2 = abcimportname + outFile3
    abcimportname3 = abcimportname2 + '"'
    abcimportname4 = str(abcimportname3)
    maya.mel.eval(abcimportname4)     
#listo    
Believetools()