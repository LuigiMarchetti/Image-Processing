import requests
import os
import time

API_KEY = ''

locais = [
    {"nome": "Prefeitura", "lat": -26.920284, "lng": -49.065802},
    {"nome": "Vila Germânica", "lat": -26.916834, "lng": -49.071345},
    {"nome": "FURB", "lat": -26.905506359692055, "lng": -49.07903283300831},
    {"nome": "Shopping Neumarkt", "lat": -26.920692, "lng": -49.063726},
    {"nome": "Castelinho da Havan", "lat": -26.922477, "lng": -49.065358},
]

zoom = 18  # quanto maior, mais perto
tamanho = "640x640"  # tamanho máximo permitido para uso gratuito

output_dir = "imagens_blumenau"
os.makedirs(output_dir, exist_ok=True)

for i, local in enumerate(locais):
    url = (
        f"https://maps.googleapis.com/maps/api/staticmap?"
        f"center={local['lat']},{local['lng']}&"
        f"zoom={zoom}&size={tamanho}&maptype=satellite&key={API_KEY}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"{output_dir}/{i+1:02d}_{local['nome'].replace(' ', '_')}.png"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"[✔] Imagem salva: {filename}")
    else:
        print(f"[✖] Falha ao obter imagem de {local['nome']}")
    time.sleep(1)

print("✅ Download concluído.")
