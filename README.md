# cadaster_costa_rica
Scripts created during the project "Mantenimiento catastral para el Registro Nacional de Costa Rica"

All the scripts use the arcpy library, and were develop for ArcGIS software versions 9-10.

Description of scripts:

- Borra versiones:
The script automatically deletes the version that the user indicate as an input.

- Crear Version:
The script automatically creates the version that the user indicate as an input.

- Concilio_Posteo_GEOTEC_DEFAULT:
The script makes a conciliation between 2 versions with some parameters indicated in the script body.

- Topologia:
Automatically creates the topology with certain parameters indicated in the script body.

- Montajes:

The script was created to make a visualization of cadastral overlaps (inconsistencia 06-07). Steps:
  1. Gets input parameters from the user (version, location, cadastral map numbers)
  2. Using a pre-design template, the script ensemble a visualization of the overlaps in 3 viewframes plus the legend/info about the overlapping cadastral parcels.
  3. Exports a .pdf document of the visualization outcome
  
