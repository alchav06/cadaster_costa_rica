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

inputFile = arcpy.GetParameterAsText(0)
predios = arcpy.GetParameterAsText(1)

arcpy.Delete_management(r"C:\Scripts\Limits\Developing.gdb")
arcpy.Delete_management(r"C:\Scripts\Limits\Outputs.gdb")

##inputFile = r'C:\Scripts\Limits\Insumos\Limite_Distrital_1_5mil.shp'
madreDIR = r"C:\Scripts\Limits"
##predios = r"C:\Scripts\Limits\Distritos.gdb\\mapa_relate"

arcpy.CreateFileGDB_management(madreDIR,"Developing")
arcpy.CreateFileGDB_management(madreDIR,"Outputs")

intDir = r"C:\Scripts\Limits\Developing.gdb"
outDir = r"C:\Scripts\Limits\Outputs.gdb"
finalDir = r"C:\Scripts\Limits\Final.gdb"

prediosTemp = "predios"

listDist = "10701,10702,10703,10704,10705,10706,11801,20101,20102,20103,20104,20105,20106,20107,20108,20109,20110,20111,20112,20113,20114,20301,20302,20303,20304,20305,20307,20308,20801,20802,20803,20804,20805,30101,30102,30103,30104,30105,30106,30107,30108,30109,30110,30111,30201,30202,30203,30204,30205,30301,30302,30303,30304,30305,30306,30307,30308,30401,30402,30403,30601,30602,30603,40101,40102,40104,40201,40202,40203,40204,40205,40206,40301,40302,40303,40304,40305,40306,40307,40308,40401,40402,40403,40404,40405,40406,40501,40502,40503,40504,40505,40601,40602,40603,40604,40701,40702,40703,40801,40802,40803,40901,40902,50201,50202,50203,50204,50205,50207,50701,50702,50703,50704,50801,50802,50803,50804,50805,50806,50807,50901,50902,50903,50904,50905,50906,51101,51102,51103,51104,60101,60102,60103,60106,60107,60108,60109,60112,60114,60115,60116,60401,60402,60403,60301"
SQLmos = "COD_DTA = " + " OR COD_DTA = ".join(listDist.split(","))
arcpy.MakeFeatureLayer_management(inputFile,"inputTemp", SQLmos)

#Lee el shapefile para diferentes valores en atributos
rows = arcpy.SearchCursor("inputTemp")
row = rows.next()
attribute_types = set([])
listShp = []

env.workspace = r'C:\Scripts\Limits'
arcpy.env.overwriteOutput = True

while row:
    attribute_types.add(row.COD_DTA) #Busca por el atributo de COD_DTA
    row = rows.next()

#Crea un shapefile por cada atributo
for each_attribute in attribute_types:
    limitSHP = intDir + "\\DT" + str(each_attribute)
    arcpy.Select_analysis (inputFile, limitSHP, "\"COD_DTA\" = " + str(each_attribute))     #<-- CHANGE my_attribute to the name of your attribute
    limitTemp = str(each_attribute)

    #Crea shapefiles temporales para poder usar herramienta selection by location
    arcpy.MakeFeatureLayer_management(limitSHP,limitTemp)
    arcpy.MakeFeatureLayer_management(predios,prediosTemp)
    selection = arcpy.SelectLayerByLocation_management(prediosTemp,"INTERSECT",limitTemp,"","NEW_SELECTION","NOT_INVERT")

    selectPRE = outDir +"\\PR_"+str(each_attribute)
    arcpy.CopyFeatures_management(selection,selectPRE)

    arcpy.AddField_management(selectPRE, "DTA", "TEXT", "", "", "5", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(selectPRE, "DTA", str(each_attribute), "PYTHON_9.3")








#Crea una lista de todos los features classes en la GDB
env.workspace = outDir
featureClassGDB = arcpy.ListFeatureClasses()
for r in featureClassGDB:
    listShp.append(r)

#Herramienta merge para unir todos los feature classes
mergeSHP = finalDir + "\\listado_" + str(date)
arcpy.Merge_management(listShp,mergeSHP)

arcpy.AddField_management(mergeSHP, "COMP", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

expression = "val"
codeblock = "if [DTA] = Left( [PRM_IDENTIFICA],5 ) Then\
            val=1\
            else\
            val=0\
            end if"

arcpy.CalculateField_management(mergeSHP,"COMP",expression, "VB",codeblock)

del each_attribute, limitTemp, madreDIR, rows, row, attribute_types, intDir, outDir
