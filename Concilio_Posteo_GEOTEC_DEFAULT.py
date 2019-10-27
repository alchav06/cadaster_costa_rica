#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Conciliar hacia GEOTEC y DEFAULT
# Purpose:
#
# Author:      achavarriav
#
# Created:     24/02/2016
# Copyright:   (c) achavarriav 2016
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

    arcpy.ReconcileVersions_management(sde,"ALL_VERSIONS",versionDEF,versionGEO,"LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_EDIT_VERSION","POST","KEEP_VERSION")
    t2 =(time.strftime("%I:%M:%S"))
    arcpy.AddMessage("  ")
    arcpy.AddMessage(u"Se concilió de la versión: "+ versionGEO +" hacia "+ versionDEF + " " + str(dia) + " " + str(t2))
    arcpy.AddMessage("EJECUTADO")

except:
    print "Se ha detectado un error que impide ejecutar el script"
    print (arcpy.GetMessage(2))

