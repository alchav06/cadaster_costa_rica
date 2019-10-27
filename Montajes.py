#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Montajes
# Purpose:     Elaboración de Montajes de Sobreposición para Mantenimiento Catastral
#
# Author:      Alfredo H. Chavarría Vargas
#
# Created:     19/04/2016
# Copyright:   (c) Alfredo H. Chavarría Vargas
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os
import datetime
import time
import string
from arcpy import env

##ingresados = "304495571981,312651132008"
##ubic = "30103"
##version = ".achavarriav"

#Ingreso de las variables generales

tipoMS = arcpy.GetParameter(0)
ingresados = arcpy.GetParameterAsText(1)
ubic = arcpy.GetParameterAsText(2)
versionName = arcpy.GetParameterAsText(3)

version = '"OPS$RNPCR\\' + string.upper(versionName) + '"' + "." + versionName
version = str(version)

#Borrar los feature class utilizados

env.workspace = r"C:\Scripts\Montajes\Temp.gdb"

featureClassGDB = arcpy.ListFeatureClasses()
for dfc in featureClassGDB:
    arcpy.Delete_management(dfc)
    del dfc
del featureClassGDB

if versionName == "nrodriguezc":
    versionName = "error"
    arcpy.AddMessage("\n ESTE USUARIO NO TIENE PERMISOS PARA EJECUTAR EL SCRIPT. \n")

else:
    if tipoMS == "Inconsistencia 06":

        #Declaración de segundas variables

        env.workspace = r'Database Connections\SIRI_PRODUCCION.sde\SIRIGISADMIN.CapasSIRIVersioned'
        arcpy.env.overwriteOutput = True
        prj = r'C:\Scripts\PRJ\CRTM05.prj'
        temp = r"C:\Scripts\Montajes\Temp.gdb"
        mxd = arcpy.mapping.MapDocument("C:\Scripts\Montajes\Montaje_base.mxd")

        #Variables de Data_Frames
        df = arcpy.mapping.ListDataFrames(mxd, "Mapa_Traslape")[0]
        dfZoom = arcpy.mapping.ListDataFrames(mxd, "Detalle_Traslape")[0]
        dfMapa = arcpy.mapping.ListDataFrames(mxd, "Predios_Ubic")[0]

        #Variables para estilos
        lyrSty = r"C:\Scripts\Montajes\Styles"
        count = 1

        #Variables para c?digo de situaci?n
        listProv = {"1":"1 - San Jose","2":"2 - Alajuela","3":"3 - Cartago","4":"4 - Heredia","5":"5 - Guanacaste","6":"6 - Puntarenas","7":"7 - Limón"}
        listCan = {"101":"01 - San Jose","107":"07 - Mora","118":"18 - Curridabat","201":"01 - Alajuela","203":"03 - Grecia","208":"08 - Poas","209":"09 - Orotina","211":"11 - Zarcero","301":"01 - Cartago","302":"02 - Paraiso","303":"03 - La Union","304":"04 - Jimenez","306":"06 - Alvarado","401":"01 - Heredia","402":"02 - Barva","403":"03 - Santo Domingo","404":"04 - Santa Barbara","405":"05 - San Rafael","406":"06 - San Isidro","407":"07 - Belen","408":"08 - Flores","409":"09 - San Pablo","501":"01 - Liberia","502":"02 - Nicoya","503":"03 - Santa Cruz","506":"06 - Cañas","507":"07 - Abangares","508":"08 - Tilaran","509":"09 - Nandayure","510":"10 - La Cruz","511":"11 - Hojancha","601":"01 - Puntarenas","602":"02 - Esparza","603":"03 - Buenos Aires","604":"04 - Montes de Oro","608":"08 - Coto Brus","610":"10 - Corredores","701":"01 - Limon","703":"03 - Siquirres","704":"04 - Talamanca","705":"05 - Matina"}
        listDist = {"10701":"01 - Colon","10702":"02 - Guayabo","10703":"03 - Tabarcia","10704":"04 - Piedras Negras","10705":"05 - Picagres","10706":"06 - Jaris","10707":"07 - Quitirrisi","11801":"01 - Curridabat","11803":"03 - Sanchez","20103":"03 - Carrizal","20104":"04 - San Antonio","20105":"05 - Guacima","20106":"06 - San Isidro","20107":"07 - Sabanilla","20108":"08 - San Rafael","20109":"09 - Rio Segundo","20110":"10 - Desamparados","20111":"11 - Turrucares","20112":"12 - Tambor","20113":"13 - La Garita","20114":"14 - Sarapiqui","20301":"01 - Grecia","20302":"02 - San Isidro","20303":"03 - San Jose","20304":"04 - San Roque","20305":"05 - Tacares","20307":"07 - Puente de Piedra","20308":"08 - Bolivar","20801":"01 - San Pedro ","20802":"02 - San Juan","20803":"03 - San Rafael","20804":"04 - Carrillos","20805":"05 - Sabana Redonda","20901":"01 - Orotina","20902":"02 - El Mastate","20903":"03 - Hacienda Vieja","20904":"04 - Coyolar","20905":"05 - La Ceiba","21101":"01 - Zarcero","21102":"02 - Laguna","21103":"03 - Tapezco","21104":"04 - Guadalupe","21105":"05 - Palmira","21107":"07 - Brisas","30101":"01 - Oriental","30102":"02 - Occidental","30103":"03 - Carmen","30104":"04 - San Nicolas","30105":"05 - Agua Caliente","30106":"06 - Guadalupe","30107":"07 - Corralillo","30108":"08 - Tierra Blanca","30109":"09 - Dulce Nombre","30110":"10 - Llano Grande","30111":"11 - Quebradilla","30201":"01 - Paraiso","30202":"02 - Santiago","30203":"03 - Orosi","30204":"04 - Cachi","30205":"05 - Llanos de Santa Lucia","30301":"01 - Tres Rios","30302":"02 - San Diego","30303":"03 - San Juan","30304":"04 - San Rafael","30305":"05 - Concepcion","30306":"06 - Dulce Nombre","30307":"07 - San Ramon","30308":"08 - Rio Azul","30401":"01 - Juan Viñas","30402":"02 - Tucurrique","30403":"03 - Pejibaye","30601":"01 - Pacayas","30602":"02 - Cervantes","30603":"03 - Capellades","40101":"01 - Heredia","40102":"02 - Mercedes","40104":"04 - Ulloa","40201":"01 - Barva","40202":"02 - San Pedro ","40203":"03 - San Pablo","40204":"04 - San Roque","40205":"05 - Santa Lucia","40206":"06 - San Jose de la Montana","40301":"01 - Santo Domingo","40302":"02 - San Vicente","40303":"03 - San Miguel","40304":"04 - Paracito","40305":"05 - Santo Tomas","40306":"06 - Santa Rosa","40307":"07 - Tures","40308":"08 - Para","40401":"01 - Santa Barbara ","40402":"02 - San Pedro ","40403":"03 - San Juan ","40404":"04 - Jesus ","40405":"05 - Santo Domingo","40406":"06 - Puraba","40501":"01 - San Rafael","40502":"02 - San Josecito","40503":"03 - Santiago","40504":"04 - Angeles","40505":"05 - Concepcion","40601":"01 - San Isidro","40602":"02 - San Jose","40603":"03 - Concepcion","40604":"04 - San Francisco","40701":"01 - San Antonio","40702":"02 - La Ribera","40703":"03 - Asuncion","40801":"01 - San Joaquin","40802":"02 - Barrantes","40803":"03 - Llorente","40901":"01 - San Pablo","40902":"02 - Rincon de Sabanilla","50104":"04 - Nacascolo","50201":"01 - Nicoya","50202":"02 - Mansion","50203":"03 - San Antonio","50204":"04 - Quebrada Honda","50205":"05 - Samara","50207":"07 - Belen de Nosarita","50701":"01 - Las Juntas","50702":"02 - Sierra","50703":"03 - San Juan","50704":"04 - Colorado","50801":"01 - Tilaran","50802":"02 - Quebrada Grande","50803":"03 - Tronadora","50804":"04 - Santa Rosa","50805":"05 - Libano","50806":"06 - Tierra Morenas","50807":"07 - Arenal","50901":"01 - Carmona ","50902":"02 - Santa Rita","50903":"03 - Zapotal","50904":"04 - San Pablo","50905":"05 - Porvenir","50906":"06 - Bejuco","51004":"04 - Santa Elena","51101":"01 - Hojancha","51102":"02 - Monte Romo","51103":"03 - Puerto Carrillo","51104":"04 - Huacas","60101":"01 - Puntarenas","60102":"02 - Pitahaya","60103":"03 - Chomes","60106":"06 - Manzanillo","60107":"07 - Guacimal","60108":"08 - Barranca","60109":"09 - Monte Verde","60112":"12 - Chacarita","60114":"14 - Acapulco","60115":"15 - El Roble","60116":"16 - Arancibia","60201":"01 - Espiritu Santo","60202":"02 - San Juan Grande","60206":"06 - Caldera","60401":"01 - Miramar","60402":"02 - La Union","60403":"03 - San Isidro","60301":"01 - Buenos Aires","60804":"04 - Limoncito","61003":"03 - Canoas","70102":"02 - Valle la Estrella","70103":"03 - Río Blanco","70302":"02 - Pacuarito","70401":"01 - Bratsi","70402":"02 - Sixaola","70501":"01 - Matina"}

        arcpy.AddMessage("  ")
        arcpy.AddMessage(u"Copyright (c) Alfredo Chavarría Vargas \n")
        arcpy.AddMessage(u"Se han indicado los siguientes parámetros para realizar el montaje:")
        arcpy.AddMessage(u"Versión: " + str(version))
        arcpy.AddMessage(u"Ubicación: " + str(ubic))
        arcpy.AddMessage("Planos: " + str(ingresados))
        arcpy.AddMessage(u"El montaje se está realizando... \n")

        try:

            #Intersect para obtener traslape
            SQLmos = "NUMERO_PLA = '" + "' OR NUMERO_PLA = '".join(ingresados.split(",")) + "'"
            arcpy.MakeFeatureLayer_management("SIRIGISADMIN.MOSAICO_PLANOS","layer_mos", SQLmos)
            arcpy.ChangeVersion_management("layer_mos", "TRANSACTIONAL", version)
            arcpy.CopyFeatures_management("layer_mos",temp + "\\Mosaico_Catastral")
            arcpy.Intersect_analysis("layer_mos",temp + "\\Traslape")

            #Carga las capas del Intersect y la totalidad de los planos involucrados
            rutaMos = r'C:\Scripts\Montajes\Temp.gdb\Mosaico_Catastral'
            rutaTras = r'C:\Scripts\Montajes\Temp.gdb\Traslape'

            mosLayer = arcpy.mapping.Layer(rutaMos)
            arcpy.mapping.AddLayer(df, mosLayer,"TOP")
            arcpy.mapping.AddLayer(dfMapa, mosLayer,"TOP")

            trasLayer = arcpy.mapping.Layer(rutaTras)

            arcpy.mapping.AddLayer(df, trasLayer,"TOP")
            arcpy.mapping.AddLayer(dfZoom, trasLayer,"TOP")

            updateLayerT = arcpy.mapping.ListLayers(mxd, "Traslape", df)[0]
            sourceLayerT = arcpy.mapping.Layer(r"C:\Scripts\Montajes\Styles\trasNet.lyr")
            arcpy.mapping.UpdateLayer(df, updateLayerT, sourceLayerT, True)

            updateLayerTzoom = arcpy.mapping.ListLayers(mxd, "Traslape", dfZoom)[0]
            arcpy.mapping.UpdateLayer(dfZoom, updateLayerTzoom, sourceLayerT, True)

            updateLayerMO = arcpy.mapping.ListLayers(mxd, "Mosaico_Catastral", df)[0]
            sourceLayerMO = arcpy.mapping.Layer(r"C:\Scripts\Montajes\Styles\Vacios.lyr")
            arcpy.mapping.UpdateLayer(df, updateLayerMO, sourceLayerMO, True)

            updateLayerMOmapa = arcpy.mapping.ListLayers(mxd, "Mosaico_Catastral", dfMapa)[0]
            arcpy.mapping.UpdateLayer(dfMapa, updateLayerMOmapa, sourceLayerMO, True)


            #Ciclo para cargar planos y asignar simbologia
            listMos = ingresados.split(",")
            for i in listMos:
                SQLplano = "NUMERO_PLA = '" + i + "'"
                nameTemp = "PL_" + str(i)
                rutaTemp = temp + "\\" + nameTemp
                arcpy.MakeFeatureLayer_management("SIRIGISADMIN.MOSAICO_PLANOS",nameTemp, SQLplano)
                arcpy.ChangeVersion_management(nameTemp, "TRANSACTIONAL", version)
                arcpy.CopyFeatures_management(nameTemp,rutaTemp)

                lyrTemp = arcpy.mapping.Layer(rutaTemp)
                arcpy.mapping.AddLayer(df, lyrTemp,"TOP")
                arcpy.mapping.AddLayer(dfZoom, lyrTemp,"TOP")

                tabla = rutaTemp

                lyrStyRuta = lyrSty + "\\M" + str(count) + ".lyr"
                lyrStyTemp = "M" + str(count)
                updateLayer = arcpy.mapping.ListLayers(mxd, nameTemp, df)[0]
                sourceLayer = arcpy.mapping.Layer(lyrStyRuta)
                arcpy.mapping.UpdateLayer(df, updateLayer, sourceLayer, True)

                updateLayerZoom = arcpy.mapping.ListLayers(mxd, nameTemp, dfZoom)[0]
                arcpy.mapping.UpdateLayer(dfZoom, updateLayerZoom, sourceLayer, True)

                count = count + 1

            #Realizar zoom a las pol?gonos clave de los DATAFRAMES
            lyr = arcpy.mapping.ListLayers(mxd, "Mosaico_Catastral",df)[0]
            ext = lyr.getExtent()
            df.extent = ext
            dfMapa.extent = ext

            lyrZoom = arcpy.mapping.ListLayers(mxd, "Traslape",dfZoom)[0]
            extZ = lyrZoom.getExtent()
            dfZoom.extent = extZ

            #Llena los datos de la ubicaci?n y simbolog?a en el cajet?n de Montajes
            prov = ubic [0]
            cant = ubic [0:3]
            dist = ubic [0:5]

            for i in listProv:
                if prov == i:
                    Fprov = listProv[i]
            for i in listCan:
                if cant == i:
                    Fcant = listCan[i]
            for i in listDist:
                if dist == i:
                    Fdist = listDist[i]

            for elem in arcpy.mapping.ListLayoutElements(mxd):
                if elem.name == "Dprov":
                    elem.text = str(Fprov)
                    elem.elementPositionX = 8.75
                    elem.elementPositionY = 3
                if elem.name == "Dcan":
                    elem.text = str(Fcant)
                    elem.elementPositionX = 8.75
                    elem.elementPositionY = 2.25
                if elem.name == "Ddis":
                    elem.text = str(Fdist)
                    elem.elementPositionX = 8.75
                    elem.elementPositionY = 1.5
                if elem.name == "simbologia":
                    removeLyr = arcpy.mapping.ListLayers(mxd, "Mosaico_Catastral")[0]
                    elem.removeItem(removeLyr)
                    elem.elementHeight = 3.2

            #Variables para ID y NUM_PLANO en cajet?n
            env.workspace = r"C:\Scripts\Montajes\Temp.gdb"
            Bcount = 1

            #Llena los datos de ID y n?mero de planos en el cajet?n de Montajes
            featureClassList = arcpy.ListFeatureClasses("PL_*")
            for fc in featureClassList:
                datos = arcpy.SearchCursor(fc,"","","IDENTIFICA;NUMERO_PLA")
                for dato in datos:
                    datosTemp = "ID " + str(dato.IDENTIFICA) + ", PL_" + str(dato.NUMERO_PLA)
                    for elem in arcpy.mapping.ListLayoutElements(mxd):
                        if elem.name == "ID" + str(Bcount):
                            elem.text = str(datosTemp)
                Bcount = Bcount + 1

            mxd.saveACopy(r"C:\Scripts\Montajes\Montaje_Final.mxd")

            carpetaSalida = r"C:\Scripts\Montajes\Resultados"
            nombre = "MS_PL" + "_PL".join(ingresados.split(","))
            rutaSalida = carpetaSalida + "\\" + nombre + ".pdf"
            arcpy.mapping.ExportToPDF(mxd,rutaSalida)

            del mxd, df, dfMapa, dfZoom, mosLayer, rutaMos, rutaTras, rutaTemp, dato

            arcpy.Delete_management(r"C:\Scripts\Montajes\Montaje_Final.mxd")

            arcpy.AddMessage(u"Se crea el montaje con el siguiente nombre: " + str(nombre))
            arcpy.AddMessage(u"El montaje se ubica en la siguiente ruta: " + str(rutaSalida))
            arcpy.AddMessage(u"El proceso fue realizado con éxito.\n")
            arcpy.AddMessage(u"Copyright (c) Alfredo Chavarría Vargas")

            # Copyright:   (c) achavarriav 2016

        except:
            arcpy.AddMessage("Se ha detectado un error que impide ejecutar el script")
            arcpy.AddMessage(arcpy.GetMessage(2))

    else:

        env.workspace = r'Database Connections\SIRI_PRODUCCION.sde\SIRIGISADMIN.CapasSIRIVersioned'
        arcpy.env.overwriteOutput = True
        prj = r'C:\Scripts\PRJ\CRTM05.prj'
        temp = r"C:\Scripts\Montajes\Temp.gdb"
        mxd = arcpy.mapping.MapDocument("C:\Scripts\Montajes\Montaje_base_siete.mxd")

        #Variables de Data_Frames
        df = arcpy.mapping.ListDataFrames(mxd, "Mapa_Traslape")[0]
        dfZoom = arcpy.mapping.ListDataFrames(mxd, "Detalle_Traslape")[0]
        dfMapa = arcpy.mapping.ListDataFrames(mxd, "Predios_Ubic")[0]

        #Variables para estilos
        lyrSty = r"C:\Scripts\Montajes\Styles"


        #Variables para c?digo de situaci?n
        listProv = {"1":"1 - San Jose","2":"2 - Alajuela","3":"3 - Cartago","4":"4 - Heredia","5":"5 - Guanacaste","6":"6 - Puntarenas","7":"7 - Limón"}
        listCan = {"101":"01 - San Jose","107":"07 - Mora","118":"18 - Curridabat","201":"01 - Alajuela","203":"03 - Grecia","208":"08 - Poas","209":"09 - Orotina","211":"11 - Zarcero","301":"01 - Cartago","302":"02 - Paraiso","303":"03 - La Union","304":"04 - Jimenez","306":"06 - Alvarado","401":"01 - Heredia","402":"02 - Barva","403":"03 - Santo Domingo","404":"04 - Santa Barbara","405":"05 - San Rafael","406":"06 - San Isidro","407":"07 - Belen","408":"08 - Flores","409":"09 - San Pablo","501":"01 - Liberia","502":"02 - Nicoya","503":"03 - Santa Cruz","506":"06 - Cañas","507":"07 - Abangares","508":"08 - Tilaran","509":"09 - Nandayure","510":"10 - La Cruz","511":"11 - Hojancha","601":"01 - Puntarenas","602":"02 - Esparza","603":"03 - Buenos Aires","604":"04 - Montes de Oro","608":"08 - Coto Brus","610":"10 - Corredores","701":"01 - Limon","703":"03 - Siquirres","704":"04 - Talamanca","705":"05 - Matina"}
        listDist = {"10701":"01 - Colon","10702":"02 - Guayabo","10703":"03 - Tabarcia","10704":"04 - Piedras Negras","10705":"05 - Picagres","10706":"06 - Jaris","10707":"07 - Quitirrisi","11801":"01 - Curridabat","11803":"03 - Sanchez","20103":"03 - Carrizal","20104":"04 - San Antonio","20105":"05 - Guacima","20106":"06 - San Isidro","20107":"07 - Sabanilla","20108":"08 - San Rafael","20109":"09 - Rio Segundo","20110":"10 - Desamparados","20111":"11 - Turrucares","20112":"12 - Tambor","20113":"13 - La Garita","20114":"14 - Sarapiqui","20301":"01 - Grecia","20302":"02 - San Isidro","20303":"03 - San Jose","20304":"04 - San Roque","20305":"05 - Tacares","20307":"07 - Puente de Piedra","20308":"08 - Bolivar","20801":"01 - San Pedro ","20802":"02 - San Juan","20803":"03 - San Rafael","20804":"04 - Carrillos","20805":"05 - Sabana Redonda","20901":"01 - Orotina","20902":"02 - El Mastate","20903":"03 - Hacienda Vieja","20904":"04 - Coyolar","20905":"05 - La Ceiba","21101":"01 - Zarcero","21102":"02 - Laguna","21103":"03 - Tapezco","21104":"04 - Guadalupe","21105":"05 - Palmira","21107":"07 - Brisas","30101":"01 - Oriental","30102":"02 - Occidental","30103":"03 - Carmen","30104":"04 - San Nicolas","30105":"05 - Agua Caliente","30106":"06 - Guadalupe","30107":"07 - Corralillo","30108":"08 - Tierra Blanca","30109":"09 - Dulce Nombre","30110":"10 - Llano Grande","30111":"11 - Quebradilla","30201":"01 - Paraiso","30202":"02 - Santiago","30203":"03 - Orosi","30204":"04 - Cachi","30205":"05 - Llanos de Santa Lucia","30301":"01 - Tres Rios","30302":"02 - San Diego","30303":"03 - San Juan","30304":"04 - San Rafael","30305":"05 - Concepcion","30306":"06 - Dulce Nombre","30307":"07 - San Ramon","30308":"08 - Rio Azul","30401":"01 - Juan Viñas","30402":"02 - Tucurrique","30403":"03 - Pejibaye","30601":"01 - Pacayas","30602":"02 - Cervantes","30603":"03 - Capellades","40101":"01 - Heredia","40102":"02 - Mercedes","40104":"04 - Ulloa","40201":"01 - Barva","40202":"02 - San Pedro ","40203":"03 - San Pablo","40204":"04 - San Roque","40205":"05 - Santa Lucia","40206":"06 - San Jose de la Montana","40301":"01 - Santo Domingo","40302":"02 - San Vicente","40303":"03 - San Miguel","40304":"04 - Paracito","40305":"05 - Santo Tomas","40306":"06 - Santa Rosa","40307":"07 - Tures","40308":"08 - Para","40401":"01 - Santa Barbara ","40402":"02 - San Pedro ","40403":"03 - San Juan ","40404":"04 - Jesus ","40405":"05 - Santo Domingo","40406":"06 - Puraba","40501":"01 - San Rafael","40502":"02 - San Josecito","40503":"03 - Santiago","40504":"04 - Angeles","40505":"05 - Concepcion","40601":"01 - San Isidro","40602":"02 - San Jose","40603":"03 - Concepcion","40604":"04 - San Francisco","40701":"01 - San Antonio","40702":"02 - La Ribera","40703":"03 - Asuncion","40801":"01 - San Joaquin","40802":"02 - Barrantes","40803":"03 - Llorente","40901":"01 - San Pablo","40902":"02 - Rincon de Sabanilla","50104":"04 - Nacascolo","50201":"01 - Nicoya","50202":"02 - Mansion","50203":"03 - San Antonio","50204":"04 - Quebrada Honda","50205":"05 - Samara","50207":"07 - Belen de Nosarita","50701":"01 - Las Juntas","50702":"02 - Sierra","50703":"03 - San Juan","50704":"04 - Colorado","50801":"01 - Tilaran","50802":"02 - Quebrada Grande","50803":"03 - Tronadora","50804":"04 - Santa Rosa","50805":"05 - Libano","50806":"06 - Tierra Morenas","50807":"07 - Arenal","50901":"01 - Carmona ","50902":"02 - Santa Rita","50903":"03 - Zapotal","50904":"04 - San Pablo","50905":"05 - Porvenir","50906":"06 - Bejuco","51004":"04 - Santa Elena","51101":"01 - Hojancha","51102":"02 - Monte Romo","51103":"03 - Puerto Carrillo","51104":"04 - Huacas","60101":"01 - Puntarenas","60102":"02 - Pitahaya","60103":"03 - Chomes","60106":"06 - Manzanillo","60107":"07 - Guacimal","60108":"08 - Barranca","60109":"09 - Monte Verde","60112":"12 - Chacarita","60114":"14 - Acapulco","60115":"15 - El Roble","60116":"16 - Arancibia","60201":"01 - Espiritu Santo","60202":"02 - San Juan Grande","60206":"06 - Caldera","60401":"01 - Miramar","60402":"02 - La Union","60403":"03 - San Isidro","60301":"01 - Buenos Aires","60804":"04 - Limoncito","61003":"03 - Canoas","70102":"02 - Valle la Estrella","70103":"03 - Río Blanco","70302":"02 - Pacuarito","70401":"01 - Bratsi","70402":"02 - Sixaola","70501":"01 - Matina"}

        ##arcpy.AddMessage("  ")
        ##arcpy.AddMessage(u"Copyright (c) Alfredo Chavarría Vargas \n")
        ##arcpy.AddMessage(u"Se han indicado los siguientes parámetros para realizar el montaje:")
        ##arcpy.AddMessage(u"Versión: " + str(version))
        ##arcpy.AddMessage(u"Ubicación: " + str(ubic))
        ##arcpy.AddMessage("Planos: " + str(ingresados))
        ##arcpy.AddMessage(u"El montaje se está realizando... \n")

        try:

            #Intersect para obtener traslape
            SQLmos = "NUMERO_PLA = '" + str(ingresados) + "'"
            nameTemp = "PL_" + str(ingresados)

            arcpy.MakeFeatureLayer_management("SIRIGISADMIN.MOSAICO_PLANOS",nameTemp, SQLmos)
            arcpy.ChangeVersion_management(nameTemp, "TRANSACTIONAL", version)

            rutaPL = temp + "\\" + nameTemp
            rutaTras = r'C:\Scripts\Montajes\Temp.gdb\Traslape'
            rutaVias = r'Database Connections\SIRI_PRODUCCION.sde\SIRIGISADMIN.CapaSIRISICbd\SIRIGISADMIN.CADI_VIAS_PUBLICAS'

            arcpy.CopyFeatures_management(nameTemp,rutaPL)
            arcpy.Intersect_analysis([rutaPL,rutaVias],rutaTras)


            #Carga las capas del Intersect y la totalidad de los planos involucrados
            trasLayer = arcpy.mapping.Layer(rutaTras)

            arcpy.mapping.AddLayer(df, trasLayer,"TOP")
            arcpy.mapping.AddLayer(dfZoom, trasLayer,"TOP")

            plLayer = arcpy.mapping.Layer(rutaPL)

            arcpy.mapping.AddLayer(df, plLayer,"TOP")
            arcpy.mapping.AddLayer(dfZoom, plLayer,"TOP")


            updateLayerT = arcpy.mapping.ListLayers(mxd, "Traslape", df)[0]
            sourceLayerT = arcpy.mapping.Layer(r"C:\Scripts\Montajes\Styles\trasSIETE.lyr")
            arcpy.mapping.UpdateLayer(df, updateLayerT, sourceLayerT, True)

            updateLayerTzoom = arcpy.mapping.ListLayers(mxd, "Traslape", dfZoom)[0]
            arcpy.mapping.UpdateLayer(dfZoom, updateLayerTzoom, sourceLayerT, True)

            updateLayer = arcpy.mapping.ListLayers(mxd, nameTemp, df)[0]
            sourceLayer = arcpy.mapping.Layer(r"C:\Scripts\Montajes\Styles\M1.lyr")
            arcpy.mapping.UpdateLayer(df, updateLayer, sourceLayer, True)

            updateLayerZoom = arcpy.mapping.ListLayers(mxd, nameTemp, dfZoom)[0]
            arcpy.mapping.UpdateLayer(dfZoom, updateLayerZoom, sourceLayer, True)

            #Ciclo para cargar planos y asignar simbologia
            listMos = ingresados

            #Realizar zoom a las pol?gonos clave de los DATAFRAMES
            lyr = arcpy.mapping.ListLayers(mxd, nameTemp,df)[0]
            ext = lyr.getExtent()
            df.extent = ext

            lyrZoom = arcpy.mapping.ListLayers(mxd, "Traslape",dfZoom)[0]
            extZ = lyrZoom.getExtent()
            dfZoom.extent = extZ

            #Llena los datos de la ubicaci?n y simbolog?a en el cajet?n de Montajes
            prov = ubic [0]
            cant = ubic [0:3]
            dist = ubic [0:5]

            for i in listProv:
                if prov == i:
                    Fprov = listProv[i]
            for i in listCan:
                if cant == i:
                    Fcant = listCan[i]
            for i in listDist:
                if dist == i:
                    Fdist = listDist[i]

            for elem in arcpy.mapping.ListLayoutElements(mxd):
                if elem.name == "Dprov":
                    elem.text = str(Fprov)
                    elem.elementPositionX = 8.75
                    elem.elementPositionY = 3
                if elem.name == "Dcan":
                    elem.text = str(Fcant)
                    elem.elementPositionX = 8.75
                    elem.elementPositionY = 2.25
                if elem.name == "Ddis":
                    elem.text = str(Fdist)
                    elem.elementPositionX = 8.75
                    elem.elementPositionY = 1.5
                if elem.name == "simbologia":
                    elem.elementHeight = 3.2

            #Variables para ID y NUM_PLANO en cajet?n
            env.workspace = r"C:\Scripts\Montajes\Temp.gdb"


            #Llena los datos de ID y n?mero de planos en el cajet?n de Montajes
            datos = arcpy.SearchCursor(rutaPL,"","","IDENTIFICA;NUMERO_PLA")
            for dato in datos:
                datosTemp = "ID " + str(dato.IDENTIFICA) + ", PL_" + str(dato.NUMERO_PLA)
                for elem in arcpy.mapping.ListLayoutElements(mxd):
                    if elem.name == "ID1":
                        elem.text = str(datosTemp)


            mxd.saveACopy(r"C:\Scripts\Montajes\Montaje_Final_Siete.mxd")

            carpetaSalida = r"C:\Scripts\Montajes\Resultados"
            nombre = "MS" + str(dato.IDENTIFICA) + "_inc07"
            rutaSalida = carpetaSalida + "\\" + nombre + ".pdf"
            arcpy.mapping.ExportToPDF(mxd,rutaSalida)

            del mxd, df, dfMapa, dfZoom, rutaTras, rutaPL, rutaVias, dato

            arcpy.Delete_management(r"C:\Scripts\Montajes\Montaje_Final_Siete.mxd")


            arcpy.AddMessage(u"Se crea el montaje con el siguiente nombre: " + str(nombre))
            arcpy.AddMessage(u"El montaje se ubica en la siguiente ruta: " + str(rutaSalida))
            arcpy.AddMessage(u"El proceso fue realizado con éxito.\n")
            arcpy.AddMessage(u"Copyright (c) Alfredo Chavarría Vargas")

            # Copyright:   (c) achavarriav 2016

        except:
            arcpy.AddMessage("Se ha detectado un error que impide ejecutar el script")
            arcpy.AddMessage(arcpy.GetMessage(2))

