import ee
import folium

ee.Initialize(project='deft-smile-462318-v2')

blumenau = ee.Geometry.Point([-49.0639, -26.9167])

# Landsat 9 collection with 15m panchromatic resolution
colecao = ee.ImageCollection('LANDSAT/LC09/C02/T1_TOA') \
    .filterBounds(blumenau) \
    .filterDate('2022-01-01', '2024-12-31') \
    .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
    .sort('system:time_start', False)

# Check if collection has images and get the best one
imagem_count = colecao.size()
print(f"Images found: {imagem_count.getInfo()}")

if imagem_count.getInfo() > 0:
    imagem = colecao.first().clip(blumenau.buffer(5000))
else:
    # Fallback to Landsat 8 if no Landsat 9 images
    colecao = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA') \
        .filterBounds(blumenau) \
        .filterDate('2020-01-01', '2024-12-31') \
        .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
        .sort('system:time_start', False)
    imagem = colecao.first().clip(blumenau.buffer(5000))

# Landsat visualization with better detail
vis_params = {
    'min': 0,
    'max': 0.3,
    'bands': ['B4', 'B3', 'B2']
}

mapa = folium.Map(location=[-26.91550, -49.06325], zoom_start=15)

map_id_dict = ee.Image(imagem).getMapId(vis_params)
folium.TileLayer(
    tiles=map_id_dict['tile_fetcher'].url_format,
    attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
    name='Landsat High-Res',
    overlay=True,
    control=True
).add_to(mapa)

folium.LayerControl().add_to(mapa)
mapa.save("mapa_blumenau_landsat.html")
print("✅ Mapa Landsat salvo como mapa_blumenau_landsat.html")