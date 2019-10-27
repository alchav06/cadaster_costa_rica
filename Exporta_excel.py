#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      achavarriav
#
# Created:     30/06/2016
# Copyright:   (c) achavarriav 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, datetime
from arcpy import env
import os


insumo_base = arcpy.GetParameterAsText(0)
#insumo_base = r'D:\Alfredo Chavarría\Respaldos Mapa\2016\Respaldos_SIRI_2016.gdb\junio_mapa_I'

mes_usuario = arcpy.GetParameterAsText(1)
mes = "\\" + mes_usuario
#mes = "\\junio"
quincena = arcpy.GetParameterAsText(2)


today = datetime.date.today()
date = today.strftime('%m_%d')


dicMes = {"01":"\\Enero","02":"\\Febrero","03":"\\Marzo","04":"\\Abril","05":"\\Mayo","06":"\\Junio","07":"\\Julio","08":"\\Agosto","09":"\\Setiembre","10":"\\Octubre","11":"\\Noviembre","12":"\\Diciembre"}
resultados = r"C:\Scripts\Atributos\2018"
env.workspace = resultados

if quincena == True:
    path_exporta = "_I.xls"

else:
    path_exporta = "_II.xls"

#path_exporta = "_I.xls"

try:
        path_mapa = resultados + mes + path_exporta
        arcpy.TableToExcel_conversion(insumo_base,path_mapa,"ALIAS","CODE")
        arcpy.ExcelToTable_conversion(path_mapa,path_mapa)

except:
    print "Se ha detectado un error que impide ejecutar el script"
    print (arcpy.GetMessage(2))

