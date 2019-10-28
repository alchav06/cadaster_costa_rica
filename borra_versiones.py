#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      achavarriav
#
# Created:     10/09/2018
# Copyright:   (c) achavarriav 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
from datetime import datetime
import time
from arcpy import env
env.overwriteOutput=True

d=(time.strftime("%Y_%m_%d"))
t1=(time.strftime("%I:%M:%S"))

#Variables de entrada
#versionName=arcpy.GetParameterAsText(0)

# crear version
#print "Creando version: "+d+" "+t1
arcpy.AddMessage("  ")
#arcpy.AddMessage(u" Eliminando Versión "+versionName+" "+str(d)+" "+str(t1))

versionName = arcpy.GetParameterAsText(0)
idioma = arcpy.GetParameter(1)

if idioma == True:
    inWorkspace =r'Conexiones de base de datos\SIRI_PRODUCCION.sde'

else:
    inWorkspace =r'Database Connections\SIRI_PRODUCCION.sde'

arcpy.DeleteVersion_management(inWorkspace, versionName)

t2=(time.strftime("%I:%M:%S"))
arcpy.AddMessage("  ")
arcpy.AddMessage(" Version Eliminada "+str(d)+" "+str(t2))

#print "Version eliminada"
