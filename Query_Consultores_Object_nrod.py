#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        prueba_atributos
# Purpose:
#
# Author:      achavarriav
#
# Created:     14/10/2016
# Copyright:   (c) achavarriav 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os
import datetime
import time
import string
from arcpy import env

lista = []

dsc = arcpy.Describe("SIRIGISADMIN.MOSAICO_PLANOS")
selection_set = dsc.FIDSet
env.workspace = r"Database Connections\SIRI_PRODUCCION.sde"
for version in arcpy.da.ListVersions(env.workspace):
    if 'nrodriguezc' in version.name:
        arcpy.AddMessage("\n ESTE USUARIO NO TIENE PERMISOS PARA EJECUTAR EL SCRIPT. \n")
        raise sys.exit(u"ERROR: DEBE SELECCIONAR ALGÚN POLÍGONO PARA QUE EL SCRIPT FUNCIONE." + arcpy.GetMessages(x))
    else:


if len(selection_set) == 0:
    raise sys.exit(u"ERROR: DEBE SELECCIONAR ALGÚN POLÍGONO PARA QUE EL SCRIPT FUNCIONE." + arcpy.GetMessages(x))

else:

    for row in arcpy.SearchCursor("SIRIGISADMIN.MOSAICO_PLANOS",['OID@']):
        dato = row.OBJECTID
        lista.append(str(dato))
        final = ",".join(lista)

    queryStr = "NOT OBJECTID ='" + "' AND NOT OBJECTID = '".join(final.split(",")) + "'"

    arcpy.AddMessage(u"Query: " + str(queryStr))

    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    for lyr in arcpy.mapping.ListLayers(mxd, "", df):
        if lyr.name == "SIRIGISADMIN.MOSAICO_PLANOS":
            lyr.definitionQuery = queryStr
    arcpy.RefreshActiveView()

del mxd
del queryStr
del final

