#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      achavarriav
#
# Created:     21/02/2016
# Copyright:   (c) achavarriav 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, datetime
from arcpy import env

today = datetime.date.today()
date = today.strftime('%m_%d')
mes = today.strftime('%m')

resultados = r'C:\Respaldos\2018.gdb'
env.workspace = resultados
arcpy.env.overwriteOutput = False
resultados = r'C:\Respaldos\2018.gdb'
prj = r'C:\Scripts\PRJ\CRTM05.prj'
dicMes = {"01":"\\Enero","02":"\\Febrero","03":"\\Marzo","04":"\\Abril","05":"\\Mayo","06":"\\Junio","07":"\\Julio","08":"\\Agosto","09":"\\Setiembre","10":"\\Octubre","11":"\\Noviembre","12":"\\Diciembre"}

try:
    for i in dicMes:
        if mes == i:
            valor = dicMes[i]
            path_mapa = resultados + valor + "\\mapa_" + str(date)
            path_mosaico = resultados + valor + "\\mosaico_" + str(date)
            if arcpy.Exists(valor):
                env.workspace = r'Database Connections\SIRI_PRODUCCION.sde\SIRIGISADMIN.CapasSIRIVersioned'
                arcpy.env.overwriteOutput = True
                arcpy.CopyFeatures_management("SIRIGISADMIN.PRM_PREDIO_MAPA", path_mapa)
                arcpy.CopyFeatures_management("SIRIGISADMIN.MOSAICO_PLANOS", path_mosaico)
            else:
                env.workspace = r'Database Connections\SIRI_PRODUCCION.sde\SIRIGISADMIN.CapasSIRIVersioned'
                arcpy.CreateFeatureDataset_management(resultados,valor, prj)
                arcpy.CopyFeatures_management("SIRIGISADMIN.PRM_PREDIO_MAPA", path_mapa)
                arcpy.CopyFeatures_management("SIRIGISADMIN.MOSAICO_PLANOS", path_mosaico)
    print "Ejecutado"

except:
    print "Se ha detectado un error que impide ejecutar el script"
    print (arcpy.GetMessage(2))
