import ee
import folium

# Initialize Earth Engine
ee.Initialize(project='deft-smile-462318-v2')  # Replace with your GEE project ID

# Define a specific street area in Blumenau
street_area = ee.Geometry.Polygon([
    [
        [-49.0640, -26.9168],
        [-49.0640, -26.9160],
        [-49.0630, -26.9160],
        [-49.0630, -26.9168],
        [-49.0640, -26.9168]
    ]
])

# Load Sentinel-2 imagery
collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(street_area) \
    .filterDate('2024-01-01', '2024-06-01') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))

# Check if collection has images
size = collection.size().getInfo()
print(f"Number of images in collection: {size}")

if size == 0:
    print("No images found. Try adjusting date range or filters.")
else:
    # Get the most recent image
    image = collection.sort('system:time_start', False).first().clip(street_area)

    # Visualization parameters
    vis_params = {
        'min': 0,
        'max': 3000,
        'bands': ['B4', 'B3', 'B2']  # Red, Green, Blue
    }

    # Create a folium map
    mapa = folium.Map(location=[-26.9164, -49.0635], zoom_start=16)

    # Add the imagery layer
    map_id_dict = ee.Image(image).getMapId(vis_params)
    folium.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data © <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name='Sentinel-2',
        overlay=True,
        control=True
    ).add_to(mapa)

    # Add layer control and save
    folium.LayerControl().add_to(mapa)
    mapa.save("street_map.html")
    print("✅ Map saved as street_map.html. Open in a browser.")