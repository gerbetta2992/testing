from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
import httpx
import subprocess
import requests

from tippecanoe_.tippecanoe import create_mbtiles

router = APIRouter()

TILESERVER_GL_URL = "http://localhost:5100"

MBTILES_PATH = "../tiles/"


# Función para generar mapas con Tippecanoe en segundo plano
@router.post("/generate_tiles/{id}")
def generate_mbtiles(owner_domain: str):  # layers: list,
    try:
        url = f"https://ncan.live/get_groups?owner_domain={owner_domain}&env=dev"
        headers = {"accept": "application/json"}

        response = requests.post(url, headers=headers)
        layers = ""
        if response.status_code == 200:
            layers = response.json()
            print(layers)

        output = f"{owner_domain}.mbtiles"
        # Generar un archivo GeoJSON temporal
        """
        geojson_file = f"{MBTILES_PATH}/{layer_name}.geojson"
        with open(geojson_file, "w") as f:
            json.dump(geojson_data, f)
        """
        # Ejecutar Tippecanoe para generar el archivo MBTiles
        # mbtiles_file = f"{MBTILES_PATH}/{layer_name}.mbtiles"
        # tippecanoe_command = f"tippecanoe -o {mbtiles_file} {geojson_file}"

        # subprocess.run(tippecanoe_command, shell=True, check=True)

        # Eliminar el archivo temporal GeoJSON
        # os.remove(geojson_file)

        stop_tileserver_command = "docker stop tileserver-container-name"
        subprocess.run(stop_tileserver_command, shell=True)

        create_mbtiles(layers, output)

        start_tileserver_command = "docker start tileserver-container-name"
        subprocess.run(start_tileserver_command, shell=True)

        return {"message": f"Mapa {layers} generado exitosamente como MBTiles"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class LayerUpdate(BaseModel):
    name: str  # Nombre de la capa que deseas actualizar
    data: dict  # Datos actualizados en formato GeoJSON u otro formato compatible


@router.put("/update-layer")
async def update_layer_endpoint(layer_update: LayerUpdate):
    try:
        result = await update_layer(layer_update)
        return result
    except HTTPException as e:
        raise e


@router.post("/create-layer")
async def create_layer(layer_data: dict):
    try:
        url = f"{TILESERVER_GL_URL}/layers"  # URL para crear una nueva capa en TileServer GL

        headers = {
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=layer_data, headers=headers)

            if response.status_code == 201:
                return {
                    "message": f"Capa creada exitosamente con ID: {response.json().get('id')}"
                }
            else:
                raise HTTPException(
                    status_code=response.status_code, detail=response.text
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_layer(layer_update: LayerUpdate):
    url = (
        f"{TILESERVER_GL_URL}/layers/{layer_update.name}"  # URL para actualizar la capa
    )

    headers = {
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=layer_update.data, headers=headers)

        if response.status_code == 200:
            return {"message": f"Capa {layer_update.name} actualizada exitosamente"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)


@router.delete("/delete-layer/{layer_name}")
async def delete_layer(layer_name: str):
    try:
        url = f"{TILESERVER_GL_URL}/layers/{layer_name}"  # URL para eliminar una capa en TileServer GL

        async with httpx.AsyncClient() as client:
            response = await client.delete(url)

            if response.status_code == 204:
                return {"message": f"Capa {layer_name} eliminada exitosamente"}
            elif response.status_code == 404:
                raise HTTPException(
                    status_code=404, detail=f"La capa {layer_name} no existe"
                )
            else:
                raise HTTPException(
                    status_code=response.status_code, detail=response.text
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
