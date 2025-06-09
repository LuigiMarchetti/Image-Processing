import ee
import folium

# Inicializa o Earth Engine
ee.Initialize(project='deft-smile-462318-v2')

# Ponto de Blumenau
blumenau = ee.Geometry.Point([-49.0639, -26.9167])

# Coleta de imagens Sentinel-2 com menos de 10% de nuvens
colecao = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(blumenau) \
    .filterDate('2024-01-01', '2024-06-01') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))

# Pega a imagem mediana da coleção
imagem = colecao.median().clip(blumenau.buffer(5000))  # recorta num raio de 5km

# Define visualização com bandas RGB
vis_params = {
    'min': 0,
    'max': 3000,
    'bands': ['B4', 'B3', 'B2']  # Vermelho, Verde, Azul
}

# Cria um mapa com folium
mapa = folium.Map(location=[-26.91550, -49.06325], zoom_start=12)

# Adiciona a camada da imagem ao mapa
map_id_dict = ee.Image(imagem).getMapId(vis_params)
folium.TileLayer(
    tiles=map_id_dict['tile_fetcher'].url_format,
    attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
    name='Sentinel-2',
    overlay=True,
    control=True
).add_to(mapa)

# Adiciona controle de camadas e exibe o mapa
folium.LayerControl().add_to(mapa)
mapa.save("mapa_blumenau.html")
print("✅ Mapa salvo como mapa_blumenau.html. Abra no navegador.")
