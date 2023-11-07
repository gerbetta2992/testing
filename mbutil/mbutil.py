from mbutil import mbtiles

# Abre el archivo MBTiles principal
mbtiles_original = mbtiles.MBTiles("datos_original.mbtiles")

# Abre el archivo MBTiles de actualización
mbtiles_actualizados = mbtiles.MBTiles("datos_actualizados.mbtiles")

# Combina los mosaicos actualizados en el archivo principal
for tile in mbtiles_actualizados.tiles():
    mbtiles_original[tile.z, tile.x, tile.y] = mbtiles_actualizados[
        tile.z, tile.x, tile.y
    ]

# Guarda el archivo MBTiles combinado
mbtiles_original.commit()

# Cierra los archivos MBTiles
mbtiles_original.close()
mbtiles_actualizados.close()
