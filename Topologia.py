#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      achavarriav
#
# Created:     29/06/2016
# Copyright:   (c) achavarriav 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, datetime
from arcpy import env
import os

today = datetime.date.today()
date = today.strftime('%m_%d')
mes = today.strftime('%m')

resultados = r'C:\Scripts\Topology\2018.gdb'
prj = r'C:\Scripts\PRJ\CRTM05.prj'
#usuario_path = arcpy.GetParameterAsText(0)
#usuario_path = r'C:\Respaldos\2016.gdb\Junio\mapa_06_28'

ingresados = arcpy.GetParameterAsText(0)


#ingresados = resultados + usuario_path
env.workspace = resultados
dicMes = {"01":"\\Enero","02":"\\Febrero","03":"\\Marzo","04":"\\Abril","05":"\\Mayo","06":"\\Junio","07":"\\Julio","08":"\\Agosto","09":"\\Setiembre","10":"\\Octubre","11":"\\Noviembre","12":"\\Diciembre"}

try:
    for i in dicMes:
        if mes == i:
            valor = dicMes[i]
            path_dataset = resultados + valor
            path_mapa = resultados + valor + "\\topo_" + str(date)
            path_topo = path_dataset + "\\topology_" + str(date)
            arcpy.AddMessage("Proceso en ejecución")

            if arcpy.Exists(valor):
                arcpy.env.overwriteOutput = True
                arcpy.CopyFeatures_management(ingresados, path_mapa)
                arcpy.CreateTopology_management(path_dataset,"topology_" + str(date))
                arcpy.AddFeatureClassToTopology_management(path_topo, path_mapa)
                arcpy.AddRuleToTopology_management(path_topo,"Must Not Have Gaps (Area)",path_mapa)
                arcpy.AddRuleToTopology_management(path_topo,"Must Not Overlap (Area)",path_mapa)
                arcpy.ValidateTopology_management(path_topo,"Full_Extent")
                arcpy.ExportTopologyErrors_management(path_topo,path_dataset,"topo" + str(date))

            else:
                arcpy.CreateFeatureDataset_management(resultados, valor, prj)
                arcpy.CopyFeatures_management(ingresados, path_mapa)
                arcpy.CreateTopology_management(path_dataset,"topology_" + str(date))
                arcpy.AddFeatureClassToTopology_management(path_topo, path_mapa)
                arcpy.AddRuleToTopology_management(path_topo,"Must Not Have Gaps (Area)",path_mapa)
                arcpy.AddRuleToTopology_management(path_topo,"Must Not Overlap (Area)",path_mapa)
                arcpy.ValidateTopology_management(path_topo,"Full_Extent")
                arcpy.ExportTopologyErrors_management(path_topo,path_dataset,"topo" + str(date))

    arcpy.AddMessage("Proceso ejecutado")
    arcpy.AddMessage(u"Copyright (c) Alfredo Chavarría Vargas")

except:
    print "Se ha detectado un error que impide ejecutar el script"
    print (arcpy.GetMessage(2))