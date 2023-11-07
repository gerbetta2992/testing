import os
import json

# Directorio donde se encuentran los archivos GeoJSON
geojson_directory = "/ruta/a/tu/directorio/geojson"

# Directorio de salida para los archivos de configuración TileStache
output_directory = "/ruta/a/tu/directorio/configs"

# Lista de archivos GeoJSON en el directorio
geojson_files = os.listdir(geojson_directory)

# Crear un archivo de configuración TileStache para cada GeoJSON
for geojson_file in geojson_files:
    if geojson_file.endswith(".geojson"):
        # Obtener el nombre base del archivo GeoJSON (sin extensión)
        layer_name = os.path.splitext(geojson_file)[0]

        # Crear un diccionario de configuración para la capa
        layer_config = {
            "provider": {
                "name": "vector",
                "driver": "GeoJSON",
                "parameters": {
                    "file": os.path.join(geojson_directory, geojson_file),
                },
            },
            "projection": "spherical mercator",
        }

        # Crear un diccionario de configuración TileStache completo
        tilestache_config = {
            "layers": {
                layer_name: layer_config,
            },
        }

        # Guardar el archivo de configuración TileStache en el directorio de salida
        output_file = os.path.join(output_directory, f"{layer_name}.json")
        with open(output_file, "w") as cfg_file:
            json.dump(tilestache_config, cfg_file, indent=4)

        print(f"Configuración generada para la capa: {layer_name}")

print("Proceso de generación de configuración completado.")
