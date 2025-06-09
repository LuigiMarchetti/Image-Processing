import requests
import os
import time
import json
from datetime import datetime

API_KEY = 'PLAK8fd53e5501ec4c96acb0f8384a0828c6'  # Coloque aqui sua API Key da Planet

SESSION = requests.Session()
SESSION.auth = (API_KEY, '')

SEARCH_URL = 'https://api.planet.com/data/v1/quick-search'

# Coordenadas aproximadas da Rua São Paulo, Blumenau
geojson_geometry = {
    "type": "Point",
    "coordinates": [-49.071, -26.920]  # lon, lat
}

def search_images(start_date, end_date, limit=100):
    """Busca imagens de satélite no período especificado"""
    search_request = {
        "item_types": ["PSScene"],  # Tipo de imagem Planet
        "filter": {
            "type": "AndFilter",
            "config": [
                {
                    "type": "GeometryFilter",
                    "field_name": "geometry",
                    "config": geojson_geometry
                },
                {
                    "type": "DateRangeFilter",
                    "field_name": "acquired",
                    "config": {
                        "gte": f"{start_date}T00:00:00.000Z",
                        "lte": f"{end_date}T23:59:59.999Z"
                    }
                },
                {
                    "type": "RangeFilter",
                    "field_name": "cloud_cover",
                    "config": {"lte": 0.1}  # Máximo 10% de cobertura de nuvens
                }
            ]
        },
        "limit": limit
    }

    response = SESSION.post(SEARCH_URL, json=search_request)
    response.raise_for_status()
    return response.json()["features"]

def get_available_assets(item):
    """Obtém lista de assets disponíveis para um item"""
    assets_url = item["_links"]["assets"]
    assets_resp = SESSION.get(assets_url)
    assets_resp.raise_for_status()
    return assets_resp.json()

def activate_asset(item, asset_type="analytic", max_wait_time=300):
    """Ativa um asset específico"""
    assets = get_available_assets(item)

    if asset_type not in assets:
        # Tenta assets alternativos
        alternative_assets = ["visual", "basic_analytic", "basic_udm2"]
        for alt_asset in alternative_assets:
            if alt_asset in assets:
                print(f"Asset {asset_type} não disponível para {item['id']}, usando {alt_asset}")
                asset_type = alt_asset
                break
        else:
            print(f"Nenhum asset compatível disponível para o item {item['id']}")
            print(f"Assets disponíveis: {list(assets.keys())}")
            return None

    asset = assets[asset_type]

    if asset["status"] != "active":
        print(f"Ativando asset {asset_type} para o item {item['id']}...")
        activation_resp = SESSION.post(asset["_links"]["activate"])
        activation_resp.raise_for_status()

        # Esperar ativação com timeout
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            asset_status_resp = SESSION.get(asset["_links"]["self"])
            asset_status_resp.raise_for_status()
            current_asset = asset_status_resp.json()

            if current_asset["status"] == "active":
                print("Ativado!")
                return current_asset
            elif current_asset["status"] == "failed":
                print("Falha na ativação do asset")
                return None
            else:
                print(f"Status: {current_asset['status']}, esperando...")
                time.sleep(10)

        print("Timeout na ativação do asset")
        return None
    else:
        print(f"Asset {asset_type} já está ativo para {item['id']}")
        return asset

def download_asset(asset, item_id, folder="downloads"):
    """Faz download do asset"""
    if not os.path.exists(folder):
        os.makedirs(folder)

    url = asset["location"]
    # Nome mais descritivo para o arquivo
    extension = url.split("/")[-1].split("?")[0].split(".")[-1]
    filename = os.path.join(folder, f"{item_id}.{extension}")

    print(f"Baixando {filename}...")
    try:
        with SESSION.get(url, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f"Download completo: {filename}")
        return filename
    except Exception as e:
        print(f"Erro no download: {e}")
        return None

def save_metadata(items, filename="metadata.json"):
    """Salva metadados das imagens em arquivo JSON"""
    metadata = []
    for item in items:
        metadata.append({
            "id": item["id"],
            "acquired": item["properties"]["acquired"],
            "cloud_cover": item["properties"]["cloud_cover"],
            "pixel_resolution": item["properties"].get("pixel_resolution"),
            "sun_azimuth": item["properties"].get("sun_azimuth"),
            "sun_elevation": item["properties"].get("sun_elevation"),
            "geometry": item["geometry"]
        })

    with open(filename, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadados salvos em {filename}")

def main():
    start_date = "2024-01-01"
    end_date = "2024-12-31"

    print(f"Buscando imagens entre {start_date} e {end_date}...")
    items = search_images(start_date, end_date)
    print(f"Encontradas {len(items)} imagens.")

    # Salvar metadados
    save_metadata(items)

    # Estatísticas
    successful_downloads = 0
    failed_downloads = 0

    for i, item in enumerate(items, 1):
        print(f"\n--- Processando item {i}/{len(items)}: {item['id']} ---")
        print(f"Data de aquisição: {item['properties']['acquired']}")
        print(f"Cobertura de nuvens: {item['properties']['cloud_cover']:.2%}")

        # Tentar diferentes tipos de asset
        for asset_type in ["analytic", "visual", "basic_analytic"]:
            asset = activate_asset(item, asset_type=asset_type)
            if asset:
                downloaded_file = download_asset(asset, item['id'])
                if downloaded_file:
                    successful_downloads += 1
                    break
                else:
                    failed_downloads += 1
        else:
            print(f"Não foi possível baixar nenhum asset para {item['id']}")
            failed_downloads += 1

    print(f"\n=== RESUMO ===")
    print(f"Total de imagens encontradas: {len(items)}")
    print(f"Downloads bem-sucedidos: {successful_downloads}")
    print(f"Downloads falharam: {failed_downloads}")
    print(f"Taxa de sucesso: {successful_downloads/len(items):.1%}")

if __name__ == "__main__":
    main()