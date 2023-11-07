import tileserver
import json
import os

# Directorio donde se encuentran los archivos GeoJSON
geojson_directory = "/ruta/a/tu/directorio/geojson"

# Obtener la lista de archivos GeoJSON en el directorio
geojson_files = [f for f in os.listdir(geojson_directory) if f.endswith(".geojson")]

# Inicializar el servidor TileServer GL
tileserver.init()

# Crear capas de GeoJSON a partir de los archivos
for geojson_file in geojson_files:
    layer_name = os.path.splitext(geojson_file)[0]

    # Importar el GeoJSON desde el archivo
    with open(os.path.join(geojson_directory, geojson_file)) as f:
        geojson_data = json.load(f)

    # Crear una capa de GeoJSON
    layer = tileserver.create_layer(
        name=layer_name,
        type="geojson",
        data=geojson_data,
        options={"format": "png", "minzoom": 0, "maxzoom": 18},
    )

    # Agregar la capa al servidor
    tileserver.add_layer(layer)

# Iniciar el servidor TileServer GL
tileserver.run()
