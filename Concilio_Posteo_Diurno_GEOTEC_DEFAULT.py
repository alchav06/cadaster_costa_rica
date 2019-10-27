#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Conciliar desde DEFAULT
# Purpose:
#
# Author:      achavarriav
#
# Created:     31/08/2017
# Copyright:   (c) achavarriav 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os
import datetime
import time
from arcpy import env

env.overwriteOutput=True
versionPROD = "SDE.ProduccionGEO"
versionGEO = "SDE.GEOTEC"
versionDEF = "SDE.DEFAULT"

dia =(time.strftime("%Y_%m_%d"))
t1 =(time.strftime("%I:%M:%S"))
sde = r'Database Connections\SIRI_PRODUCCION.sde'

arcpy.AddMessage("  ")
arcpy.AddMessage("Conciliando... " +str(dia)+" "+str(t1))

try:

    arcpy.ReconcileVersions_management(sde,"ALL_VERSIONS",versionDEF,versionGEO,"LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","NO_POST","KEEP_VERSION")
    t1 =(time.strftime("%I:%M:%S"))
    arcpy.AddMessage("  ")
    arcpy.AddMessage(u"Se concilió de la versión: "+ versionDEF +" hacia "+ versionGEO + " " + str(dia) + " " + str(t1))
    arcpy.AddMessage("EJECUTADO")

except:
    print "Se ha detectado un error que impide ejecutar el script"
    print (arcpy.GetMessage(2))
