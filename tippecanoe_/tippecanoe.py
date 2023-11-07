import subprocess
import argparse


def create_mbtiles(layers, output):
    """
    run local

    """
    layers = layers.split(",")

    # Construye el comando Tippecanoe con las capas y archivos de entrada
    command = ["tippecanoe", "-zg", "--force", "-o", output]

    for layer in layers:
        # layer_command = f"-L'" + f'{{"file":"./geojson/{layer}.geojson", "layer":"{layer}", "description":""}}'
        layer_command = f'-L\'{{"file":"./geojson/{layer}.geojson", "layer":"{layer}", "description":""}}\''
        command.append(layer_command)

    # Convierte la lista de comandos en una cadena
    command_string = " ".join(command)
    # print("##########", command_string)
    # Ejecuta el comando Tippecanoe
    subprocess.call(command_string, shell=True)


"""  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create MBTiles using Tippecanoe")
    parser.add_argument("layers", help="Comma List of layers an GeoJSON name Files")
    parser.add_argument("output", help="Output MBTiles file")

    args = parser.parse_args()

    create_mbtiles(args.layers, args.output)
"""
