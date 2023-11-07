from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
import terracotta

app = FastAPI()


# Modelos Pydantic para las peticiones y respuestas
class TilesetCreate(BaseModel):
    name: str
    url: str
    metadata: dict


class TilesetUpdate(BaseModel):
    name: str
    metadata: dict


class Tileset(BaseModel):
    name: str
    url: str
    metadata: dict


# Terracotta Server URL
TERRACOTTA_URL = "http://your-terracotta-server-url"

# Almacén temporal de datos (reemplaza con una base de datos real)
tilesets = {}


def run():
    # Inicializa el servidor
    server = terracotta.Server(config_path="config.json")

    # Carga mosaicos desde un archivo MBTiles
    server["mi_capa"].from_mbtiles("mi_capa.mbtiles")

    server.run()


# Rutas para crear, actualizar y consultar tilesets
@app.post("/tilesets/", response_model=Tileset)
def create_tileset(tileset: TilesetCreate):
    # Tu lógica para crear un tileset en Terracotta, aquí puedes enviar una solicitud POST a Terracotta
    # Ejemplo:
    # response = requests.post(f"{TERRACOTTA_URL}/tilesets", json=tileset.dict())
    # Verifica la respuesta de Terracotta y maneja errores si es necesario
    # Luego, puedes devolver la respuesta de Terracotta o tu propia respuesta personalizada.
    tilesets[tileset.name] = tileset
    return tileset


@app.put("/tilesets/{name}", response_model=Tileset)
def update_tileset(name: str, tileset: TilesetUpdate):
    """
    -o datos_actualizados.mbtiles establece el nombre del archivo MBTiles de salida para los mosaicos de actualización.
    -B8 y -E12 establecen el rango de niveles de zoom a generar.
    -Z10 especifica el nivel de zoom máximo para los mosaicos.
    -l mi_capa establece la capa a la que pertenecen los datos de actualización.
    datos_actualizados.geojson es el archivo GeoJSON que contiene los datos de actualización.
    """
    ##tippecanoe -o datos_actualizados.mbtiles -B8 -E12 -Z10 -l mi_capa datos_actualizados.geojson
    # stop terracota
    ##mb-util datos_original.mbtiles datos_actualizados.mbtiles datos_combinados.mbtiles

    # Tu lógica para actualizar un tileset en Terracotta, aquí puedes enviar una solicitud PUT a Terracotta
    # Ejemplo:
    # response = requests.put(f"{TERRACOTTA_URL}/tilesets/{name}", json=tileset.dict())
    # Verifica la respuesta de Terracotta y maneja errores si es necesario
    # Luego, puedes devolver la respuesta de Terracotta o tu propia respuesta personalizada.
    if name not in tilesets:
        raise HTTPException(status_code=404, detail="Tileset not found")
    tilesets[name].name = tileset.name
    tilesets[name].metadata = tileset.metadata
    return tilesets[name]


@app.get("/tilesets/{name}", response_model=Tileset)
def read_tileset(name: str):
    # Tu lógica para consultar un tileset específico en Terracotta, aquí puedes enviar una solicitud GET a Terracotta
    # Ejemplo:
    # response = requests.get(f"{TERRACOTTA_URL}/tilesets/{name}")
    # Verifica la respuesta de Terracotta y maneja errores si es necesario
    # Luego, puedes devolver la respuesta de Terracotta o tu propia respuesta personalizada.
    if name not in tilesets:
        raise HTTPException(status_code=404, detail="Tileset not found")
    return tilesets[name]


@app.get("/tilesets/", response_model=list[Tileset])
def list_tilesets(
    skip: int = Query(0, description="Número de elementos a omitir"),
    limit: int = Query(10, description="Número de elementos a mostrar"),
):
    # Tu lógica para listar todos los tilesets en Terracotta, aquí puedes enviar una solicitud GET a Terracotta
    # Ejemplo:
    # response = requests.get(f"{TERRACOTTA_URL}/tilesets")
    # Verifica la respuesta de Terracotta y maneja errores si es necesario
    # Luego, puedes devolver la respuesta de Terracotta o tu propia respuesta personalizada.
    tileset_list = list(tilesets.values())[skip : skip + limit]
    return tileset_list
