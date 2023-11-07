#set -xe
import subprocess
import argparse
#input=$1
#output=$2
#layers=$3 #["layer1", "layer2", "layer3"]

def create_mbtiles(output, layers):
    layers = layers.split(',')
    #ogr2ogr -f GeoJSON -t_srs epsg:4326 $tmp_geojson $input
    #tippecanoe --layer parcelas -zg -o $output --coalesce-densest-as-needed --extend-zooms-if-still-dropping $tmp_geojson
    # Organiza tus datos en diferentes capas capa1.mbtiles
    #tippecanoe --layer $layer -zg -o $output  --extend-zooms-if-still-dropping $input


    # Luego, genera el mosaico vectorial en el formato deseado (MBTiles)
    #tippecanoe -o salida.mbtiles $layer $layer

    # alternativa
    #tippecanoe -zg -o $output  -L f'{"file":'$input', "layer":'$layer', "description":""}' -L'{"file":'$input2', "layer":'$layer2', "description":""}'

    # Construye el comando Tippecanoe con las capas y archivos de entrada
    command = ["tippecanoe", "-zg", "--force","-o", output]

    for layer in layers:
        #layer_command = f"-L'" + f'{{"file":"./geojson/{layer}.geojson", "layer":"{layer}", "description":""}}'
        layer_command = f"-L'{{\"file\":\"./geojson/{layer}.geojson\", \"layer\":\"{layer}\", \"description\":\"\"}}'"
        command.append(layer_command)

    # Convierte la lista de comandos en una cadena
    command_string = " ".join(command)
    print("##########", command_string)
    # Ejecuta el comando Tippecanoe
    subprocess.call(command_string, shell=True)
    
    """_summary_
    run local
    
    """
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create MBTiles using Tippecanoe")
    parser.add_argument("output", help="Output MBTiles file")
    parser.add_argument("layers", help="Comma List of layers an GeoJSON name Files")
    args = parser.parse_args()

    create_mbtiles(args.output, args.layers)