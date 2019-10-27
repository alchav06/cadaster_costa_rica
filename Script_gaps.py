#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Pruebas_Revisión de Gaps en vías públicas
# Purpose:
#
# Author:      achavarriav
#
# Created:     28/11/2017
# Copyright:   (c) achavarriav 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os
import datetime
import time
from arcpy import env

today = datetime.date.today()
date = today.strftime('%m_%d')
mes = today.strftime('%m')

#resultados = r'C:\Scripts\Gaps\Gaps.gdb'
#env.workspace = resultados
#arcpy.env.overwriteOutput = False
#prj = r'C:\Scripts\PRJ\CRTM05.prj'
#dicMes = {"01":"\\Enero","02":"\\Febrero","03":"\\Marzo","04":"\\Abril","05":"\\Mayo","06":"\\Junio","07":"\\Julio","08":"\\Agosto","09":"\\Setiembre","10":"\\Octubre","11":"\\Noviembre","12":"\\Diciembre"}
#via = "10701V00000100"
##gaps = r'D:\Alfredo Chavarría\Topología\2017\11 - Noviembre\II Quincena\Vías\errores_gaps_vias.shp'

gaps = arcpy.GetParameterAsText(0)

#Definir variables

madreDIR = r"C:\Scripts\Gaps"
arcpy.CreateFileGDB_management(madreDIR,"Pruebas_Developing")
arcpy.CreateFileGDB_management(madreDIR,"Pruebas_Outputs")

##inputFile = r"C:\Scripts\Gaps\Pruebas_Inputs.gdb\\vias_prueba"

inputFile = arcpy.GetParameterAsText(1)
outDir = r"C:\Scripts\Gaps\Pruebas_Outputs.gdb"
intDir = r"C:\Scripts\Gaps\Pruebas_Developing.gdb"
finalDir = r"C:\Scripts\Gaps\Final.gdb"
##gaps = r"C:\Scripts\Gaps\Pruebas_Inputs.gdb\\errores_gaps_pruebas"
gapsTemp = "gaps"

#Lee el shapefile para diferentes valores en atributos
rows = arcpy.SearchCursor(inputFile)
row = rows.next()
attribute_types = set([])
listShp = []

env.workspace = r'C:\Scripts\Gaps'
arcpy.env.overwriteOutput = True

while row:
    attribute_types.add(row.PRM_IDENTIFICA) #Busca por el atributo de Identificador
    row = rows.next()

#Crea un shapefile por cada atributo
for each_attribute in attribute_types:
    intSHP = intDir + "\\ID" + each_attribute
    arcpy.Select_analysis (inputFile, intSHP, "\"PRM_IDENTIFICA\" = '" + each_attribute + "'")     #<-- CHANGE my_attribute to the name of your attribute
    shpTemp = str(each_attribute)

    #Crea shapefiles temporales para poder usar herramienta selection by location
    arcpy.MakeFeatureLayer_management(intSHP,shpTemp)
    arcpy.MakeFeatureLayer_management(gaps,gapsTemp)
    selection = arcpy.SelectLayerByLocation_management(gapsTemp,"BOUNDARY_TOUCHES",shpTemp,"","NEW_SELECTION","NOT_INVERT")

    #Ingresa todos los polígonos de la selección dentro del shapefile
    arcpy.Append_management(selection,intSHP,"NO_TEST","","")

    #La herramienta Dissolve une todos los polígonos en uno solo
    outSHP = outDir + "\\ID" + each_attribute
    arcpy.Dissolve_management(intSHP,outSHP, dissolve_field="", statistics_fields="OBJECTID FIRST;PRM_PROVINCIA FIRST;PRM_CANTON FIRST;PRM_DISTRITO FIRST;PRM_DUPLICADO FIRST;PRM_HORIZONTAL FIRST;PRM_FINCA FIRST;PRM_IDENTIFICA FIRST;PRM_COMPATIBLE FIRST;PRM_PLANO FIRST;PRM_RELACION FIRST;PRM_PARCELA FIRST;PRM_BLOQUE FIRST;PRM_PREDIO FIRST;PRM_INCONS_01 FIRST;PRM_INCONS_02 FIRST;PRM_INCONS_03 FIRST;PRM_INCONS_04 FIRST;PRM_INCONS_05 FIRST;PRM_INCONS_06 FIRST;PRM_INCONS_07 FIRST;PRM_INCONS_08 FIRST;PRM_INCONS_09 FIRST;PRM_INCONS_10 FIRST;PRM_INCONS_11 FIRST;PRM_MODIFICA_1 FIRST;PRM_MODIFICA_2 FIRST;PRM_MODIFICA_3 FIRST;PRM_MODIFICA_4 FIRST;PRM_MODIFICA_5 FIRST;PRM_MODIFICA_6 FIRST;PRM_MODIFICA_7 FIRST;PRM_MODIFICA_9 FIRST;PRM_RAC FIRST;PRM_ABRE FIRST;PRM_INFORMANTE FIRST;PRM_INGRESO FIRST;PRM_CONOCE FIRST;PRM_CARNE FIRST;PRM_NPROVINCIA FIRST;PRM_NCANTON FIRST;PRM_NDISTRITO FIRST;PRM_ID FIRST;PRM_INCONS_12 FIRST;CREATED_USER FIRST;CREATED_DATE FIRST;LAST_EDITED_USER FIRST;LAST_EDITED_DATE FIRST;CERTIFICADO FIRST;Shape_Length FIRST;Shape_Area FIRST", multi_part="SINGLE_PART", unsplit_lines="DISSOLVE_LINES")
    del outSHP, intSHP

#Crea una lista de todos los features classes en la GDB
env.workspace = outDir
featureClassGDB = arcpy.ListFeatureClasses()
for r in featureClassGDB:
    listShp.append(r)

#Herramienta merge para unir todos los feature classes
arcpy.Merge_management(listShp,finalDir + "\\vias_final")

del selection, each_attribute, shpTemp, madreDIR, gaps, gapsTemp

#Borrar las GDBs

arcpy.AddMessage(u"El proceso fue realizado con éxito.\n")
arcpy.AddMessage(u"Copyright (c) Alfredo Chavarría Vargas")

del rows, row, attribute_types

#END